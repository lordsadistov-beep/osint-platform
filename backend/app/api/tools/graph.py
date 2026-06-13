from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...core.database import get_db
from ...core.dependencies import get_current_user
from ...models.user import User
from ...models.connection import Connection
from ...schemas.tool import GraphNode, GraphEdge, GraphResponse

router = APIRouter()


@router.post("/graph/{entity_type}/{entity_value}", response_model=GraphResponse)
async def build_graph(
    entity_type: str,
    entity_value: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Connection).where(
            Connection.user_id == user.id,
            ((Connection.source_type == entity_type) & (Connection.source_value == entity_value))
            | ((Connection.target_type == entity_type) & (Connection.target_value == entity_value)),
        )
    )
    connections = result.scalars().all()
    nodes = {}
    edges = []
    src_id = f"{entity_type}:{entity_value}"
    nodes[src_id] = GraphNode(id=src_id, label=entity_value, type=entity_type, value=entity_value)
    for conn in connections:
        tgt_id = f"{conn.target_type}:{conn.target_value}" if conn.source_value == entity_value else f"{conn.source_type}:{conn.source_value}"
        tgt_type = conn.target_type if conn.source_value == entity_value else conn.source_type
        tgt_val = conn.target_value if conn.source_value == entity_value else conn.source_value
        full_id = f"{tgt_type}:{tgt_val}"
        if full_id not in nodes:
            nodes[full_id] = GraphNode(id=full_id, label=tgt_val, type=tgt_type, value=tgt_val)
        edges.append(GraphEdge(source=src_id, target=full_id, relationship=conn.relationship))
    return GraphResponse(nodes=list(nodes.values()), edges=edges)
