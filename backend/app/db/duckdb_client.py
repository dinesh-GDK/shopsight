"""DuckDB client for querying parquet files."""

import duckdb
import pandas as pd
from typing import List, Any, Optional
from app.config import settings
from app.utils.logger import logger
from app.utils.exceptions import DatabaseException


class DuckDBClient:
    """DuckDB client for analytical queries on parquet files."""

    def __init__(self):
        """Initialize DuckDB connection."""
        try:
            # In-memory database
            self.conn = duckdb.connect(':memory:')

            # Configure performance
            self.conn.execute(f"SET threads TO {settings.DUCKDB_THREADS}")
            self.conn.execute(f"SET memory_limit = '{settings.DUCKDB_MEMORY_LIMIT}'")

            self.config = settings
            logger.info("DuckDB client initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize DuckDB client: {e}")
            raise DatabaseException(f"Database initialization failed: {e}")

    def is_connected(self) -> bool:
        """
        Check if connection is alive.

        Returns:
            True if connected, False otherwise
        """
        try:
            self.conn.execute("SELECT 1")
            return True
        except Exception:
            return False

    def execute(self, query: str, params: Optional[List[Any]] = None) -> List[tuple]:
        """
        Execute SQL query and return results as list of tuples.

        Args:
            query: SQL query string (use ? for parameters)
            params: Query parameters

        Returns:
            List of result tuples

        Raises:
            DatabaseException: If query execution fails
        """
        try:
            if params:
                result = self.conn.execute(query, params)
            else:
                result = self.conn.execute(query)

            return result.fetchall()

        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise DatabaseException(f"Query execution failed: {e}")

    def query_to_df(self, query: str, params: Optional[List[Any]] = None) -> pd.DataFrame:
        """
        Execute SQL query and return results as pandas DataFrame.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            DataFrame with query results

        Raises:
            DatabaseException: If query execution fails
        """
        try:
            if params:
                result = self.conn.execute(query, params)
            else:
                result = self.conn.execute(query)

            return result.df()

        except Exception as e:
            logger.error(f"Query to DataFrame failed: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise DatabaseException(f"Query to DataFrame failed: {e}")

    def close(self):
        """Close database connection."""
        try:
            self.conn.close()
            logger.info("DuckDB connection closed")
        except Exception as e:
            logger.error(f"Failed to close DuckDB connection: {e}")
