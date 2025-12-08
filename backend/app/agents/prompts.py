"""Prompt templates for LLM agent."""

QUERY_PARSER_PROMPT = """
Parse this e-commerce search query into structured JSON.

Query: "{query}"

Extract:
1. Keywords: Main search terms (brand, category, product type)
2. Filters: Specific constraints (price, color, department)
3. Intent: What the user wants (product_search, sales_analysis, comparison)

Return JSON format:
{{
    "keywords": ["keyword1", "keyword2"],
    "filters": {{"key": "value"}},
    "intent": "product_search"
}}

Examples:
Query: "Nike running shoes"
Output: {{"keywords": ["Nike", "running", "shoes"], "filters": {{}}, "intent": "product_search"}}

Query: "Women's jackets under $50"
Output: {{"keywords": ["women", "jackets"], "filters": {{"price_max": 50}}, "intent": "product_search"}}

Query: "Black dresses for sport department"
Output: {{"keywords": ["black", "dresses"], "filters": {{"department": "sport"}}, "intent": "product_search"}}

Now parse: "{query}"
"""

INSIGHT_GENERATOR_PROMPT = """
Analyze this e-commerce sales data and generate 2-3 actionable business insights.

Data:
{context}

Generate insights that:
1. Identify trends and patterns
2. Highlight peak performance periods
3. Provide actionable recommendations

Write in a professional but conversational tone. Focus on "why" not just "what".
Keep insights concise (2-3 sentences total).
"""
