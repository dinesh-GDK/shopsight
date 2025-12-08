import React from 'react';
import { Users } from 'lucide-react';

export default function CustomerSegments({ segments }) {
  if (!segments || segments.length === 0) {
    return null;
  }

  const colors = [
    'bg-blue-500',
    'bg-purple-500',
    'bg-green-500',
    'bg-orange-500'
  ];

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex items-center space-x-2 mb-4">
        <Users className="w-5 h-5 text-gray-700" />
        <h3 className="text-lg font-semibold text-gray-900">Customer Segments</h3>
      </div>

      <div className="space-y-4">
        {segments.map((segment, index) => (
          <div key={index}>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">
                {segment.segment}
              </span>
              <span className="text-sm text-gray-600">
                {segment.percentage}% • Avg age: {segment.avg_age}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`${colors[index % colors.length]} h-2 rounded-full transition-all duration-500`}
                style={{ width: `${segment.percentage}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>

      <p className="mt-4 text-xs text-gray-500 italic">
        Segments based on customer demographics (mocked data)
      </p>
    </div>
  );
}
