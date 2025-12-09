"""Request models for API endpoints."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class DateRange(BaseModel):
    """Date range filter."""
    start: Optional[date] = None
    end: Optional[date] = None


class SearchRequest(BaseModel):
    """Search request model."""
    query: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Natural language search query"
    )
    page: int = Field(
        default=1,
        ge=1,
        description="Page number (1-indexed)"
    )
    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Number of products per page"
    )
    min_confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Minimum confidence score for search results (0.0 - 1.0)"
    )
    include_sales: bool = Field(
        default=True,
        description="Include historical sales data"
    )
    include_forecast: bool = Field(
        default=False,
        description="Include demand forecast"
    )
    include_segments: bool = Field(
        default=False,
        description="Include customer segments"
    )
    include_sales_trend: bool = Field(
        default=True,
        description="Include sales trend with seasonality analysis"
    )
    date_range: Optional[DateRange] = None

    class Config:
        json_schema_extra = {
            "example": {
                "query": "Nike running shoes",
                "page": 1,
                "page_size": 20,
                "min_confidence": 0.5,
                "include_sales": True,
                "include_sales_trend": True,
                "include_forecast": True,
                "include_segments": True
            }
        }
