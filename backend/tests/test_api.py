"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns application info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "status" in data
    assert data["status"] == "running"


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "services" in data
    assert "duckdb" in data["services"]
    assert "ollama" in data["services"]


def test_search_endpoint_basic():
    """Test basic search functionality."""
    payload = {
        "query": "shoes",
        "limit": 10,
        "include_sales": False,
        "include_forecast": False,
        "include_segments": False
    }

    response = client.post("/api/search", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "query" in data
    assert "products" in data
    assert "metadata" in data
    assert data["query"] == "shoes"


def test_search_endpoint_validation():
    """Test search endpoint input validation."""
    # Test empty query
    payload = {"query": "", "limit": 10}
    response = client.post("/api/search", json=payload)
    assert response.status_code == 422  # Validation error

    # Test invalid limit
    payload = {"query": "test", "limit": 0}
    response = client.post("/api/search", json=payload)
    assert response.status_code == 422

    # Test limit too high
    payload = {"query": "test", "limit": 1000}
    response = client.post("/api/search", json=payload)
    assert response.status_code == 422


def test_search_with_all_options():
    """Test search with all optional features enabled."""
    payload = {
        "query": "Nike",
        "limit": 5,
        "include_sales": True,
        "include_forecast": True,
        "include_segments": True
    }

    response = client.post("/api/search", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "products" in data
    assert "metadata" in data
    assert "processing_time_ms" in data["metadata"]
    assert "llm_calls" in data["metadata"]


def test_product_not_found():
    """Test get product with non-existent ID."""
    response = client.get("/api/products/999999999")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data or "detail" in data
