"""Dependency injection for FastAPI."""

from functools import lru_cache
from app.db.duckdb_client import DuckDBClient
from app.agents.orchestrator import AgentOrchestrator
from app.utils.logger import logger


@lru_cache()
def get_db_client() -> DuckDBClient:
    """
    Get singleton DuckDB client instance.

    Returns:
        DuckDB client instance
    """
    logger.info("Initializing DuckDB client")
    return DuckDBClient()


@lru_cache()
def get_agent_orchestrator() -> AgentOrchestrator:
    """
    Get singleton LLM agent orchestrator instance.

    Returns:
        Agent orchestrator instance
    """
    logger.info("Initializing Agent Orchestrator")
    return AgentOrchestrator()
