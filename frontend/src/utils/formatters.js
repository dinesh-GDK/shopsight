/**
 * Format number as currency (USD)
 */
export function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
}

/**
 * Format number with commas
 */
export function formatNumber(value) {
  return new Intl.NumberFormat('en-US').format(value);
}

/**
 * Format date to readable string
 */
export function formatDate(dateString, options = {}) {
  const defaultOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    ...options,
  };
  return new Date(dateString).toLocaleDateString('en-US', defaultOptions);
}

/**
 * Format date for chart display (short format)
 */
export function formatChartDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    year: '2-digit',
  });
}

/**
 * Truncate text to specified length
 */
export function truncate(text, maxLength = 100) {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength).trim() + '...';
}
