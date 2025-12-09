"""
Confidence Scorer Service

Calculates relevance confidence scores for search results based on
how well product attributes match the parsed query.
"""

import re
from typing import Dict, List, Optional
from app.models.entities import Article


class ConfidenceScorer:
    """
    Calculate confidence scores for search results.

    Scores are weighted combinations of:
    - Brand match (35%)
    - Type match (30%)
    - Color match (20%)
    - Name match (15%)
    """

    # Scoring weights
    BRAND_WEIGHT = 0.35
    TYPE_WEIGHT = 0.30
    COLOR_WEIGHT = 0.20
    NAME_WEIGHT = 0.15

    @staticmethod
    def _contains_word(text: str, word: str) -> bool:
        """
        Check if a word exists in text using word boundary matching.

        This prevents false matches like "Nike" in "Jannike".

        Args:
            text: The text to search in
            word: The word to search for

        Returns:
            True if word is found as a complete word in text
        """
        if not text or not word:
            return False

        # Use word boundary regex for exact word matching
        # \b ensures we match whole words only
        pattern = r'\b' + re.escape(word.lower()) + r'\b'
        return bool(re.search(pattern, text.lower()))

    @staticmethod
    def _fuzzy_contains(text: str, word: str) -> bool:
        """
        Check if word is contained in text with some flexibility.

        Allows partial matches within compound words (e.g., "running" in "runningshoes")
        but requires at least word start or end boundaries.

        Args:
            text: The text to search in
            word: The word to search for

        Returns:
            True if word is found with boundary matching
        """
        if not text or not word:
            return False

        text_lower = text.lower()
        word_lower = word.lower()

        # First try exact word boundary match
        if ConfidenceScorer._contains_word(text, word):
            return True

        # Then try word start/end boundaries for compound words
        # e.g., "running" matches "running-shoes" or "runningshoes"
        pattern = r'(^|\s|-)' + re.escape(word_lower) + r'($|\s|-)'
        return bool(re.search(pattern, text_lower))

    @staticmethod
    def _exact_match(text: str, word: str) -> bool:
        """
        Check for exact match (case-insensitive).

        Args:
            text: The text to compare
            word: The word to compare against

        Returns:
            True if exact match
        """
        if not text or not word:
            return False
        return text.lower().strip() == word.lower().strip()

    def score_product(
        self,
        product: Dict,
        parsed_query: Dict
    ) -> float:
        """
        Calculate confidence score for a product.

        Args:
            product: Product dictionary with fields from database
            parsed_query: Parsed query with keywords and attributes

        Returns:
            Confidence score between 0.0 and 1.0
        """
        attributes = parsed_query.get("attributes", {})
        keywords = parsed_query.get("keywords", [])

        brand_score = self._score_brand(product, attributes.get("brand"))
        type_score = self._score_type(product, attributes.get("type"))
        color_score = self._score_color(product, attributes.get("color"))
        name_score = self._score_name(product, keywords)

        # Calculate weighted average
        confidence = (
            brand_score * self.BRAND_WEIGHT +
            type_score * self.TYPE_WEIGHT +
            color_score * self.COLOR_WEIGHT +
            name_score * self.NAME_WEIGHT
        )

        # Ensure bounds [0.0, 1.0]
        confidence = max(0.0, min(1.0, confidence))

        return round(confidence, 3)

    def _score_brand(self, product: Dict, expected_brand: Optional[str]) -> float:
        """
        Score how well product brand matches expected brand.

        Args:
            product: Product dictionary
            expected_brand: Expected brand from query (e.g., "Nike")

        Returns:
            Score between 0.0 and 1.0
        """
        if not expected_brand:
            return 0.5  # Neutral if no brand specified

        # Check product name first (highest priority) - use word boundary matching
        prod_name = product.get("name", "")
        if self._contains_word(prod_name, expected_brand):
            return 1.0  # Exact word match in product name

        # Check index_name (brand/collection field)
        index_name = product.get("index_name", "")
        if self._contains_word(index_name, expected_brand):
            return 0.9

        # Check department name
        department = product.get("department", "")
        if self._contains_word(department, expected_brand):
            return 0.6

        return 0.0  # No match

    def _score_type(self, product: Dict, expected_type: Optional[str]) -> float:
        """
        Score how well product type matches expected type.

        Args:
            product: Product dictionary
            expected_type: Expected type from query (e.g., "jacket", "shoes")

        Returns:
            Score between 0.0 and 1.0
        """
        if not expected_type:
            return 0.5  # Neutral if no type specified

        # Check product type name (most specific) - exact or fuzzy match
        product_type = product.get("type", "")
        if self._exact_match(product_type, expected_type):
            return 1.0  # Exact type match
        if self._fuzzy_contains(product_type, expected_type):
            return 0.95  # Fuzzy match in type field

        # Check product name - use word boundary
        prod_name = product.get("name", "")
        if self._contains_word(prod_name, expected_type):
            return 0.9

        # Check product group name (broader category)
        product_group = product.get("product_group_name", "")
        if self._fuzzy_contains(product_group, expected_type):
            return 0.7

        # Check garment group (even broader)
        garment_group = product.get("garment_group_name", "")
        if self._fuzzy_contains(garment_group, expected_type):
            return 0.5

        return 0.0  # No match

    def _score_color(self, product: Dict, expected_color: Optional[str]) -> float:
        """
        Score how well product color matches expected color.

        Args:
            product: Product dictionary
            expected_color: Expected color from query (e.g., "black", "blue")

        Returns:
            Score between 0.0 and 1.0
        """
        if not expected_color:
            return 0.5  # Neutral if no color specified

        # Check color group name (primary color field) - exact or fuzzy match
        color = product.get("color", "")
        if self._exact_match(color, expected_color):
            return 1.0  # Exact color match
        if self._fuzzy_contains(color, expected_color):
            return 0.95  # Fuzzy match in color field

        # Check perceived color master name
        perceived_color_master = product.get("perceived_colour_master_name", "")
        if self._fuzzy_contains(perceived_color_master, expected_color):
            return 0.9

        # Check perceived color value name
        perceived_color_value = product.get("perceived_colour_value_name", "")
        if self._fuzzy_contains(perceived_color_value, expected_color):
            return 0.8

        # Check product name (color might be in name) - use word boundary
        prod_name = product.get("name", "")
        if self._contains_word(prod_name, expected_color):
            return 0.7

        return 0.0  # No match

    def _score_name(self, product: Dict, keywords: List[str]) -> float:
        """
        Score based on keyword matches in product name (bonus scoring).

        Args:
            product: Product dictionary
            keywords: List of all keywords from query

        Returns:
            Score between 0.0 and 1.0
        """
        if not keywords:
            return 0.5

        prod_name = product.get("name", "")
        product_type = product.get("type", "")

        matched_in_name = 0
        matched_in_type = 0

        for keyword in keywords:
            # Use word boundary matching for keywords too
            if self._contains_word(prod_name, keyword):
                matched_in_name += 1
            if self._contains_word(product_type, keyword):
                matched_in_type += 1

        # Calculate match ratio
        total_keywords = len(keywords)
        name_ratio = matched_in_name / total_keywords
        type_ratio = matched_in_type / total_keywords

        # Weighted combination
        score = (name_ratio * 0.7) + (type_ratio * 0.3)

        return min(1.0, score)

    def score_products_batch(
        self,
        products: List[Dict],
        parsed_query: Dict
    ) -> List[Dict]:
        """
        Score multiple products and add confidence_score field.

        Args:
            products: List of product dictionaries
            parsed_query: Parsed query with keywords and attributes

        Returns:
            List of products with confidence_score added
        """
        scored_products = []

        for product in products:
            confidence = self.score_product(product, parsed_query)
            product_with_score = {**product, "confidence_score": confidence}
            scored_products.append(product_with_score)

        return scored_products
