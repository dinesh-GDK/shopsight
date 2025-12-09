# ShopSight - Backend Specification

**Version:** 1.0
**Date:** December 7, 2024
**Target Audience:** Backend Engineers
**Tech Stack:** Python 3.11, FastAPI, DuckDB, Ollama

---

## Table of Contents
1. [Project Setup](#project-setup)
2. [Architecture Overview](#architecture-overview)
3. [API Endpoints](#api-endpoints)
4. [Data Models](#data-models)
5. [Service Layer](#service-layer)
6. [LLM Agent Implementation](#llm-agent-implementation)
7. [Database Layer](#database-layer)
8. [Error Handling](#error-handling)
9. [Testing Strategy](#testing-strategy)
10. [Deployment](#deployment)

---

## Project Setup

### Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration and environment variables
│   ├── dependencies.py         # Dependency injection
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py           # API route definitions
│   │   └── middleware.py       # CORS, logging middleware
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py     # Main LLM agent logic
│   │   ├── tools.py            # Tool definitions for function calling
│   │   └── prompts.py          # Prompt templates
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── product_search.py   # Product search service (REAL)
│   │   ├── confidence_scorer.py # Search relevance scoring (REAL)
│   │   ├── sales_analyzer.py   # Sales aggregation service (REAL)
│   │   ├── forecaster.py       # Demand forecasting service (MOCKED)
│   │   └── segmenter.py        # Customer segmentation service (MOCKED)
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   └── duckdb_client.py    # DuckDB connection and query helpers
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── requests.py         # Pydantic request models
│   │   ├── responses.py        # Pydantic response models
│   │   └── entities.py         # Domain entities
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py           # Logging configuration
│       └── validators.py       # Custom validators
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_services.py
│   └── test_agents.py
│
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md
```

### Dependencies (requirements.txt)

```txt
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
duckdb==0.9.2

# LLM Integration
ollama==0.1.6

# Data Processing
pandas==2.1.3
numpy==1.26.2

# Utilities
python-dotenv==1.0.0
python-multipart==0.0.6

# CORS
fastapi-cors==0.0.6

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2

# Development
black==23.11.0
ruff==0.1.6
```

### Environment Configuration (.env)

```bash
# Application
APP_NAME=ShopSight
APP_VERSION=1.0.0
DEBUG=True

# API
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=True

# Data Paths
DATA_DIR=../hm_with_images
ARTICLES_PATH=../hm_with_images/articles/*.parquet
CUSTOMERS_PATH=../hm_with_images/customers/*.parquet
TRANSACTIONS_PATH=../hm_with_images/transactions/*.parquet

# LLM
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2
OLLAMA_TIMEOUT=30

# Performance
DUCKDB_THREADS=4
DUCKDB_MEMORY_LIMIT=4GB

# Logging
LOG_LEVEL=INFO
```

---

## Architecture Overview

### Request Flow

```
HTTP Request
    ↓
[FastAPI Router] → Validate request (Pydantic)
    ↓
[API Handler] → Extract parameters
    ↓
[Agent Orchestrator] → Decide which services to call
    ↓
[LLM (Ollama)] → Parse query, generate insights
    ↓
[Services Layer] → Execute business logic
    ↓
[DuckDB Client] → Query parquet files
    ↓
[Response Builder] → Format response (Pydantic)
    ↓
HTTP Response (JSON)
```

### Dependency Injection

```python
# app/dependencies.py
from functools import lru_cache
from app.db.duckdb_client import DuckDBClient
from app.agents.orchestrator import AgentOrchestrator

@lru_cache()
def get_db_client() -> DuckDBClient:
    """Singleton DuckDB client."""
    return DuckDBClient()

@lru_cache()
def get_agent_orchestrator() -> AgentOrchestrator:
    """Singleton LLM agent."""
    return AgentOrchestrator()
```

---

## API Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check if API is running and dependencies are healthy.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-12-07T10:30:00Z",
  "services": {
    "duckdb": "connected",
    "ollama": "connected",
    "model": "llama3.2"
  }
}
```

**Implementation:**
```python
# app/api/routes.py
from fastapi import APIRouter, Depends
from app.dependencies import get_db_client, get_agent_orchestrator

router = APIRouter()

@router.get("/health")
async def health_check(
    db: DuckDBClient = Depends(get_db_client),
    agent: AgentOrchestrator = Depends(get_agent_orchestrator)
):
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "duckdb": "connected" if db.is_connected() else "disconnected",
            "ollama": "connected" if agent.is_ollama_available() else "disconnected",
            "model": agent.model_name
        }
    }
```

---

### 2. Debug Endpoints

**Debug Data Check**

**Endpoint:** `GET /debug/data-check`

**Description:** Verify data file accessibility and connection status.

**Response:**
```json
{
  "status": "success",
  "articles_path": "../hm_with_images/articles/*.parquet",
  "total_articles": 105542,
  "samples": [
    {"id": 108775015, "name": "Strap top"},
    ...
  ],
  "db_connected": true
}
```

**Debug Test Search**

**Endpoint:** `GET /debug/test-search`

**Description:** Test product search directly with hardcoded "shirt" keyword.

**Response:**
```json
{
  "test": "Product search debug",
  "keywords": ["shirt"],
  "found": 5,
  "products": [
    {
      "id": 110065001,
      "name": "OP T-shirt (Idro)",
      "type": "Bra",
      "department": "Clean Lingerie"
    },
    ...
  ],
  "config_path": "../hm_with_images/articles/*.parquet"
}
```

---

### 3. Search Products

**Endpoint:** `POST /api/search`

**Description:** Search products using natural language query and return comprehensive analytics.

**Request Body:**
```json
{
  "query": "Nike running shoes",
  "page": 1,
  "page_size": 20,
  "min_confidence": 0.5,
  "include_sales": true,
  "include_sales_trend": true,
  "include_forecast": true,
  "include_segments": true,
  "date_range": {
    "start": "2019-01-01",
    "end": "2020-09-22"
  }
}
```

**Request Model:**
```python
# app/models/requests.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class DateRange(BaseModel):
    start: Optional[date] = None
    end: Optional[date] = None

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description="Natural language search query")
    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(default=20, ge=1, le=100, description="Number of products per page")
    min_confidence: float = Field(default=0.5, ge=0.0, le=1.0, description="Minimum confidence score (0.0-1.0)")
    include_sales: bool = Field(default=True, description="Include historical sales data")
    include_sales_trend: bool = Field(default=True, description="Include sales trend with seasonality analysis")
    include_forecast: bool = Field(default=False, description="Include demand forecast")
    include_segments: bool = Field(default=False, description="Include customer segments")
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
```

**Response:**
```json
{
  "query": "Nike running shoes",
  "parsed_query": {
    "keywords": ["Nike", "running", "shoes"],
    "attributes": {
      "brand": "Nike",
      "type": "shoes",
      "color": null,
      "style": "running",
      "gender": null,
      "department": null
    },
    "filters": {},
    "intent": "product_search"
  },
  "products": [
    {
      "article_id": 768065001,
      "name": "Nike Air Zoom Pegasus Running Shoe",
      "type": "Sneakers",
      "color": "Black",
      "department": "Sport",
      "price_range": "75-100",
      "image_url": "https://example.com/image.jpg",
      "confidence_score": 0.87
    }
  ],
  "pagination": {
    "current_page": 1,
    "page_size": 20,
    "total_items": 12719,
    "total_pages": 636,
    "has_next": true,
    "has_prev": false
  },
  "sales_data": {
    "timeline": [
      {"date": "2019-01", "revenue": 12500.50, "transactions": 245, "avg_price": 51.02},
      {"date": "2019-02", "revenue": 15200.75, "transactions": 298, "avg_price": 51.01}
    ],
    "summary": {
      "total_revenue": 245000.00,
      "total_transactions": 4832,
      "date_range": {"start": "2018-09-20", "end": "2020-09-22"}
    }
  },
  "insights": {
    "text": "Nike running shoes show strong seasonal demand with peak sales in December 2019...",
    "key_findings": [
      "45% revenue increase during holiday season",
      "Consistent growth trend (+15% YoY)",
      "Price point remains stable around $51"
    ]
  },
  "forecast": {
    "predictions": [
      {"date": "2020-10", "predicted_revenue": 16000, "confidence": "low"}
    ],
    "note": "Forecast based on linear extrapolation (mocked)"
  },
  "customer_segments": [
    {"segment": "Young Professionals", "percentage": 35, "avg_age": 28},
    {"segment": "Fitness Enthusiasts", "percentage": 42, "avg_age": 32}
  ],
  "metadata": {
    "processing_time_ms": 1245,
    "product_count": 20,
    "llm_calls": 2
  }
}
```

**Response Model:**
```python
# app/models/responses.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date

class Product(BaseModel):
    article_id: int
    name: str
    type: str
    color: str
    department: str
    price_range: Optional[str]
    image_url: Optional[str]

class SalesDataPoint(BaseModel):
    date: str
    revenue: float
    transactions: int
    avg_price: float

class SalesSummary(BaseModel):
    total_revenue: float
    total_transactions: int
    date_range: Dict[str, str]

class SalesData(BaseModel):
    timeline: List[SalesDataPoint]
    summary: SalesSummary

class MonthlySalesPoint(BaseModel):
    month: str
    sales: int

class DataQuality(BaseModel):
    months_observed: int
    sparse_data: bool

class SalesTrendData(BaseModel):
    article_id: str
    monthly_sales: List[MonthlySalesPoint]
    seasonality_score: float
    peak_months: List[str]
    data_quality: DataQuality

class Insights(BaseModel):
    text: str
    key_findings: List[str]

class ForecastPoint(BaseModel):
    date: str
    predicted_revenue: float
    confidence: str

class Forecast(BaseModel):
    predictions: List[ForecastPoint]
    note: str

class CustomerSegment(BaseModel):
    segment: str
    percentage: int
    avg_age: int

class PaginationInfo(BaseModel):
    current_page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_prev: bool

class SearchResponse(BaseModel):
    query: str
    parsed_query: Dict[str, Any]
    products: List[Product]
    pagination: PaginationInfo
    sales_data: Optional[SalesData]
    sales_trend: Optional[SalesTrendData]
    insights: Optional[Insights]
    forecast: Optional[Forecast]
    customer_segments: Optional[List[CustomerSegment]]
    metadata: Dict[str, Any]
```

**Implementation:**
```python
# app/api/routes.py
@router.post("/api/search", response_model=SearchResponse)
async def search_products(
    request: SearchRequest,
    db: DuckDBClient = Depends(get_db_client),
    agent: AgentOrchestrator = Depends(get_agent_orchestrator)
):
    start_time = time.time()
    llm_call_count = 0

    # Step 1: Parse query with LLM
    parsed_query = await agent.parse_query(request.query)
    llm_call_count += 1

    # Step 2: Search products with pagination
    product_service = ProductSearchService(db)
    products, total_count = product_service.search(
        keywords=parsed_query['keywords'],
        filters=parsed_query.get('filters', {}),
        page=request.page,
        page_size=request.page_size
    )

    # Calculate pagination metadata
    total_pages = (total_count + request.page_size - 1) // request.page_size
    has_next = request.page < total_pages
    has_prev = request.page > 1

    pagination = PaginationInfo(
        current_page=request.page,
        page_size=request.page_size,
        total_items=total_count,
        total_pages=total_pages,
        has_next=has_next,
        has_prev=has_prev
    )

    # Step 3: Get sales data if requested
    sales_data = None
    if request.include_sales and products:
        sales_service = SalesAnalyzerService(db)
        article_ids = [p.article_id for p in products]
        sales_data = sales_service.get_sales_history(
            article_ids=article_ids,
            date_range=request.date_range
        )

    # Step 4: Generate insights with LLM
    insights = None
    if sales_data and sales_data.timeline:
        insights = await agent.generate_insights(products, sales_data)
        llm_call_count += 1

    # Step 5: Get forecast if requested
    forecast = None
    if request.include_forecast and sales_data:
        forecast_service = ForecasterService()
        forecast = forecast_service.predict(sales_data)

    # Step 6: Get customer segments if requested
    segments = None
    if request.include_segments and products:
        segment_service = SegmenterService(db)
        article_ids = [p.article_id for p in products]
        segments = segment_service.get_segments(article_ids)

    # Build response
    processing_time = int((time.time() - start_time) * 1000)

    return SearchResponse(
        query=request.query,
        parsed_query=parsed_query,
        products=products,
        pagination=pagination,
        sales_data=sales_data,
        insights=insights,
        forecast=forecast,
        customer_segments=segments,
        metadata={
            "processing_time_ms": processing_time,
            "product_count": len(products),
            "llm_calls": llm_call_count
        }
    )
```

---

### 4. Get Product Details

**Endpoint:** `GET /api/products/{article_id}`

**Description:** Get detailed information about a specific product.

**Path Parameters:**
- `article_id` (int): Product identifier

**Query Parameters:**
- `include_sales` (bool): Include sales history (default: true)

**Response:**
```json
{
  "article_id": 768065001,
  "name": "Nike Air Zoom Pegasus Running Shoe",
  "type": "Sneakers",
  "color": "Black",
  "department": "Sport",
  "section": "Womens Sport",
  "garment_group": "Shoes",
  "image_url": "https://example.com/image.jpg",
  "sales_summary": {
    "total_revenue": 45000,
    "total_transactions": 892,
    "first_sale": "2018-09-20",
    "last_sale": "2020-09-22"
  }
}
```

**Implementation:**
```python
@router.get("/api/products/{article_id}")
async def get_product(
    article_id: int,
    include_sales: bool = True,
    db: DuckDBClient = Depends(get_db_client)
):
    product_service = ProductSearchService(db)
    product = product_service.get_by_id(article_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if include_sales:
        sales_service = SalesAnalyzerService(db)
        sales_summary = sales_service.get_summary(article_id)
        product.sales_summary = sales_summary

    return product
```

---

## Data Models

### Domain Entities

```python
# app/models/entities.py
from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Article:
    article_id: int
    prod_name: str
    product_type_name: str
    product_group_name: str
    colour_group_name: str
    department_name: str
    section_name: str
    garment_group_name: str
    index_name: Optional[str]  # Image URL

@dataclass
class Customer:
    customer_id: str
    age: Optional[int]
    postal_code: Optional[str]
    club_member_status: Optional[str]
    fashion_news_frequency: Optional[str]

@dataclass
class Transaction:
    transaction_id: str
    t_dat: date
    article_id: int
    customer_id: str
    price: float
    sales_channel_id: int
```

---

## Service Layer

### 1. Product Search Service (REAL)

```python
# app/services/product_search.py
from typing import List, Dict, Optional, Tuple
from app.db.duckdb_client import DuckDBClient
from app.models.responses import Product

class ProductSearchService:
    def __init__(self, db: DuckDBClient):
        self.db = db

    def _build_where_clause(
        self,
        keywords: List[str],
        filters: Optional[Dict] = None
    ) -> Tuple[str, List]:
        """Build WHERE clause and parameters for search query."""
        if filters is None:
            filters = {}

        where_clauses = []
        params = []

        # Add keyword search clauses
        for keyword in keywords:
            where_clauses.append(
                "(LOWER(prod_name) LIKE ? OR LOWER(product_type_name) LIKE ?)"
            )
            keyword_pattern = f"%{keyword.lower()}%"
            params.append(keyword_pattern)
            params.append(keyword_pattern)

        # Separate keyword clauses from filter clauses
        keyword_clauses = []
        filter_clauses = []

        for i, keyword in enumerate(keywords):
            keyword_clauses.append(where_clauses[i])

        # Add filters (must match ALL filters with AND)
        if filters.get('department'):
            filter_clauses.append("LOWER(department_name) = ?")
            params.append(filters['department'].lower())

        if filters.get('color'):
            filter_clauses.append("LOWER(colour_group_name) = ?")
            params.append(filters['color'].lower())

        # Combine: keywords with OR, filters with AND
        where_parts = []
        if keyword_clauses:
            where_parts.append("(" + " OR ".join(keyword_clauses) + ")")
        if filter_clauses:
            where_parts.append(" AND ".join(filter_clauses))

        where_sql = " AND ".join(where_parts) if where_parts else "1=1"

        return where_sql, params

    def get_count(
        self,
        keywords: List[str],
        filters: Optional[Dict] = None
    ) -> int:
        """Get total count of products matching search criteria."""
        where_sql, params = self._build_where_clause(keywords, filters)

        query = f"""
        SELECT COUNT(*)
        FROM read_parquet(?)
        WHERE {where_sql}
        """

        result = self.db.execute(
            query,
            [self.db.config.articles_path] + params
        )
        return result[0][0] if result else 0

    def search(
        self,
        keywords: List[str],
        filters: Optional[Dict] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Product], int]:
        """
        Search products by keywords and filters with pagination.

        Args:
            keywords: List of search terms (e.g., ["Nike", "running", "shoes"])
            filters: Additional filters (e.g., {"department": "Sport"})
            page: Page number (1-indexed)
            page_size: Number of results per page

        Returns:
            Tuple of (products list, total count)
        """
        if filters is None:
            filters = {}

        # Build WHERE clause
        where_sql, params = self._build_where_clause(keywords, filters)

        # Calculate offset
        offset = (page - 1) * page_size

        query = f"""
        SELECT
            article_id,
            prod_name as name,
            product_type_name as type,
            colour_group_name as color,
            department_name as department,
            image_url as image_url
        FROM read_parquet(?)
        WHERE {where_sql}
        LIMIT ? OFFSET ?
        """

        # Execute query
        result = self.db.execute(
            query,
            [self.db.config.articles_path] + params + [page_size, offset]
        )

        # Convert to Product objects
        products = [
            Product(
                article_id=row[0],
                name=row[1],
                type=row[2],
                color=row[3],
                department=row[4],
                price_range=None,
                image_url=row[5]
            )
            for row in result
        ]

        # Get total count
        total_count = self.get_count(keywords, filters)

        return products, total_count

    def get_by_id(self, article_id: int) -> Optional[Product]:
        """Get single product by ID."""
        query = """
        SELECT
            article_id,
            prod_name,
            product_type_name,
            colour_group_name,
            department_name,
            section_name,
            garment_group_name,
            index_name
        FROM read_parquet(?)
        WHERE article_id = ?
        """

        result = self.db.execute(
            query,
            [self.db.config.articles_path, article_id]
        )

        if not result:
            return None

        row = result[0]
        return Product(
            article_id=row[0],
            name=row[1],
            type=row[2],
            color=row[3],
            department=row[4],
            image_url=row[7]
        )
```

---

### 1.5. Confidence Scorer Service (REAL)

**Purpose:** Calculate relevance confidence scores for search results to improve search quality and enable intelligent filtering.

```python
# app/services/confidence_scorer.py
import re
from typing import Dict, List, Optional

class ConfidenceScorer:
    """
    Calculate confidence scores for search results based on attribute matching.

    Scoring weights:
    - Brand match: 35%
    - Type match: 30%
    - Color match: 20%
    - Name match: 15%
    """

    BRAND_WEIGHT = 0.35
    TYPE_WEIGHT = 0.30
    COLOR_WEIGHT = 0.20
    NAME_WEIGHT = 0.15

    @staticmethod
    def _contains_word(text: str, word: str) -> bool:
        """
        Check if word exists using word boundary matching.

        Prevents false positives like "Nike" matching "Jannike".
        Uses regex: \b word \b
        """
        if not text or not word:
            return False
        pattern = r'\b' + re.escape(word.lower()) + r'\b'
        return bool(re.search(pattern, text.lower()))

    def score_product(
        self,
        product: Dict,
        parsed_query: Dict
    ) -> float:
        """
        Calculate confidence score (0.0 - 1.0) for a product.

        Args:
            product: Product dict with fields (name, type, color, etc.)
            parsed_query: Parsed query with keywords and attributes

        Returns:
            Confidence score between 0.0 and 1.0

        Example:
            product = {
                "name": "Nike Running Shoes Elite",
                "type": "Shoes",
                "color": "Black",
                "department": "Sport",
                "index_name": "Nike"
            }

            parsed_query = {
                "keywords": ["Nike", "running", "shoes"],
                "attributes": {
                    "brand": "Nike",
                    "type": "shoes",
                    "color": None
                }
            }

            score = scorer.score_product(product, parsed_query)
            # Returns: ~0.87 (high match)
        """
        attributes = parsed_query.get("attributes", {})
        keywords = parsed_query.get("keywords", [])

        brand_score = self._score_brand(product, attributes.get("brand"))
        type_score = self._score_type(product, attributes.get("type"))
        color_score = self._score_color(product, attributes.get("color"))
        name_score = self._score_name(product, keywords)

        confidence = (
            brand_score * self.BRAND_WEIGHT +
            type_score * self.TYPE_WEIGHT +
            color_score * self.COLOR_WEIGHT +
            name_score * self.NAME_WEIGHT
        )

        return round(max(0.0, min(1.0, confidence)), 3)

    def score_products_batch(
        self,
        products: List[Dict],
        parsed_query: Dict
    ) -> List[Dict]:
        """Score multiple products and add confidence_score field."""
        scored_products = []
        for product in products:
            confidence = self.score_product(product, parsed_query)
            product_with_score = {**product, "confidence_score": confidence}
            scored_products.append(product_with_score)
        return scored_products
```

**Key Features:**
- **Word Boundary Matching:** Prevents "Nike" from matching "Jannike"
- **Weighted Scoring:** Brand and type are weighted higher than color
- **Batch Processing:** Efficiently scores multiple products
- **Transparent:** Score breakdown helps users understand relevance

**Integration with ProductSearchService:**
```python
# In ProductSearchService.search_with_confidence()
scorer = ConfidenceScorer()
scored_products = scorer.score_products_batch(candidates, parsed_query)

# Filter by minimum confidence
filtered_products = [
    p for p in scored_products
    if p["confidence_score"] >= min_confidence
]

# Sort by confidence (descending)
filtered_products.sort(key=lambda p: p["confidence_score"], reverse=True)
```

---

### 2. Sales Analyzer Service (REAL)

```python
# app/services/sales_analyzer.py
from typing import List, Optional
from datetime import date
import pandas as pd
from app.db.duckdb_client import DuckDBClient
from app.models.responses import SalesData, SalesDataPoint, SalesSummary
from app.models.requests import DateRange

class SalesAnalyzerService:
    def __init__(self, db: DuckDBClient):
        self.db = db

    def get_sales_history(
        self,
        article_ids: List[int],
        date_range: Optional[DateRange] = None,
        granularity: str = "month"  # day, week, month
    ) -> SalesData:
        """
        Get sales history for products.

        Args:
            article_ids: List of product IDs
            date_range: Optional date filter
            granularity: Aggregation level (day/week/month)

        Returns:
            SalesData with timeline and summary
        """
        # Build date filter
        date_filter = "1=1"
        params = [self.db.config.transactions_path]

        if date_range and date_range.start:
            date_filter += " AND t_dat >= ?"
            params.append(date_range.start)

        if date_range and date_range.end:
            date_filter += " AND t_dat <= ?"
            params.append(date_range.end)

        # Build article filter
        article_filter = f"article_id IN ({','.join(['?'] * len(article_ids))})"
        params.extend(article_ids)

        # Determine DATE_TRUNC function
        trunc_func = {
            "day": "DATE_TRUNC('day', t_dat)",
            "week": "DATE_TRUNC('week', t_dat)",
            "month": "DATE_TRUNC('month', t_dat)"
        }[granularity]

        query = f"""
        SELECT
            {trunc_func} as period,
            COUNT(*) as transaction_count,
            SUM(price) as total_revenue,
            AVG(price) as avg_price,
            COUNT(DISTINCT customer_id) as unique_customers
        FROM read_parquet(?)
        WHERE {date_filter} AND {article_filter}
        GROUP BY period
        ORDER BY period
        """

        # Execute and convert to DataFrame
        df = self.db.query_to_df(query, params)

        # Build timeline
        timeline = [
            SalesDataPoint(
                date=row['period'].strftime('%Y-%m-%d'),
                revenue=float(row['total_revenue']),
                transactions=int(row['transaction_count']),
                avg_price=float(row['avg_price'])
            )
            for _, row in df.iterrows()
        ]

        # Build summary
        summary = SalesSummary(
            total_revenue=float(df['total_revenue'].sum()),
            total_transactions=int(df['transaction_count'].sum()),
            date_range={
                "start": df['period'].min().strftime('%Y-%m-%d'),
                "end": df['period'].max().strftime('%Y-%m-%d')
            }
        )

        return SalesData(timeline=timeline, summary=summary)

    def get_summary(self, article_id: int) -> dict:
        """Get sales summary for a single product."""
        query = """
        SELECT
            COUNT(*) as total_transactions,
            SUM(price) as total_revenue,
            MIN(t_dat) as first_sale,
            MAX(t_dat) as last_sale
        FROM read_parquet(?)
        WHERE article_id = ?
        """

        result = self.db.execute(
            query,
            [self.db.config.transactions_path, article_id]
        )

        if not result:
            return None

        row = result[0]
        return {
            "total_transactions": row[0],
            "total_revenue": float(row[1]),
            "first_sale": row[2].strftime('%Y-%m-%d'),
            "last_sale": row[3].strftime('%Y-%m-%d')
        }
```

---

### 3. Forecaster Service (MOCKED)

```python
# app/services/forecaster.py
from typing import List
import pandas as pd
from app.models.responses import Forecast, ForecastPoint, SalesData

class ForecasterService:
    """
    Mocked demand forecasting service.
    Uses simple linear extrapolation from last 3 months.
    """

    def predict(
        self,
        sales_data: SalesData,
        periods: int = 3
    ) -> Forecast:
        """
        Generate forecast for next N periods.

        Args:
            sales_data: Historical sales data
            periods: Number of future periods to predict

        Returns:
            Forecast with predictions and confidence note
        """
        # Convert to DataFrame
        df = pd.DataFrame([
            {
                'date': pd.to_datetime(dp.date),
                'revenue': dp.revenue
            }
            for dp in sales_data.timeline
        ])

        if len(df) < 3:
            # Not enough data for forecast
            return Forecast(
                predictions=[],
                note="Insufficient historical data for forecasting (mocked)"
            )

        # Simple linear extrapolation from last 3 points
        last_3 = df.tail(3)
        avg_growth = (last_3['revenue'].iloc[-1] - last_3['revenue'].iloc[0]) / 2

        predictions = []
        last_date = df['date'].max()
        last_revenue = df['revenue'].iloc[-1]

        for i in range(1, periods + 1):
            future_date = last_date + pd.DateOffset(months=i)
            predicted_revenue = max(0, last_revenue + (avg_growth * i))

            predictions.append(ForecastPoint(
                date=future_date.strftime('%Y-%m'),
                predicted_revenue=round(predicted_revenue, 2),
                confidence="low"
            ))

        return Forecast(
            predictions=predictions,
            note="Forecast based on linear extrapolation from last 3 months (mocked data)"
        )
```

---

### 4. Segmenter Service (MOCKED)

```python
# app/services/segmenter.py
from typing import List
from app.db.duckdb_client import DuckDBClient
from app.models.responses import CustomerSegment

class SegmenterService:
    """
    Mocked customer segmentation service.
    Uses rule-based segmentation on customer demographics.
    """

    def __init__(self, db: DuckDBClient):
        self.db = db

    def get_segments(self, article_ids: List[int]) -> List[CustomerSegment]:
        """
        Get customer segments for products.

        Args:
            article_ids: List of product IDs

        Returns:
            List of customer segments with demographics
        """
        # Query customers who bought these products
        article_filter = f"article_id IN ({','.join(['?'] * len(article_ids))})"

        query = f"""
        SELECT
            c.age,
            c.club_member_status
        FROM read_parquet(?) t
        JOIN read_parquet(?) c ON t.customer_id = c.customer_id
        WHERE {article_filter} AND c.age IS NOT NULL
        """

        params = [
            self.db.config.transactions_path,
            self.db.config.customers_path
        ] + article_ids

        df = self.db.query_to_df(query, params)

        if df.empty:
            # Return default segments if no data
            return self._default_segments()

        # Simple rule-based segmentation
        segments = []

        # Segment by age
        young = df[df['age'] < 30]
        middle = df[(df['age'] >= 30) & (df['age'] < 50)]
        mature = df[df['age'] >= 50]

        total = len(df)

        if len(young) > 0:
            segments.append(CustomerSegment(
                segment="Young Professionals (18-29)",
                percentage=int((len(young) / total) * 100),
                avg_age=int(young['age'].mean())
            ))

        if len(middle) > 0:
            segments.append(CustomerSegment(
                segment="Established Adults (30-49)",
                percentage=int((len(middle) / total) * 100),
                avg_age=int(middle['age'].mean())
            ))

        if len(mature) > 0:
            segments.append(CustomerSegment(
                segment="Mature Customers (50+)",
                percentage=int((len(mature) / total) * 100),
                avg_age=int(mature['age'].mean())
            ))

        return segments

    def _default_segments(self) -> List[CustomerSegment]:
        """Return default segments when no data available."""
        return [
            CustomerSegment(segment="Young Professionals", percentage=35, avg_age=28),
            CustomerSegment(segment="Fitness Enthusiasts", percentage=42, avg_age=32),
            CustomerSegment(segment="Casual Shoppers", percentage=23, avg_age=41)
        ]
```

---

## LLM Agent Implementation

### Agent Orchestrator

```python
# app/agents/orchestrator.py
import ollama
import json
from typing import Dict, Any, List
from app.agents.prompts import QUERY_PARSER_PROMPT, INSIGHT_GENERATOR_PROMPT
from app.models.responses import Product, SalesData, Insights

class AgentOrchestrator:
    def __init__(self, model: str = "llama3.2", host: str = "http://localhost:11434"):
        self.model = model
        self.client = ollama.Client(host=host)

    def is_ollama_available(self) -> bool:
        """Check if Ollama is running."""
        try:
            self.client.list()
            return True
        except Exception:
            return False

    async def parse_query(self, query: str) -> Dict[str, Any]:
        """
        Parse natural language query into structured search parameters.

        Args:
            query: User's search query (e.g., "Nike running shoes under $50")

        Returns:
            Dict with keywords, filters, and intent
        """
        prompt = QUERY_PARSER_PROMPT.format(query=query)

        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a query parser for e-commerce search. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.1}
            )

            # Parse JSON from response
            content = response['message']['content']
            # Extract JSON if wrapped in markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            parsed = json.loads(content)
            return parsed

        except Exception as e:
            # Fallback to simple keyword extraction
            keywords = [word for word in query.split() if len(word) > 2]
            return {
                "keywords": keywords,
                "filters": {},
                "intent": "product_search"
            }

    async def generate_insights(
        self,
        products: List[Product],
        sales_data: SalesData
    ) -> Insights:
        """
        Generate AI insights from sales data.

        Args:
            products: List of products
            sales_data: Sales history data

        Returns:
            Insights object with text and key findings
        """
        # Prepare context
        product_names = [p.name for p in products[:5]]  # Limit to top 5
        total_revenue = sales_data.summary.total_revenue
        total_txns = sales_data.summary.total_transactions

        # Find peak month
        timeline_df = pd.DataFrame([
            {'date': dp.date, 'revenue': dp.revenue}
            for dp in sales_data.timeline
        ])
        peak_month = timeline_df.loc[timeline_df['revenue'].idxmax(), 'date']
        peak_revenue = timeline_df['revenue'].max()

        context = {
            "products": product_names,
            "total_revenue": f"${total_revenue:,.2f}",
            "total_transactions": total_txns,
            "date_range": sales_data.summary.date_range,
            "peak_month": peak_month,
            "peak_revenue": f"${peak_revenue:,.2f}"
        }

        prompt = INSIGHT_GENERATOR_PROMPT.format(context=json.dumps(context, indent=2))

        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a business analyst generating insights from e-commerce data."},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.3}
            )

            insight_text = response['message']['content']

            # Extract key findings (simple heuristic)
            key_findings = [
                f"Total revenue: ${total_revenue:,.2f}",
                f"Peak sales in {peak_month}",
                f"{total_txns:,} total transactions"
            ]

            return Insights(
                text=insight_text,
                key_findings=key_findings
            )

        except Exception as e:
            # Fallback insights
            return Insights(
                text=f"Products generated ${total_revenue:,.2f} in revenue across {total_txns:,} transactions.",
                key_findings=[
                    f"Peak month: {peak_month}",
                    f"Average transaction value: ${total_revenue/total_txns:.2f}"
                ]
            )
```

### Prompt Templates

```python
# app/agents/prompts.py

QUERY_PARSER_PROMPT = """
Parse this e-commerce search query into structured JSON.

Query: "{query}"

Extract:
1. Keywords: Main search terms (brand, category, product type)
2. Filters: Specific constraints (price, color, department)
3. Intent: What the user wants (product_search, sales_analysis, comparison)

Return JSON format:
{{
    "keywords": ["keyword1", "keyword2"],
    "filters": {{"key": "value"}},
    "intent": "product_search"
}}

Examples:
Query: "Nike running shoes"
Output: {{"keywords": ["Nike", "running", "shoes"], "filters": {{}}, "intent": "product_search"}}

Query: "Women's jackets under $50"
Output: {{"keywords": ["women", "jackets"], "filters": {{"price_max": 50}}, "intent": "product_search"}}

Now parse: "{query}"
"""

INSIGHT_GENERATOR_PROMPT = """
Analyze this e-commerce sales data and generate 2-3 actionable business insights.

Data:
{context}

Generate insights that:
1. Identify trends and patterns
2. Highlight peak performance periods
3. Provide actionable recommendations

Write in a professional but conversational tone. Focus on "why" not just "what".
Keep insights concise (2-3 sentences total).
"""
```

---

## Database Layer

### DuckDB Client

```python
# app/db/duckdb_client.py
import duckdb
import pandas as pd
from typing import List, Any, Optional
from app.config import settings

class DuckDBClient:
    def __init__(self):
        # In-memory database
        self.conn = duckdb.connect(':memory:')

        # Configure performance
        self.conn.execute(f"SET threads TO {settings.DUCKDB_THREADS}")
        self.conn.execute(f"SET memory_limit = '{settings.DUCKDB_MEMORY_LIMIT}'")

        self.config = settings

    def is_connected(self) -> bool:
        """Check if connection is alive."""
        try:
            self.conn.execute("SELECT 1")
            return True
        except:
            return False

    def execute(self, query: str, params: List[Any] = None) -> List[tuple]:
        """
        Execute SQL query and return results as list of tuples.

        Args:
            query: SQL query string (use ? for parameters)
            params: Query parameters

        Returns:
            List of result tuples
        """
        if params:
            result = self.conn.execute(query, params)
        else:
            result = self.conn.execute(query)

        return result.fetchall()

    def query_to_df(self, query: str, params: List[Any] = None) -> pd.DataFrame:
        """
        Execute SQL query and return results as pandas DataFrame.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            DataFrame with query results
        """
        if params:
            result = self.conn.execute(query, params)
        else:
            result = self.conn.execute(query)

        return result.df()

    def close(self):
        """Close database connection."""
        self.conn.close()
```

---

## Error Handling

### Exception Classes

```python
# app/utils/exceptions.py
class ShopSightException(Exception):
    """Base exception for ShopSight."""
    pass

class ProductNotFoundException(ShopSightException):
    """Raised when product is not found."""
    pass

class LLMServiceException(ShopSightException):
    """Raised when LLM service fails."""
    pass

class DatabaseException(ShopSightException):
    """Raised when database operation fails."""
    pass
```

### Global Exception Handler

```python
# app/api/middleware.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.utils.exceptions import ShopSightException

@app.exception_handler(ShopSightException)
async def shopsight_exception_handler(request: Request, exc: ShopSightException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": exc.__class__.__name__,
            "message": str(exc)
        }
    )

@app.exception_handler(ProductNotFoundException)
async def product_not_found_handler(request: Request, exc: ProductNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "Product not found", "message": str(exc)}
    )
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_services.py
import pytest
from app.services.product_search import ProductSearchService
from app.db.duckdb_client import DuckDBClient

@pytest.fixture
def db_client():
    return DuckDBClient()

def test_product_search_with_keywords(db_client):
    service = ProductSearchService(db_client)
    results = service.search(keywords=["shirt"], limit=10)

    assert len(results) > 0
    assert all("shirt" in p.name.lower() for p in results)

def test_product_search_with_filters(db_client):
    service = ProductSearchService(db_client)
    results = service.search(
        keywords=["shoes"],
        filters={"department": "Sport"},
        limit=10
    )

    assert all(p.department.lower() == "sport" for p in results)
```

### Integration Tests

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_search_endpoint():
    response = client.post(
        "/api/search",
        json={"query": "Nike shoes", "limit": 10}
    )
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert len(data["products"]) > 0
```

---

## Deployment

### Running Locally

```bash
# Setup with Conda (Recommended)
conda env create -f environment.yml
conda activate shopsight-backend

# Or setup with pip
pip install -r requirements.txt

# Start Ollama (separate terminal)
ollama serve
ollama pull llama3.2

# Start API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the automated startup script
./start.sh
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Performance Benchmarks

Expected performance on modern hardware (8GB RAM, 4-core CPU):

| Operation | Target | Measured |
|-----------|--------|----------|
| Product search (10 results) | < 100ms | ~50ms |
| Sales aggregation (1 product, 2 years) | < 300ms | ~200ms |
| LLM query parsing | < 3s | ~2s |
| LLM insight generation | < 5s | ~4s |
| Full search request | < 8s | ~6s |

---

**End of Backend Specification**

For questions or clarifications, contact the engineering lead.
