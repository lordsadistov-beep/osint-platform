import os
import tempfile
from PIL import Image
from PIL.ExifTags import TAGS

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.dependencies import get_current_user
from ...models.user import User
from ...models.search_history import SearchHistory
from ...schemas.tool import MetadataResponse

router = APIRouter()


def extract_exif(filepath: str) -> dict:
    exif_data = {}
    try:
        img = Image.open(filepath)
        info = img._getexif()
        if info:
            for tag_id, value in info.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if isinstance(value, bytes):
                    try:
                        value = value.decode("utf-8", errors="ignore")
                    except Exception:
                        value = str(value)
                exif_data[tag_name] = str(value)
    except Exception:
        pass
    return exif_data


@router.post("/metadata", response_model=MetadataResponse)
async def extract_metadata(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/tiff", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")
    suffix = os.path.splitext(file.filename or "upload")[1] or ".tmp"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    exif = extract_exif(tmp_path)
    os.unlink(tmp_path)
    gps = None
    if "GPSInfo" in exif:
        gps = {"raw": exif["GPSInfo"]}
    result = MetadataResponse(
        filename=file.filename or "unknown",
        size=len(content),
        type=file.content_type or "unknown",
        exif=exif,
        gps=gps,
        created_date=exif.get("DateTimeOriginal"),
        camera=f"{exif.get('Make', '')} {exif.get('Model', '')}".strip(),
        software=exif.get("Software"),
    )
    history = SearchHistory(
        user_id=user.id, tool_slug="metadata", query=file.filename or "unknown",
        result_summary={"type": file.content_type, "exif_count": len(exif)},
    )
    db.add(history)
    await db.flush()
    return result
