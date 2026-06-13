from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from ..core.database import get_db
from ..core.dependencies import get_current_user
from ..models.user import User
from ..models.search_history import SearchHistory
from ..models.lesson import UserProgress
from ..models.challenge import ChallengeSubmission
from ..models.connection import Connection
from ..schemas.dashboard import DashboardStats, HistoryItem, PaginatedHistory, ExportRequest
from ..schemas.graph import ConnectionResponse
from ..schemas.tool import GraphNode, GraphEdge, GraphResponse, SaveConnectionRequest

router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
async def get_stats(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    searches = (await db.execute(select(func.count(SearchHistory.id)).where(SearchHistory.user_id == user.id))).scalar() or 0
    connections = (await db.execute(select(func.count(Connection.id)).where(Connection.user_id == user.id))).scalar() or 0
    lessons_done = (await db.execute(select(func.count(UserProgress.id)).where(UserProgress.user_id == user.id, UserProgress.completed == True))).scalar() or 0
    challenges_solved = (await db.execute(select(func.count(ChallengeSubmission.id)).where(ChallengeSubmission.user_id == user.id, ChallengeSubmission.is_correct == True))).scalar() or 0
    total_users = (await db.execute(select(func.count(User.id)).where(User.is_active == True))).scalar() or 1
    user_rank = (await db.execute(select(func.count(User.id)).where(User.experience > user.experience))).scalar() or 0
    rank_percent = round((user_rank / total_users) * 100, 1) if total_users > 1 else 100.0
    return DashboardStats(
        total_searches=searches,
        total_connections=connections,
        lessons_completed=lessons_done,
        challenges_solved=challenges_solved,
        experience=user.experience,
        level=user.level,
        rank_percent=rank_percent,
    )


@router.get("/history", response_model=PaginatedHistory)
async def get_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(SearchHistory).where(SearchHistory.user_id == user.id).order_by(desc(SearchHistory.created_at))
    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar()
    result = await db.execute(query.offset((page - 1) * limit).limit(limit))
    items = [HistoryItem.from_orm(h) for h in result.scalars().all()]
    return PaginatedHistory(items=items, total=total, page=page, limit=limit)


@router.delete("/history/{id}")
async def delete_history(id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SearchHistory).where(SearchHistory.id == id, SearchHistory.user_id == user.id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="History entry not found")
    await db.delete(item)
    await db.flush()
    return {"success": True}


@router.get("/graph", response_model=GraphResponse)
async def get_graph(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Connection).where(Connection.user_id == user.id))
    connections = result.scalars().all()
    nodes = {}
    edges = []
    for conn in connections:
        src_id = f"{conn.source_type}:{conn.source_value}"
        tgt_id = f"{conn.target_type}:{conn.target_value}"
        if src_id not in nodes:
            nodes[src_id] = GraphNode(id=src_id, label=conn.source_value, type=conn.source_type, value=conn.source_value)
        if tgt_id not in nodes:
            nodes[tgt_id] = GraphNode(id=tgt_id, label=conn.target_value, type=conn.target_type, value=conn.target_value)
        edges.append(GraphEdge(source=src_id, target=tgt_id, relationship=conn.relationship))
    return GraphResponse(nodes=list(nodes.values()), edges=edges)


@router.post("/graph/save", response_model=ConnectionResponse)
async def save_connection(req: SaveConnectionRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    conn = Connection(
        user_id=user.id,
        source_type=req.source_type,
        source_value=req.source_value,
        target_type=req.target_type,
        target_value=req.target_value,
        relationship=req.relationship,
    )
    db.add(conn)
    await db.flush()
    return ConnectionResponse.from_orm(conn)


@router.delete("/graph/{id}")
async def delete_connection(id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Connection).where(Connection.id == id, Connection.user_id == user.id))
    conn = result.scalar_one_or_none()
    if not conn:
        raise HTTPException(status_code=404, detail="Connection not found")
    await db.delete(conn)
    await db.flush()
    return {"success": True}


@router.post("/export")
async def export_data(req: ExportRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Connection).where(Connection.user_id == user.id))
    connections = result.scalars().all()
    data = [{"source": f"{c.source_type}:{c.source_value}", "target": f"{c.target_type}:{c.target_value}", "relationship": c.relationship} for c in connections]
    return {"data": data}
