from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import get_database
from app.schemas.search import SearchAutocompleteResponse
from app.schemas.search_index import (
    SearchIndexedResponse,
    SearchAnalyticsMetric,
    SearchBenchmarkReport,
)
from app.services.search_service import SearchService
from app.services.search_index_service import SearchIndexService

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


# ---------------------------------------------------------------------
# Optimized Inverted Search Index Endpoints (#647)
# ---------------------------------------------------------------------


@router.get(
    "/indexed",
    response_model=SearchIndexedResponse,
    summary="Optimized global index search",
)
def search_indexed(
    q: str = Query("", max_length=200, description="Search query string"),
    category: Optional[str] = Query(None, description="Resource category: developers, projects, organizations, discussions, skills, technologies"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_database),
):
    """Executes high-performance tokenized search across inverted index with weighted relevance ranking."""
    return SearchIndexService.execute_search(
        db=db,
        query=q,
        category=category,
        limit=limit,
        offset=offset,
    )


@router.post(
    "/index/reindex",
    summary="Reindex global search resources",
)
def reindex_search_resources(
    db: Session = Depends(get_database),
):
    """Rebuilds the inverted search index across developers, projects, organizations, discussions, skills, and technologies."""
    return SearchIndexService.reindex_all(db)


@router.get(
    "/analytics",
    response_model=SearchAnalyticsMetric,
    summary="Get search analytics & latency metrics",
)
def get_search_analytics():
    """Returns search query latency metrics, top search terms, zero-result counts, and category distribution."""
    return SearchIndexService.get_analytics()


@router.get(
    "/benchmark",
    response_model=SearchBenchmarkReport,
    summary="Run search index performance benchmark",
)
def run_search_benchmark(
    q: str = Query("dev", description="Query to benchmark"),
    iterations: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_database),
):
    """Benchmarks query execution latency comparing Inverted Index search vs Naive SQL ILIKE search."""
    return SearchIndexService.run_benchmark(db=db, query=q, iterations=iterations)
