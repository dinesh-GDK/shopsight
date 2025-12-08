/**
 * API configuration
 */
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  TIMEOUT: 30000,
};

/**
 * Example search queries
 */
export const EXAMPLE_QUERIES = [
  'Nike running shoes',
  'Women jackets',
  'Sports equipment',
  'Black dresses',
  'Men accessories',
];

/**
 * Chart color palette
 */
export const CHART_COLORS = {
  primary: '#2563eb',
  secondary: '#8b5cf6',
  success: '#16a34a',
  warning: '#ea580c',
  danger: '#dc2626',
  gray: '#6b7280',
};

/**
 * Loading messages
 */
export const LOADING_MESSAGES = {
  SEARCHING: 'Searching products...',
  ANALYZING: 'Analyzing sales data...',
  GENERATING: 'Generating insights...',
};

/**
 * Error messages
 */
export const ERROR_MESSAGES = {
  NETWORK: 'Network error. Please check your connection.',
  SERVER: 'Server error. Please try again later.',
  TIMEOUT: 'Request timed out. Please try again.',
  UNKNOWN: 'An unexpected error occurred.',
};
