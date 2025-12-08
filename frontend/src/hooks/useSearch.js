import { useState, useCallback } from 'react';
import { searchProducts } from '../services/api';

/**
 * Custom hook for managing search state and API calls
 */
export function useSearch() {
  const [state, setState] = useState({
    query: '',
    loading: false,
    error: null,
    results: null,
  });

  const search = useCallback(async (query, options = {}) => {
    setState(prev => ({
      ...prev,
      query,
      loading: true,
      error: null,
    }));

    try {
      const results = await searchProducts({
        query,
        limit: 20,
        include_sales: true,
        include_forecast: true,
        include_segments: true,
        ...options,
      });

      setState({
        query,
        loading: false,
        error: null,
        results,
      });

      return results;
    } catch (error) {
      const errorMessage = error.message || 'Failed to search products';
      setState({
        query,
        loading: false,
        error: errorMessage,
        results: null,
      });

      throw error;
    }
  }, []);

  const reset = useCallback(() => {
    setState({
      query: '',
      loading: false,
      error: null,
      results: null,
    });
  }, []);

  return {
    ...state,
    search,
    reset,
  };
}
