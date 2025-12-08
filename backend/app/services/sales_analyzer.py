"""Sales analyzer service (REAL implementation)."""

from typing import List, Optional, Dict, Any
from datetime import date
import pandas as pd
from app.db.duckdb_client import DuckDBClient
from app.models.responses import SalesData, SalesDataPoint, SalesSummary
from app.models.requests import DateRange
from app.utils.logger import logger


class SalesAnalyzerService:
    """Service for analyzing sales data."""

    def __init__(self, db: DuckDBClient):
        """
        Initialize sales analyzer service.

        Args:
            db: DuckDB client instance
        """
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
        params = [self.db.config.TRANSACTIONS_PATH]

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

        try:
            # Execute and convert to DataFrame
            df = self.db.query_to_df(query, params)

            if df.empty:
                logger.warning(f"No sales data found for articles: {article_ids}")
                return SalesData(
                    timeline=[],
                    summary=SalesSummary(
                        total_revenue=0.0,
                        total_transactions=0,
                        date_range={"start": "", "end": ""}
                    )
                )

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

            logger.info(
                f"Retrieved sales data for {len(article_ids)} articles: "
                f"{summary.total_transactions} transactions, "
                f"${summary.total_revenue:.2f} revenue"
            )

            return SalesData(timeline=timeline, summary=summary)

        except Exception as e:
            logger.error(f"Failed to get sales history: {e}")
            raise

    def get_summary(self, article_id: int) -> Optional[Dict[str, Any]]:
        """
        Get sales summary for a single product.

        Args:
            article_id: Product article ID

        Returns:
            Dictionary with sales summary or None if no data
        """
        query = """
        SELECT
            COUNT(*) as total_transactions,
            SUM(price) as total_revenue,
            MIN(t_dat) as first_sale,
            MAX(t_dat) as last_sale
        FROM read_parquet(?)
        WHERE article_id = ?
        """

        try:
            result = self.db.execute(
                query,
                [self.db.config.TRANSACTIONS_PATH, article_id]
            )

            if not result or result[0][0] == 0:
                logger.warning(f"No sales data found for article: {article_id}")
                return None

            row = result[0]
            return {
                "total_transactions": row[0],
                "total_revenue": float(row[1]),
                "first_sale": row[2].strftime('%Y-%m-%d') if row[2] else None,
                "last_sale": row[3].strftime('%Y-%m-%d') if row[3] else None
            }

        except Exception as e:
            logger.error(f"Failed to get sales summary for {article_id}: {e}")
            raise
