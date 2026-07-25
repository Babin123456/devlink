from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import get_database
from app.schemas.search import (
    SearchAutocompleteResponse,
    SearchResponse,
)
from app.services.search_service import SearchService

router = APIRouter()


# ---------------------------------------------------------------------
# GET /api/search
# ---------------------------------------------------------------------


@router.get(
    "",
    response_model=SearchResponse,
    summary="Global search across all categories",
)
def search(
    q: str = Query("", min_length=0, max_length=200),
    category: Optional[str] = Query(
        None,
        description="One of: developers, projects, organizations, skills, tags. "
        "If omitted, returns top matches from every category.",
    ),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_database),
):
    """Full paginated search across developers, projects, organizations,
    skills, and tags.

    Pass ``category`` to filter to a single category (paginated). Omit it to
    get the top ``limit`` matches from every category.
    """
    return SearchService.search(db, q, category=category, page=page, limit=limit)


# ---------------------------------------------------------------------
# GET /api/search/autocomplete
# ---------------------------------------------------------------------


@router.get(
    "/autocomplete",
    response_model=SearchAutocompleteResponse,
    summary="Global search autocomplete (per-category suggestions)",
)
def autocomplete(
    q: str = Query("", min_length=0, max_length=100),
    db: Session = Depends(get_database),
):
    """Lightweight autocomplete payload returning a few suggestions per
    category (users, projects, organizations, skills, tags).

    Used by the frontend search bar dropdown. Returns empty lists for an
    empty / whitespace-only query.
    """
    return SearchService.autocomplete(db, q)


# ---------------------------------------------------------------------
# GET /api/search/suggestions
# ---------------------------------------------------------------------


@router.get(
    "/suggestions",
    response_model=List[str],
    summary="Flat list of search suggestions",
)
def suggestions(
    q: str = Query("", min_length=0, max_length=100),
    limit: int = Query(8, ge=1, le=20),
    db: Session = Depends(get_database),
):
    """Flat list of suggestion strings for keyboard-navigable dropdowns.

    Combines top matches across all categories into a single deduplicated
    list, ordered: users → projects → organizations → skills → tags.
    """
    return SearchService.suggestions(db, q, limit=limit)
