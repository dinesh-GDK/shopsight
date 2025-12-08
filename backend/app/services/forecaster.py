"""Forecaster service (MOCKED implementation)."""

from typing import List
import pandas as pd
from app.models.responses import Forecast, ForecastPoint, SalesData
from app.utils.logger import logger


class ForecasterService:
    """
    Mocked demand forecasting service.
    Uses simple linear extrapolation from last 3 months.
    """

    def predict(
        self,
        sales_data: SalesData,
        periods: int = 3
    ) -> Forecast:
        """
        Generate forecast for next N periods.

        Args:
            sales_data: Historical sales data
            periods: Number of future periods to predict

        Returns:
            Forecast with predictions and confidence note
        """
        try:
            # Convert to DataFrame
            df = pd.DataFrame([
                {
                    'date': pd.to_datetime(dp.date),
                    'revenue': dp.revenue
                }
                for dp in sales_data.timeline
            ])

            if len(df) < 3:
                # Not enough data for forecast
                logger.warning("Insufficient data for forecasting (< 3 data points)")
                return Forecast(
                    predictions=[],
                    note="Insufficient historical data for forecasting (mocked)"
                )

            # Simple linear extrapolation from last 3 points
            last_3 = df.tail(3)
            avg_growth = (last_3['revenue'].iloc[-1] - last_3['revenue'].iloc[0]) / 2

            predictions = []
            last_date = df['date'].max()
            last_revenue = df['revenue'].iloc[-1]

            for i in range(1, periods + 1):
                future_date = last_date + pd.DateOffset(months=i)
                predicted_revenue = max(0, last_revenue + (avg_growth * i))

                predictions.append(ForecastPoint(
                    date=future_date.strftime('%Y-%m'),
                    predicted_revenue=round(predicted_revenue, 2),
                    confidence="low"
                ))

            logger.info(f"Generated {len(predictions)} forecast periods (mocked)")

            return Forecast(
                predictions=predictions,
                note="Forecast based on linear extrapolation from last 3 months (mocked data)"
            )

        except Exception as e:
            logger.error(f"Forecasting failed: {e}")
            # Return empty forecast on error
            return Forecast(
                predictions=[],
                note=f"Forecasting failed: {str(e)} (mocked)"
            )
