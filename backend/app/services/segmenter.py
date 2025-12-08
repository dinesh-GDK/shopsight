"""Customer segmentation service (MOCKED implementation)."""

from typing import List
from app.db.duckdb_client import DuckDBClient
from app.models.responses import CustomerSegment
from app.utils.logger import logger


class SegmenterService:
    """
    Mocked customer segmentation service.
    Uses rule-based segmentation on customer demographics.
    """

    def __init__(self, db: DuckDBClient):
        """
        Initialize segmenter service.

        Args:
            db: DuckDB client instance
        """
        self.db = db

    def get_segments(self, article_ids: List[int]) -> List[CustomerSegment]:
        """
        Get customer segments for products.

        Args:
            article_ids: List of product IDs

        Returns:
            List of customer segments with demographics
        """
        try:
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
                self.db.config.TRANSACTIONS_PATH,
                self.db.config.CUSTOMERS_PATH
            ] + article_ids

            df = self.db.query_to_df(query, params)

            if df.empty:
                # Return default segments if no data
                logger.warning(f"No customer data found for articles: {article_ids}, using defaults")
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

            logger.info(f"Generated {len(segments)} customer segments (mocked)")
            return segments

        except Exception as e:
            logger.error(f"Customer segmentation failed: {e}")
            return self._default_segments()

    def _default_segments(self) -> List[CustomerSegment]:
        """
        Return default segments when no data available.

        Returns:
            List of default customer segments
        """
        return [
            CustomerSegment(segment="Young Professionals", percentage=35, avg_age=28),
            CustomerSegment(segment="Fitness Enthusiasts", percentage=42, avg_age=32),
            CustomerSegment(segment="Casual Shoppers", percentage=23, avg_age=41)
        ]
