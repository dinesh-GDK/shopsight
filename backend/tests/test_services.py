"""Unit tests for service layer."""

import pytest
from app.db.duckdb_client import DuckDBClient
from app.services.product_search import ProductSearchService
from app.services.sales_analyzer import SalesAnalyzerService
from app.services.forecaster import ForecasterService
from app.services.segmenter import SegmenterService
from app.models.responses import SalesData, SalesDataPoint, SalesSummary


@pytest.fixture
def db_client():
    """Create DuckDB client for testing."""
    return DuckDBClient()


def test_duckdb_connection(db_client):
    """Test DuckDB connection is working."""
    assert db_client.is_connected()


def test_product_search_basic(db_client):
    """Test basic product search."""
    service = ProductSearchService(db_client)
    results = service.search(keywords=["shirt"], limit=10)

    assert isinstance(results, list)
    assert len(results) <= 10
    if len(results) > 0:
        # Verify product structure
        product = results[0]
        assert hasattr(product, 'article_id')
        assert hasattr(product, 'name')
        assert hasattr(product, 'type')


def test_product_search_with_filters(db_client):
    """Test product search with filters."""
    service = ProductSearchService(db_client)
    results = service.search(
        keywords=["dress"],
        filters={"department": "Divided"},
        limit=10
    )

    assert isinstance(results, list)
    if len(results) > 0:
        # All results should match department filter (case insensitive)
        for product in results:
            assert product.department.lower() == "divided"


def test_product_search_no_results(db_client):
    """Test product search with no matches."""
    service = ProductSearchService(db_client)
    results = service.search(
        keywords=["xyznonexistentproduct123"],
        limit=10
    )

    assert isinstance(results, list)
    assert len(results) == 0


def test_sales_analyzer_get_history(db_client):
    """Test sales history retrieval."""
    service = SalesAnalyzerService(db_client)

    # First, get a valid article ID
    product_service = ProductSearchService(db_client)
    products = product_service.search(keywords=["shirt"], limit=1)

    if len(products) > 0:
        article_id = products[0].article_id
        sales_data = service.get_sales_history(
            article_ids=[article_id],
            granularity="month"
        )

        assert isinstance(sales_data, SalesData)
        assert hasattr(sales_data, 'timeline')
        assert hasattr(sales_data, 'summary')


def test_forecaster_service():
    """Test forecaster service."""
    service = ForecasterService()

    # Create mock sales data
    sales_data = SalesData(
        timeline=[
            SalesDataPoint(date="2020-01-01", revenue=1000, transactions=50, avg_price=20),
            SalesDataPoint(date="2020-02-01", revenue=1200, transactions=60, avg_price=20),
            SalesDataPoint(date="2020-03-01", revenue=1400, transactions=70, avg_price=20),
        ],
        summary=SalesSummary(
            total_revenue=3600,
            total_transactions=180,
            date_range={"start": "2020-01-01", "end": "2020-03-01"}
        )
    )

    forecast = service.predict(sales_data, periods=3)

    assert hasattr(forecast, 'predictions')
    assert hasattr(forecast, 'note')
    assert len(forecast.predictions) == 3
    assert "mocked" in forecast.note.lower()


def test_forecaster_insufficient_data():
    """Test forecaster with insufficient data."""
    service = ForecasterService()

    # Create sales data with only 1 point
    sales_data = SalesData(
        timeline=[
            SalesDataPoint(date="2020-01-01", revenue=1000, transactions=50, avg_price=20),
        ],
        summary=SalesSummary(
            total_revenue=1000,
            total_transactions=50,
            date_range={"start": "2020-01-01", "end": "2020-01-01"}
        )
    )

    forecast = service.predict(sales_data, periods=3)

    assert len(forecast.predictions) == 0
    assert "insufficient" in forecast.note.lower()


def test_segmenter_service(db_client):
    """Test customer segmentation service."""
    service = SegmenterService(db_client)

    # Get a valid article ID
    product_service = ProductSearchService(db_client)
    products = product_service.search(keywords=["shirt"], limit=1)

    if len(products) > 0:
        article_id = products[0].article_id
        segments = service.get_segments([article_id])

        assert isinstance(segments, list)
        assert len(segments) > 0
        # Verify segment structure
        segment = segments[0]
        assert hasattr(segment, 'segment')
        assert hasattr(segment, 'percentage')
        assert hasattr(segment, 'avg_age')
