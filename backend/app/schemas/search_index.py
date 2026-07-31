from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class SearchIndexedResultItem(BaseModel):
    id: str
    entity_type: str  # developers, projects, organizations, discussions, skills, technologies
    title: str
    description: Optional[str] = None
    score: float
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SearchIndexedResponse(BaseModel):
    query: str
    category: Optional[str] = None
    total_results: int
    execution_time_ms: float
    results: List[SearchIndexedResultItem]


class SearchAnalyticsMetric(BaseModel):
    total_searches: int
    avg_latency_ms: float
    top_queries: List[Dict[str, Any]]
    zero_result_queries: List[Dict[str, Any]]
    category_distribution: Dict[str, int]


class SearchBenchmarkReport(BaseModel):
    query: str
    iterations: int
    naive_sql_avg_ms: float
    inverted_index_avg_ms: float
    latency_reduction_percent: float
    speedup_factor: float
    status: str
