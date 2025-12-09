"""Product search service (REAL implementation)."""

from typing import List, Dict, Optional, Tuple
from app.db.duckdb_client import DuckDBClient
from app.models.responses import Product
from app.services.confidence_scorer import ConfidenceScorer
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

    def search_with_confidence(
        self,
        keywords: List[str],
        parsed_query: Dict,
        filters: Optional[Dict] = None,
        page: int = 1,
        page_size: int = 20,
        min_confidence: float = 0.0
    ) -> Tuple[List[Product], int]:
        """
        Search products with confidence scoring and filtering.

        Args:
            keywords: List of search terms
            parsed_query: Full parsed query with attributes (from LLM)
            filters: Additional filters
            page: Page number (1-indexed)
            page_size: Number of results per page
            min_confidence: Minimum confidence threshold (0.0-1.0)

        Returns:
            Tuple of (scored and filtered products, total count after filtering)
        """
        if filters is None:
            filters = {}

        # Build WHERE clause (broader search for candidates)
        where_sql, params = self._build_where_clause(keywords, filters)

        # Get more candidates than requested (to have enough after filtering)
        # Limit to max 500 candidates for performance
        candidate_limit = min(500, page_size * 25)

        query = f"""
        SELECT
            article_id,
            prod_name as name,
            product_type_name as type,
            colour_group_name as color,
            department_name as department,
            product_group_name,
            garment_group_name,
            index_name,
            perceived_colour_master_name,
            perceived_colour_value_name,
            image_url
        FROM read_parquet(?)
        WHERE {where_sql}
        LIMIT ?
        """

        try:
            logger.info(f"Searching with confidence scoring. Min confidence: {min_confidence}")
            logger.info(f"Parsed query attributes: {parsed_query.get('attributes', {})}")

            # Execute query to get candidates
            result = self.db.execute(
                query,
                [self.db.config.ARTICLES_PATH] + params + [candidate_limit]
            )

            logger.info(f"Got {len(result)} candidate products")

            # Convert to dictionaries for scoring
            candidates = [
                {
                    "article_id": row[0],
                    "name": row[1],
                    "type": row[2],
                    "color": row[3],
                    "department": row[4],
                    "product_group_name": row[5],
                    "garment_group_name": row[6],
                    "index_name": row[7],
                    "perceived_colour_master_name": row[8],
                    "perceived_colour_value_name": row[9],
                    "image_url": row[10]
                }
                for row in result
            ]

            # Score all candidates
            scorer = ConfidenceScorer()
            scored_products = scorer.score_products_batch(candidates, parsed_query)

            # Filter by minimum confidence
            filtered_products = [
                p for p in scored_products
                if p["confidence_score"] >= min_confidence
            ]

            # Sort by confidence score (descending)
            filtered_products.sort(key=lambda p: p["confidence_score"], reverse=True)

            logger.info(f"After confidence filtering (>= {min_confidence}): {len(filtered_products)} products")

            # Apply pagination
            total_count = len(filtered_products)
            start = (page - 1) * page_size
            end = start + page_size
            paginated_products = filtered_products[start:end]

            # Convert to Product objects
            products = [
                Product(
                    article_id=p["article_id"],
                    name=p["name"],
                    type=p["type"],
                    color=p["color"],
                    department=p["department"],
                    price_range=None,
                    image_url=p["image_url"],
                    confidence_score=p["confidence_score"]
                )
                for p in paginated_products
            ]

            logger.info(f"Returning page {page}: {len(products)} products, total: {total_count}")

            # Log top 5 confidence scores for debugging
            if products:
                top_scores = [(p.name, p.confidence_score) for p in products[:5]]
                logger.info(f"Top 5 confidence scores: {top_scores}")

            return products, total_count

        except Exception as e:
            logger.error(f"Product search with confidence failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise

    def get_all_article_ids(
        self,
        keywords: List[str],
        filters: Optional[Dict] = None
    ) -> List[int]:
        """
        Get ALL article IDs matching search criteria (no pagination).
        Used for analytics calculations that should span all matching products.

        Args:
            keywords: List of search terms
            filters: Additional filters

        Returns:
            List of all matching article IDs
        """
        if filters is None:
            filters = {}

        # Build WHERE clause
        where_sql, params = self._build_where_clause(keywords, filters)

        query = f"""
        SELECT article_id
        FROM read_parquet(?)
        WHERE {where_sql}
        """

        try:
            result = self.db.execute(
                query,
                [self.db.config.ARTICLES_PATH] + params
            )

            article_ids = [row[0] for row in result]
            logger.info(f"Found {len(article_ids)} total article IDs for analytics")
            return article_ids

        except Exception as e:
            logger.error(f"Failed to get all article IDs: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise

    def get_all_article_ids_with_confidence(
        self,
        keywords: List[str],
        parsed_query: Dict,
        filters: Optional[Dict] = None,
        min_confidence: float = 0.0
    ) -> List[int]:
        """
        Get ALL article IDs matching search criteria with confidence filtering.
        Used for analytics calculations on confidence-filtered results.

        Args:
            keywords: List of search terms
            parsed_query: Full parsed query with attributes
            filters: Additional filters
            min_confidence: Minimum confidence threshold

        Returns:
            List of all matching article IDs that pass confidence threshold
        """
        if filters is None:
            filters = {}

        # If no confidence filtering, use faster method
        if min_confidence == 0.0:
            return self.get_all_article_ids(keywords, filters)

        # Build WHERE clause
        where_sql, params = self._build_where_clause(keywords, filters)

        # Get ALL candidates (limit to reasonable number for performance)
        # For analytics, we'll cap at 1000 products
        candidate_limit = 1000

        query = f"""
        SELECT
            article_id,
            prod_name as name,
            product_type_name as type,
            colour_group_name as color,
            department_name as department,
            product_group_name,
            garment_group_name,
            index_name,
            perceived_colour_master_name,
            perceived_colour_value_name
        FROM read_parquet(?)
        WHERE {where_sql}
        LIMIT ?
        """

        try:
            logger.info(f"Getting all article IDs with confidence >= {min_confidence}")

            # Execute query to get candidates
            result = self.db.execute(
                query,
                [self.db.config.ARTICLES_PATH] + params + [candidate_limit]
            )

            # Convert to dictionaries for scoring
            candidates = [
                {
                    "article_id": row[0],
                    "name": row[1],
                    "type": row[2],
                    "color": row[3],
                    "department": row[4],
                    "product_group_name": row[5],
                    "garment_group_name": row[6],
                    "index_name": row[7],
                    "perceived_colour_master_name": row[8],
                    "perceived_colour_value_name": row[9]
                }
                for row in result
            ]

            # Score and filter
            scorer = ConfidenceScorer()
            scored_products = scorer.score_products_batch(candidates, parsed_query)

            # Filter by confidence and extract IDs
            article_ids = [
                p["article_id"] for p in scored_products
                if p["confidence_score"] >= min_confidence
            ]

            logger.info(f"Found {len(article_ids)} article IDs for analytics after confidence filtering")
            return article_ids

        except Exception as e:
            logger.error(f"Failed to get article IDs with confidence: {e}")
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
