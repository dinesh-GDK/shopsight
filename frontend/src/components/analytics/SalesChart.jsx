import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { formatCurrency, formatChartDate } from '../../utils/formatters';

export default function SalesChart({ data, title = "Sales History" }) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
        <p className="text-gray-500 text-center py-8">No sales data available</p>
      </div>
    );
  }

  // Format data for chart
  const chartData = data.map(d => ({
    date: formatChartDate(d.date || d.month),
    revenue: d.revenue || d.total_revenue,
    transactions: d.transactions || d.transaction_count
  }));

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white border border-gray-200 rounded-lg p-3 shadow-lg">
          <p className="font-semibold text-gray-900">{payload[0].payload.date}</p>
          <p className="text-sm text-blue-600">
            Revenue: {formatCurrency(payload[0].value)}
          </p>
          {payload[0].payload.transactions && (
            <p className="text-sm text-gray-600">
              Transactions: {payload[0].payload.transactions.toLocaleString()}
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="date"
            tick={{ fill: '#6b7280', fontSize: 12 }}
          />
          <YAxis
            tick={{ fill: '#6b7280', fontSize: 12 }}
            tickFormatter={formatCurrency}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Line
            type="monotone"
            dataKey="revenue"
            stroke="#2563eb"
            strokeWidth={2}
            dot={{ fill: '#2563eb', r: 4 }}
            activeDot={{ r: 6 }}
            name="Revenue"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
