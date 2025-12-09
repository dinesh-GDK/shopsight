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

ENHANCED_QUERY_PARSER_PROMPT = """
Parse this e-commerce search query into structured JSON with detailed attribute extraction.

Query: "{query}"

Extract the following:
1. Keywords: All important search terms
2. Attributes: Structured product attributes
   - brand: Brand name if mentioned (e.g., "Nike", "Adidas", "H&M")
   - type: Product type/category (e.g., "jacket", "shoes", "dress", "shirt")
   - color: Color if mentioned (e.g., "black", "blue", "red")
   - style: Style descriptor if mentioned (e.g., "running", "casual", "formal")
   - gender: Target gender if mentioned (e.g., "women", "men", "kids")
   - department: Department if mentioned (e.g., "sport", "casual")
3. Filters: Price or other constraints
4. Intent: User's intent

Return JSON format:
{{
    "keywords": ["keyword1", "keyword2", "..."],
    "attributes": {{
        "brand": "brand_name or null",
        "type": "product_type or null",
        "color": "color or null",
        "style": "style or null",
        "gender": "gender or null",
        "department": "department or null"
    }},
    "filters": {{"key": "value"}},
    "intent": "product_search"
}}

Examples:

Query: "Nike black jacket"
Output: {{
    "keywords": ["Nike", "black", "jacket"],
    "attributes": {{
        "brand": "Nike",
        "type": "jacket",
        "color": "black",
        "style": null,
        "gender": null,
        "department": null
    }},
    "filters": {{}},
    "intent": "product_search"
}}

Query: "Women's running shoes"
Output: {{
    "keywords": ["women", "running", "shoes"],
    "attributes": {{
        "brand": null,
        "type": "shoes",
        "color": null,
        "style": "running",
        "gender": "women",
        "department": "sport"
    }},
    "filters": {{}},
    "intent": "product_search"
}}

Query: "Adidas blue hoodie for men"
Output: {{
    "keywords": ["Adidas", "blue", "hoodie", "men"],
    "attributes": {{
        "brand": "Adidas",
        "type": "hoodie",
        "color": "blue",
        "style": null,
        "gender": "men",
        "department": null
    }},
    "filters": {{}},
    "intent": "product_search"
}}

Query: "Red dresses under $50"
Output: {{
    "keywords": ["red", "dresses"],
    "attributes": {{
        "brand": null,
        "type": "dress",
        "color": "red",
        "style": null,
        "gender": null,
        "department": null
    }},
    "filters": {{"price_max": 50}},
    "intent": "product_search"
}}

Now parse: "{query}"

IMPORTANT: Return ONLY valid JSON, no additional text or explanation.
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
