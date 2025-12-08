"""API route definitions."""

import time
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_db_client, get_agent_orchestrator
from app.db.duckdb_client import DuckDBClient
from app.agents.orchestrator import AgentOrchestrator
from app.services.product_search import ProductSearchService
from app.services.sales_analyzer import SalesAnalyzerService
from app.services.forecaster import ForecasterService
from app.services.segmenter import SegmenterService
from app.models.requests import SearchRequest
from app.models.responses import (
    SearchResponse,
    ProductDetailResponse,
    HealthResponse,
    PaginationInfo
)
from app.utils.logger import logger

router = APIRouter()


@router.get("/debug/test-search")
async def debug_test_search(db: DuckDBClient = Depends(get_db_client)):
    """Debug endpoint to test product search directly."""
    from app.services.product_search import ProductSearchService

    service = ProductSearchService(db)

    # Test with simple keyword (using new pagination signature)
    results, total_count = service.search(keywords=["shirt"], page=1, page_size=5)

    return {
        "test": "Product search debug",
        "keywords": ["shirt"],
        "found": len(results),
        "total": total_count,
        "products": [
            {
                "id": p.article_id,
                "name": p.name,
                "type": p.type,
                "department": p.department
            }
            for p in results
        ],
        "config_path": db.config.ARTICLES_PATH
    }


@router.get("/debug/data-check")
async def debug_data_check(db: DuckDBClient = Depends(get_db_client)):
    """Debug endpoint to check data access."""
    try:
        # Test basic query
        query = "SELECT COUNT(*) FROM read_parquet(?)"
        result = db.execute(query, [db.config.ARTICLES_PATH])
        total_articles = result[0][0] if result else 0

        # Get sample
        sample_query = "SELECT article_id, prod_name FROM read_parquet(?) LIMIT 5"
        samples = db.execute(sample_query, [db.config.ARTICLES_PATH])

        return {
            "status": "success",
            "articles_path": db.config.ARTICLES_PATH,
            "total_articles": total_articles,
            "samples": [{"id": row[0], "name": row[1]} for row in samples],
            "db_connected": db.is_connected()
        }
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "articles_path": db.config.ARTICLES_PATH
        }


@router.get("/health", response_model=HealthResponse)
async def health_check(
    db: DuckDBClient = Depends(get_db_client),
    agent: AgentOrchestrator = Depends(get_agent_orchestrator)
):
    """
    Health check endpoint.

    Returns:
        Health status of the application and its dependencies
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat() + "Z",
        services={
            "duckdb": "connected" if db.is_connected() else "disconnected",
            "ollama": "connected" if agent.is_ollama_available() else "disconnected",
            "model": agent.model_name
        }
    )


@router.post("/api/search", response_model=SearchResponse)
async def search_products(
    request: SearchRequest,
    db: DuckDBClient = Depends(get_db_client),
    agent: AgentOrchestrator = Depends(get_agent_orchestrator)
):
    """
    Search products using natural language query with pagination.

    Args:
        request: Search request with query and options
        db: DuckDB client (injected)
        agent: LLM agent orchestrator (injected)

    Returns:
        Search response with products, sales data, insights, and pagination info
    """
    start_time = time.time()
    llm_call_count = 0

    logger.info(f"Processing search request: {request.query} (page {request.page}, size {request.page_size})")

    # Step 1: Parse query with LLM
    parsed_query = await agent.parse_query(request.query)
    llm_call_count += 1

    # Step 2: Search products with pagination
    product_service = ProductSearchService(db)
    products, total_count = product_service.search(
        keywords=parsed_query.get('keywords', []),
        filters=parsed_query.get('filters', {}),
        page=request.page,
        page_size=request.page_size
    )

    # Calculate pagination metadata
    total_pages = (total_count + request.page_size - 1) // request.page_size  # Ceiling division
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

    logger.info(
        f"Search completed: {len(products)}/{total_count} products, "
        f"page {request.page}/{total_pages}, "
        f"{processing_time}ms, {llm_call_count} LLM calls"
    )

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


@router.get("/api/products/{article_id}", response_model=ProductDetailResponse)
async def get_product(
    article_id: int,
    include_sales: bool = True,
    db: DuckDBClient = Depends(get_db_client)
):
    """
    Get detailed information about a specific product.

    Args:
        article_id: Product article ID
        include_sales: Include sales summary
        db: DuckDB client (injected)

    Returns:
        Product details with optional sales summary

    Raises:
        HTTPException: If product not found
    """
    logger.info(f"Fetching product details for article_id: {article_id}")

    product_service = ProductSearchService(db)

    try:
        # Get product by ID - this will raise ProductNotFoundException if not found
        product = product_service.get_by_id(article_id)
    except Exception as e:
        logger.error(f"Product not found: {article_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {article_id} not found"
        )

    # Build response
    response_data = {
        "article_id": product.article_id,
        "name": product.name,
        "type": product.type,
        "color": product.color,
        "department": product.department,
        "section": "",  # Not available in search result
        "garment_group": "",  # Not available in search result
        "image_url": product.image_url,
        "sales_summary": None
    }

    # Get sales summary if requested
    if include_sales:
        sales_service = SalesAnalyzerService(db)
        sales_summary = sales_service.get_summary(article_id)
        response_data["sales_summary"] = sales_summary

    return ProductDetailResponse(**response_data)
