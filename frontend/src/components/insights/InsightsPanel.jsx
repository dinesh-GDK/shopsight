import React from 'react';
import { Sparkles, Lightbulb } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function InsightsPanel({ insights, loading }) {
  if (loading) {
    return (
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg shadow-sm p-6">
        <div className="animate-pulse space-y-3">
          <div className="h-4 bg-purple-200 rounded w-3/4"></div>
          <div className="h-4 bg-purple-200 rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  if (!insights) {
    return null;
  }

  return (
    <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg shadow-sm p-6">
      <div className="flex items-center space-x-2 mb-4">
        <Sparkles className="w-5 h-5 text-purple-600" />
        <h3 className="text-lg font-semibold text-gray-900">AI Insights</h3>
      </div>

      <div className="text-gray-700 mb-4 leading-relaxed prose prose-sm max-w-none">
        <ReactMarkdown>{insights.text}</ReactMarkdown>
      </div>

      {insights.key_findings && insights.key_findings.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm font-semibold text-gray-700 flex items-center space-x-2">
            <Lightbulb className="w-4 h-4" />
            <span>Key Findings:</span>
          </p>
          <ul className="space-y-2">
            {insights.key_findings.map((finding, index) => (
              <li key={index} className="flex items-start space-x-2 text-sm text-gray-700">
                <span className="text-purple-600 font-bold">•</span>
                <div className="prose prose-sm max-w-none">
                  <ReactMarkdown>{finding}</ReactMarkdown>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
