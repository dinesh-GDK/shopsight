"""LLM Agent orchestrator for query understanding and insight generation."""

import traceback
import ollama
import json
import pandas as pd
from typing import Dict, Any, List
from app.agents.prompts import QUERY_PARSER_PROMPT, INSIGHT_GENERATOR_PROMPT
from app.models.responses import Product, SalesData, Insights
from app.config import settings
from app.utils.logger import logger
from app.utils.exceptions import LLMServiceException


class AgentOrchestrator:
    """LLM agent for query parsing and insight generation."""

    def __init__(
        self,
        model: str = None,
        host: str = None
    ):
        """
        Initialize agent orchestrator.

        Args:
            model: LLM model name (defaults to settings.OLLAMA_MODEL)
            host: Ollama host URL (defaults to settings.OLLAMA_HOST)
        """
        self.model = model or settings.OLLAMA_MODEL
        self.host = host or settings.OLLAMA_HOST
        self.model_name = self.model

        try:
            self.client = ollama.Client(host=self.host)
            logger.info(f"Agent orchestrator initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize Ollama client: {e}")
            raise LLMServiceException(f"Failed to initialize Ollama client: {e}")

    def is_ollama_available(self) -> bool:
        """
        Check if Ollama is running.

        Returns:
            True if Ollama is available, False otherwise
        """
        try:
            self.client.list()
            return True
        except Exception as e:
            logger.warning(f"Ollama not available: {e}")
            return False

    async def parse_query(self, query: str) -> Dict[str, Any]:
        """
        Parse natural language query into structured search parameters.

        Args:
            query: User's search query (e.g., "Nike running shoes under $50")

        Returns:
            Dict with keywords, filters, and intent
        """
        prompt = QUERY_PARSER_PROMPT.format(query=query)

        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a query parser for e-commerce search. Return only valid JSON."
                    },
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.1}
            )

            # Parse JSON from response
            content = response['message']['content']

            # Extract JSON if wrapped in markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            parsed = json.loads(content)
            logger.info(f"Parsed query '{query}' into: {parsed}")
            return parsed

        except Exception as e:
            logger.warning(f"LLM query parsing failed, using fallback: {e}; {traceback.print_exc()}")
            # Fallback to simple keyword extraction
            keywords = [word for word in query.split() if len(word) > 2]
            return {
                "keywords": keywords,
                "filters": {},
                "intent": "product_search"
            }

    async def generate_insights(
        self,
        products: List[Product],
        sales_data: SalesData
    ) -> Insights:
        """
        Generate AI insights from sales data.

        Args:
            products: List of products
            sales_data: Sales history data

        Returns:
            Insights object with text and key findings
        """
        try:
            # Prepare context
            product_names = [p.name for p in products[:5]]  # Limit to top 5
            total_revenue = sales_data.summary.total_revenue
            total_txns = sales_data.summary.total_transactions

            # Find peak month
            if sales_data.timeline:
                timeline_df = pd.DataFrame([
                    {'date': dp.date, 'revenue': dp.revenue}
                    for dp in sales_data.timeline
                ])
                peak_month = timeline_df.loc[timeline_df['revenue'].idxmax(), 'date']
                peak_revenue = timeline_df['revenue'].max()
            else:
                peak_month = "N/A"
                peak_revenue = 0.0

            context = {
                "products": product_names,
                "total_revenue": f"${total_revenue:,.2f}",
                "total_transactions": total_txns,
                "date_range": sales_data.summary.date_range,
                "peak_month": peak_month,
                "peak_revenue": f"${peak_revenue:,.2f}"
            }

            prompt = INSIGHT_GENERATOR_PROMPT.format(context=json.dumps(context, indent=2))

            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a business analyst generating insights from e-commerce data."
                    },
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.3}
            )

            insight_text = response['message']['content']

            # Extract key findings (simple heuristic)
            key_findings = [
                f"Total revenue: ${total_revenue:,.2f}",
                f"Peak sales in {peak_month}",
                f"{total_txns:,} total transactions"
            ]

            logger.info("Generated AI insights successfully")

            return Insights(
                text=insight_text,
                key_findings=key_findings
            )

        except Exception as e:
            logger.warning(f"LLM insight generation failed, using fallback: {e}")
            # Fallback insights
            total_revenue = sales_data.summary.total_revenue
            total_txns = sales_data.summary.total_transactions

            if total_txns > 0:
                avg_txn_value = total_revenue / total_txns
            else:
                avg_txn_value = 0.0

            return Insights(
                text=f"Products generated ${total_revenue:,.2f} in revenue across {total_txns:,} transactions.",
                key_findings=[
                    f"Total revenue: ${total_revenue:,.2f}",
                    f"Total transactions: {total_txns:,}",
                    f"Average transaction value: ${avg_txn_value:.2f}"
                ]
            )
