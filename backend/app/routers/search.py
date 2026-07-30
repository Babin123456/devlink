from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import get_database
from app.schemas.search import SearchAutocompleteResponse
from app.services.search_service import SearchService

router = APIRouter()


@router.get("", summary="Full multi-category search")
def full_search(
    q: str = Query("", max_length=200),
    category: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_database),
):
    """Full-text paginated search across Users, Projects, Organizations, Skills, and Tags."""
    return SearchService.search(
        db=db,
        q=q,
        category=category,
        page=page,
        limit=limit,
    )


@router.get(
    "/autocomplete",
    response_model=SearchAutocompleteResponse,
    summary="Global search autocomplete",
)
def autocomplete(
    q: str = Query("", min_length=0, max_length=100),
    db: Session = Depends(get_database),
):
    """Lightweight autocomplete endpoint returning top matches per category."""
    return SearchService.autocomplete(db=db, q=q)


@router.get(
    "/suggestions",
    response_model=List[str],
    summary="Global search suggestions",
)
def suggestions(
    q: str = Query("", min_length=0, max_length=100),
    limit: int = Query(8, ge=1, le=50),
    db: Session = Depends(get_database),
):
    """Returns a flat list of matching query suggestion strings."""
    return SearchService.suggestions(db=db, q=q, limit=limit)
