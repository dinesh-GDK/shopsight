import React, { useState } from 'react';
import { Search, X, Loader2 } from 'lucide-react';
import { EXAMPLE_QUERIES } from '../../utils/constants';

export default function SearchBar({ onSearch, loading, placeholder = "Search products..." }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  const handleClear = () => {
    setQuery('');
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-gray-400" />
        </div>

        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          disabled={loading}
          autoFocus
          className="block w-full pl-12 pr-20 py-4 text-lg border-2 border-gray-300 rounded-lg
                     focus:ring-2 focus:ring-primary-500 focus:border-primary-500
                     disabled:bg-gray-100 disabled:cursor-not-allowed
                     transition-colors"
        />

        <div className="absolute inset-y-0 right-0 flex items-center pr-2 space-x-2">
          {query && !loading && (
            <button
              type="button"
              onClick={handleClear}
              className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          )}

          <button
            type="submit"
            disabled={!query.trim() || loading}
            className="px-4 py-2 bg-primary-600 text-white rounded-md
                       hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed
                       transition-colors flex items-center space-x-2"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Searching...</span>
              </>
            ) : (
              <span>Search</span>
            )}
          </button>
        </div>
      </div>

      {/* Example queries */}
      <div className="mt-3 flex flex-wrap gap-2 justify-center">
        <span className="text-sm text-gray-500">Try:</span>
        {EXAMPLE_QUERIES.map((example) => (
          <button
            key={example}
            type="button"
            onClick={() => setQuery(example)}
            className="text-sm px-3 py-1 bg-gray-100 text-gray-700 rounded-full
                       hover:bg-gray-200 transition-colors"
          >
            {example}
          </button>
        ))}
      </div>
    </form>
  );
}
