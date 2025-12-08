"""Response models for API endpoints."""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class Product(BaseModel):
    """Product response model."""
    article_id: int
    name: str
    type: str
    color: str
    department: str
    price_range: Optional[str] = None
    image_url: Optional[str] = None


class SalesDataPoint(BaseModel):
    """Single sales data point in timeline."""
    date: str
    revenue: float
    transactions: int
    avg_price: float


class SalesSummary(BaseModel):
    """Summary of sales data."""
    total_revenue: float
    total_transactions: int
    date_range: Dict[str, str]


class SalesData(BaseModel):
    """Sales data with timeline and summary."""
    timeline: List[SalesDataPoint]
    summary: SalesSummary


class Insights(BaseModel):
    """AI-generated insights."""
    text: str
    key_findings: List[str]


class ForecastPoint(BaseModel):
    """Single forecast data point."""
    date: str
    predicted_revenue: float
    confidence: str


class Forecast(BaseModel):
    """Demand forecast data."""
    predictions: List[ForecastPoint]
    note: str


class CustomerSegment(BaseModel):
    """Customer segment information."""
    segment: str
    percentage: int
    avg_age: int


class PaginationInfo(BaseModel):
    """Pagination metadata."""
    current_page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_prev: bool


class SearchResponse(BaseModel):
    """Search API response."""
    query: str
    parsed_query: Dict[str, Any]
    products: List[Product]
    pagination: PaginationInfo
    sales_data: Optional[SalesData] = None
    insights: Optional[Insights] = None
    forecast: Optional[Forecast] = None
    customer_segments: Optional[List[CustomerSegment]] = None
    metadata: Dict[str, Any]


class ProductDetailResponse(BaseModel):
    """Product detail API response."""
    article_id: int
    name: str
    type: str
    color: str
    department: str
    section: str
    garment_group: str
    image_url: Optional[str] = None
    sales_summary: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    services: Dict[str, str]
