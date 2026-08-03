from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field


class RequestEndpointMetric(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    endpoint: str = Field(..., description="API path or endpoint group")
    method: str = Field(..., description="HTTP method")
    requests: int = Field(..., description="Total request count for the endpoint")
    avg_response_time_ms: float = Field(
        ..., description="Average response time in milliseconds"
    )
    error_count: int = Field(..., description="Number of 4xx/5xx responses")
    error_rate_pct: float = Field(..., description="Error percentage for the endpoint")


class DailyRequestMetric(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: str = Field(..., description="Date string in YYYY-MM-DD format")
    requests: int = Field(..., description="Total requests on this date")
    errors: int = Field(..., description="Error responses on this date")


class RequestAnalyticsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    timeframe_days: int = Field(..., description="Analysis window length in days")
    total_requests: int = Field(..., description="Total API requests in the window")
    avg_response_time_ms: float = Field(
        ..., description="Average response time across all requests"
    )
    error_rate_pct: float = Field(..., description="Percentage of error responses")
    active_users: int = Field(
        ..., description="Distinct authenticated users with requests in the window"
    )
    rate_limited_requests: int = Field(
        ..., description="Count of requests rejected by rate limiting"
    )
    requests_by_endpoint: List[RequestEndpointMetric] = Field(
        default_factory=list,
        description="Per-endpoint breakdown of requests, latency, and errors",
    )
    daily_trend: List[DailyRequestMetric] = Field(
        default_factory=list,
        description="Daily request and error volume time series",
    )
