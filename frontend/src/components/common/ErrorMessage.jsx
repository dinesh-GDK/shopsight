import React from 'react';
import { AlertCircle } from 'lucide-react';

export default function ErrorMessage({ message, onRetry }) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-6">
      <div className="flex items-center space-x-3">
        <AlertCircle className="w-6 h-6 text-red-600 flex-shrink-0" />
        <div className="flex-1">
          <h3 className="text-sm font-semibold text-red-900">Error</h3>
          <p className="text-sm text-red-700 mt-1">{message}</p>
        </div>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
        >
          Try Again
        </button>
      )}
    </div>
  );
}
