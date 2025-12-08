"""Product search service (REAL implementation)."""

from typing import List, Dict, Optional, Tuple
from app.db.duckdb_client import DuckDBClient
from app.models.responses import Product
from app.utils.logger import logger
from app.utils.exceptions import ProductNotFoundException


class ProductSearchService:
    """Service for searching and retrieving products."""

    def __init__(self, db: DuckDBClient):
        """
        Initialize product search service.

        Args:
            db: DuckDB client instance
        """
        self.db = db

    def _build_where_clause(
        self,
        keywords: List[str],
        filters: Optional[Dict] = None
    ) -> Tuple[str, List]:
        """
        Build WHERE clause and parameters for search query.

        Args:
            keywords: List of search terms
            filters: Additional filters

        Returns:
            Tuple of (where_sql, params)
        """
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

        # Add filter clauses
        if filters.get('department'):
            where_clauses.append("LOWER(department_name) = ?")
            params.append(filters['department'].lower())

        if filters.get('color'):
            where_clauses.append("LOWER(colour_group_name) = ?")
            params.append(filters['color'].lower())

        if filters.get('type'):
            where_clauses.append("LOWER(product_type_name) = ?")
            params.append(filters['type'].lower())

        # Separate keyword clauses from filter clauses
        keyword_clauses = []
        filter_clauses = []

        for i, keyword in enumerate(keywords):
            keyword_clauses.append(where_clauses[i])

        for i in range(len(keywords), len(where_clauses)):
            filter_clauses.append(where_clauses[i])

        # Build final WHERE clause
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
        """
        Get total count of products matching search criteria.

        Args:
            keywords: List of search terms
            filters: Additional filters

        Returns:
            Total count of matching products
        """
        where_sql, params = self._build_where_clause(keywords, filters)

        query = f"""
        SELECT COUNT(*)
        FROM read_parquet(?)
        WHERE {where_sql}
        """

        try:
            result = self.db.execute(
                query,
                [self.db.config.ARTICLES_PATH] + params
            )
            return result[0][0] if result else 0

        except Exception as e:
            logger.error(f"Product count failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise

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
            filters: Additional filters (e.g., {"department": "Sport", "price_max": 100})
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
        try:
            # Debug logging
            logger.info(f"Executing search with keywords: {keywords}, filters: {filters}")
            logger.info(f"Articles path: {self.db.config.ARTICLES_PATH}")
            logger.info(f"WHERE clause: {where_sql}")
            logger.info(f"Query parameters: {params}")
            logger.info(f"Page: {page}, Page size: {page_size}, Offset: {offset}")

            result = self.db.execute(
                query,
                [self.db.config.ARTICLES_PATH] + params + [page_size, offset]
            )

            logger.info(f"Query returned {len(result)} rows")

            # Convert to Product objects
            products = [
                Product(
                    article_id=row[0],
                    name=row[1],
                    type=row[2],
                    color=row[3],
                    department=row[4],
                    price_range=None,  # Calculate from sales if needed
                    image_url=row[-1]
                )
                for row in result
            ]

            # Get total count
            total_count = self.get_count(keywords, filters)

            logger.info(f"Found {len(products)} products for keywords: {keywords}, total: {total_count}")
            return products, total_count

        except Exception as e:
            logger.error(f"Product search failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise

    def get_by_id(self, article_id: int) -> Optional[Product]:
        """
        Get single product by ID.

        Args:
            article_id: Product article ID

        Returns:
            Product object or None if not found

        Raises:
            ProductNotFoundException: If product not found
        """
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

        try:
            result = self.db.execute(
                query,
                [self.db.config.ARTICLES_PATH, article_id]
            )

            if not result:
                raise ProductNotFoundException(f"Product with ID {article_id} not found")

            row = result[0]
            return Product(
                article_id=row[0],
                name=row[1],
                type=row[2],
                color=row[3],
                department=row[4],
                image_url=row[7]
            )

        except Exception as e:
            logger.error(f"Failed to get product by ID {article_id}: {e}")
            raise
