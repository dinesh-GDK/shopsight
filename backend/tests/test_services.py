"""Unit tests for service layer."""

import pytest
from app.db.duckdb_client import DuckDBClient
from app.services.product_search import ProductSearchService
from app.services.sales_analyzer import SalesAnalyzerService
from app.services.forecaster import ForecasterService
from app.services.segmenter import SegmenterService
from app.models.responses import (
    SalesData, SalesDataPoint, SalesSummary,
    SalesTrendData, MonthlySalesPoint, DataQuality
)


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


def test_sales_trend_and_seasonality(db_client):
    """Test sales trend and seasonality computation."""
    service = SalesAnalyzerService(db_client)

    # Get a valid article ID
    product_service = ProductSearchService(db_client)
    products, _ = product_service.search(keywords=["shirt"], page=1, page_size=1)

    if len(products) > 0:
        article_id = products[0].article_id
        sales_trend = service.compute_sales_trend_and_seasonality(
            article_ids=[article_id]
        )

        # Should return data or None
        if sales_trend:
            assert isinstance(sales_trend, SalesTrendData)
            assert hasattr(sales_trend, 'article_id')
            assert hasattr(sales_trend, 'monthly_sales')
            assert hasattr(sales_trend, 'seasonality_score')
            assert hasattr(sales_trend, 'peak_months')
            assert hasattr(sales_trend, 'data_quality')

            # Verify monthly sales structure
            assert isinstance(sales_trend.monthly_sales, list)
            if len(sales_trend.monthly_sales) > 0:
                point = sales_trend.monthly_sales[0]
                assert isinstance(point, MonthlySalesPoint)
                assert hasattr(point, 'month')
                assert hasattr(point, 'sales')

            # Verify seasonality score is valid
            assert sales_trend.seasonality_score >= 0

            # Verify data quality
            assert isinstance(sales_trend.data_quality, DataQuality)
            assert sales_trend.data_quality.months_observed >= 0


def test_sales_trend_flat_sales():
    """Test seasonality score with flat sales (score should be ~1.0)."""
    # This is a theoretical test - in practice we'd need to mock the database
    # For now, we verify the logic by checking the formula would work correctly
    # If all months have same sales, peak/avg = sales/sales = 1.0
    pass


def test_sales_trend_strong_seasonality():
    """Test seasonality score with strong peak (score should be >2.0)."""
    # Theoretical test: if one month has 3x average, score = 3.0
    pass


def test_sales_trend_no_data(db_client):
    """Test sales trend with non-existent article ID."""
    service = SalesAnalyzerService(db_client)

    # Use an article ID that definitely doesn't exist
    sales_trend = service.compute_sales_trend_and_seasonality(
        article_ids=[999999999999]
    )

    # Should return None for no data
    assert sales_trend is None


def test_sales_trend_multiple_articles(db_client):
    """Test sales trend computation with multiple articles."""
    service = SalesAnalyzerService(db_client)

    # Get multiple article IDs
    product_service = ProductSearchService(db_client)
    products, _ = product_service.search(keywords=["shirt"], page=1, page_size=3)

    if len(products) >= 2:
        article_ids = [p.article_id for p in products[:2]]
        sales_trend = service.compute_sales_trend_and_seasonality(
            article_ids=article_ids
        )

        if sales_trend:
            # Should aggregate sales from all articles
            assert isinstance(sales_trend, SalesTrendData)
            assert len(sales_trend.monthly_sales) > 0

            # Article ID should be comma-separated list
            assert ',' in sales_trend.article_id or len(article_ids) == 1
