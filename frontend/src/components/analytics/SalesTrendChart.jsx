import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function SalesTrendChart({ salesTrend, title = "Sales Trend (Monthly Units)" }) {
  if (!salesTrend || !salesTrend.monthly_sales || salesTrend.monthly_sales.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
        <p className="text-gray-500 text-center py-8">No sales trend data available</p>
      </div>
    );
  }

  const { monthly_sales, data_quality } = salesTrend;

  // Format data for chart
  const chartData = monthly_sales.map(point => ({
    month: point.month,
    sales: point.sales
  }));

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white border border-gray-200 rounded-lg p-3 shadow-lg">
          <p className="font-semibold text-gray-900">{payload[0].payload.month}</p>
          <p className="text-sm text-purple-600">
            Units Sold: {payload[0].value.toLocaleString()}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        {data_quality && data_quality.sparse_data && (
          <span className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs font-medium rounded">
            Limited Data
          </span>
        )}
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="month"
            tick={{ fill: '#6b7280', fontSize: 12 }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis
            tick={{ fill: '#6b7280', fontSize: 12 }}
            label={{ value: 'Units Sold', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar
            dataKey="sales"
            fill="#8b5cf6"
            radius={[4, 4, 0, 0]}
            name="Units Sold"
          />
        </BarChart>
      </ResponsiveContainer>

      {data_quality && (
        <div className="mt-4 text-xs text-gray-500">
          Data based on {data_quality.months_observed} month{data_quality.months_observed !== 1 ? 's' : ''} of sales history
        </div>
      )}
    </div>
  );
}
