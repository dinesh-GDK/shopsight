import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    const message = error.response?.data?.message || error.message || 'An error occurred';
    console.error('[API Error]', message);
    throw new Error(message);
  }
);

/**
 * Search products with natural language query
 */
export async function searchProducts(params) {
  return api.post('/api/search', params);
}

/**
 * Get product details by ID
 */
export async function getProduct(articleId, includeSales = true) {
  return api.get(`/api/products/${articleId}`, {
    params: { include_sales: includeSales }
  });
}

/**
 * Check API health
 */
export async function checkHealth() {
  return api.get('/health');
}

export default api;
