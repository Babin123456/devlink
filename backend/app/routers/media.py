from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_database
from app.models.user import User
from app.utils.media import MediaStorageManager
from pydantic import BaseModel

router = APIRouter(prefix="/media", tags=["Media"])


class MediaUploadResponse(BaseModel):
    hash: str
    url: str
    thumbnail_url: str
    reused: bool


@router.post(
    "/upload",
    response_model=MediaUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_media(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    """
    Upload an image. The image will be optimized, converted to WebP,
    and a thumbnail will be generated. Duplicate detection is performed.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided.",
        )

    contents = await file.read()
    try:
        result = MediaStorageManager.save_media(
            file_contents=contents,
            filename=file.filename,
            content_type=file.content_type or "",
        )
        return result
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process and store image: {str(exc)}",
        ) from exc
