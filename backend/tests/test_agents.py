"""Unit tests for LLM agents."""

import pytest
from app.agents.orchestrator import AgentOrchestrator
from app.models.responses import SalesData, SalesDataPoint, SalesSummary, Product


@pytest.fixture
def agent():
    """Create agent orchestrator for testing."""
    return AgentOrchestrator()


def test_agent_initialization(agent):
    """Test agent orchestrator initializes correctly."""
    assert agent.model is not None
    assert agent.host is not None


@pytest.mark.asyncio
async def test_parse_query_fallback(agent):
    """Test query parsing with fallback mechanism."""
    # This test should work even if Ollama is not available
    query = "Nike running shoes"
    result = await agent.parse_query(query)

    assert isinstance(result, dict)
    assert "keywords" in result
    assert "filters" in result
    assert "intent" in result
    assert isinstance(result["keywords"], list)


@pytest.mark.asyncio
async def test_generate_insights_fallback(agent):
    """Test insight generation with fallback mechanism."""
    # Create mock data
    products = [
        Product(
            article_id=123,
            name="Test Product",
            type="Shirt",
            color="Blue",
            department="Men"
        )
    ]

    sales_data = SalesData(
        timeline=[
            SalesDataPoint(date="2020-01-01", revenue=1000, transactions=50, avg_price=20),
            SalesDataPoint(date="2020-02-01", revenue=1200, transactions=60, avg_price=20),
        ],
        summary=SalesSummary(
            total_revenue=2200,
            total_transactions=110,
            date_range={"start": "2020-01-01", "end": "2020-02-01"}
        )
    )

    insights = await agent.generate_insights(products, sales_data)

    assert hasattr(insights, 'text')
    assert hasattr(insights, 'key_findings')
    assert isinstance(insights.text, str)
    assert isinstance(insights.key_findings, list)
    assert len(insights.key_findings) > 0


@pytest.mark.skipif(
    not AgentOrchestrator().is_ollama_available(),
    reason="Ollama not available"
)
@pytest.mark.asyncio
async def test_parse_query_with_ollama(agent):
    """Test query parsing with Ollama (only if available)."""
    query = "Show me black Nike shoes"
    result = await agent.parse_query(query)

    assert isinstance(result, dict)
    assert "keywords" in result
    assert len(result["keywords"]) > 0
    # Should contain at least "Nike" or "shoes"
    keywords_lower = [k.lower() for k in result["keywords"]]
    assert any(word in keywords_lower for word in ["nike", "shoes", "black"])
