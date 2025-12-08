import React from 'react';
import { TrendingUp, Activity, Minus } from 'lucide-react';

export default function SeasonalityScoreBadge({ salesTrend }) {
  if (!salesTrend || salesTrend.seasonality_score === undefined) {
    return null;
  }

  const { seasonality_score, peak_months } = salesTrend;

  // Determine seasonality level
  let level, color, bgColor, icon, description;

  if (seasonality_score >= 2.0) {
    level = 'Strong Seasonality';
    color = 'text-red-700';
    bgColor = 'bg-red-50 border-red-200';
    icon = <TrendingUp className="w-5 h-5 text-red-600" />;
    description = 'Sales show strong seasonal patterns with significant peaks';
  } else if (seasonality_score >= 1.5) {
    level = 'Moderate Seasonality';
    color = 'text-orange-700';
    bgColor = 'bg-orange-50 border-orange-200';
    icon = <Activity className="w-5 h-5 text-orange-600" />;
    description = 'Sales show moderate seasonal variation';
  } else {
    level = 'Low Seasonality';
    color = 'text-green-700';
    bgColor = 'bg-green-50 border-green-200';
    icon = <Minus className="w-5 h-5 text-green-600" />;
    description = 'Sales are relatively stable throughout the year';
  }

  return (
    <div className={`${bgColor} border rounded-lg p-6`}>
      <div className="flex items-start space-x-3">
        <div className="flex-shrink-0 mt-1">
          {icon}
        </div>
        <div className="flex-1">
          <div className="flex items-center justify-between mb-2">
            <h4 className={`text-sm font-semibold ${color}`}>
              {level}
            </h4>
            <span className={`text-2xl font-bold ${color}`}>
              {seasonality_score}
            </span>
          </div>
          <p className="text-sm text-gray-600 mb-3">
            {description}
          </p>
          {peak_months && peak_months.length > 0 && (
            <div className="flex items-center space-x-2">
              <span className="text-xs font-medium text-gray-700">Peak Month{peak_months.length > 1 ? 's' : ''}:</span>
              {peak_months.map((month, index) => (
                <span
                  key={index}
                  className={`px-2 py-1 ${color} ${bgColor.replace('50', '100')} text-xs font-medium rounded`}
                >
                  {month}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Seasonality Score Explanation */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-500">
          <strong>Seasonality Score:</strong> {seasonality_score} (Ratio of peak to average monthly sales)
        </p>
        <div className="mt-2 text-xs text-gray-500">
          <div className="flex items-center space-x-4">
            <span>1.0 = Flat</span>
            <span>1.5-2.0 = Moderate</span>
            <span>2.0+ = Strong</span>
          </div>
        </div>
      </div>
    </div>
  );
}
