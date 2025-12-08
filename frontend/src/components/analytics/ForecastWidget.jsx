import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { AlertCircle } from 'lucide-react';
import { formatCurrency } from '../../utils/formatters';

export default function ForecastWidget({ forecast }) {
  if (!forecast || !forecast.predictions || forecast.predictions.length === 0) {
    return null;
  }

  const chartData = forecast.predictions.map(f => ({
    date: f.date,
    revenue: f.predicted_revenue
  }));

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 border-2 border-orange-200">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Demand Forecast</h3>
        <span className="px-3 py-1 bg-orange-100 text-orange-700 text-xs font-semibold rounded-full">
          FORECASTED
        </span>
      </div>

      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={chartData}>
          <XAxis dataKey="date" tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} tickFormatter={formatCurrency} />
          <Tooltip
            formatter={(value) => formatCurrency(value)}
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px'
            }}
          />
          <Line
            type="monotone"
            dataKey="revenue"
            stroke="#f97316"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ fill: '#f97316' }}
          />
        </LineChart>
      </ResponsiveContainer>

      {forecast.note && (
        <div className="mt-4 flex items-start space-x-2 text-sm text-gray-600 bg-orange-50 p-3 rounded-md">
          <AlertCircle className="w-4 h-4 text-orange-600 mt-0.5 flex-shrink-0" />
          <p>{forecast.note}</p>
        </div>
      )}
    </div>
  );
}
