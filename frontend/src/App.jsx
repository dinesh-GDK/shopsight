import React, { useState } from 'react';
import Layout from './components/layout/Layout';
import SearchBar from './components/search/SearchBar';
import ConfidenceSlider from './components/search/ConfidenceSlider';
import ProductGrid from './components/products/ProductGrid';
import SalesChart from './components/analytics/SalesChart';
import SalesTrendChart from './components/analytics/SalesTrendChart';
import SeasonalityScoreBadge from './components/analytics/SeasonalityScoreBadge';
import MetricsCard from './components/analytics/MetricsCard';
import InsightsPanel from './components/insights/InsightsPanel';
import ForecastWidget from './components/analytics/ForecastWidget';
import CustomerSegments from './components/insights/CustomerSegments';
import ErrorMessage from './components/common/ErrorMessage';
import Pagination from './components/common/Pagination';
import { searchProducts } from './services/api';
import { DollarSign, ShoppingCart, TrendingUp } from 'lucide-react';
import { formatCurrency } from './utils/formatters';

export default function App() {
  const [searchState, setSearchState] = useState({
    query: '',
    currentPage: 1,
    pageSize: 20,
    minConfidence: 0.5, // Default to 50% minimum confidence
    loading: false,
    loadingProducts: false,
    error: null,
    results: null
  });

  const handleSearch = async (query, page = 1, isPagination = false) => {
    setSearchState(prev => ({
      ...prev,
      query,
      currentPage: page,
      loading: !isPagination, // Only show full loading for new searches
      loadingProducts: true, // Always show product loading
      error: null
    }));

    try {
      const results = await searchProducts({
        query,
        page,
        page_size: searchState.pageSize,
        min_confidence: searchState.minConfidence, // NEW: Include confidence threshold
        include_sales: true,
        include_sales_trend: true,
        include_forecast: true,
        include_segments: true
      });

      setSearchState(prev => ({
        ...prev,
        query,
        currentPage: page,
        loading: false,
        loadingProducts: false,
        error: null,
        results
      }));
    } catch (error) {
      setSearchState(prev => ({
        ...prev,
        query,
        currentPage: page,
        loading: false,
        loadingProducts: false,
        error: error.message || 'Failed to search products',
        results: null
      }));
    }
  };

  const handlePageChange = (newPage) => {
    // Scroll to top of product grid
    window.scrollTo({ top: 0, behavior: 'smooth' });
    handleSearch(searchState.query, newPage, true); // Pass true to indicate pagination
  };

  const handleConfidenceChange = (newConfidence) => {
    setSearchState(prev => ({
      ...prev,
      minConfidence: newConfidence,
      currentPage: 1 // Reset to page 1 when filter changes
    }));

    // Don't automatically search - wait for user to click Search button
  };

  const { loading, loadingProducts, error, results, minConfidence } = searchState;

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Section */}
        <div className="mb-8">
          <SearchBar
            onSearch={handleSearch}
            loading={loading}
            placeholder="Search products using natural language..."
          />
        </div>

        {/* Confidence Filter - Always visible */}
        <div className="max-w-2xl mx-auto mb-8">
          <ConfidenceSlider
            value={minConfidence}
            onChange={handleConfidenceChange}
            disabled={loading || loadingProducts}
          />
        </div>

        {/* Error State */}
        {error && (
          <ErrorMessage
            message={error}
            onRetry={() => handleSearch(searchState.query)}
          />
        )}

        {/* Results Dashboard */}
        {results && (
          <div className="space-y-8">
            {/* Metrics */}
            {results.sales_data && results.sales_data.summary && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <MetricsCard
                  title="Total Revenue"
                  value={formatCurrency(results.sales_data.summary.total_revenue)}
                  icon={<DollarSign className="w-6 h-6" />}
                  color="green"
                />
                <MetricsCard
                  title="Total Transactions"
                  value={results.sales_data.summary.total_transactions.toLocaleString()}
                  icon={<ShoppingCart className="w-6 h-6" />}
                  color="blue"
                />
                <MetricsCard
                  title="Products Found"
                  value={results.pagination ? results.pagination.total_items.toLocaleString() : results.products.length}
                  icon={<TrendingUp className="w-6 h-6" />}
                  color="purple"
                />
              </div>
            )}

            {/* Products */}
            <ProductGrid
              products={results.products}
              pagination={results.pagination}
              loading={loadingProducts}
            />

            {/* Pagination */}
            {results.pagination && !loadingProducts && (
              <Pagination
                pagination={results.pagination}
                onPageChange={handlePageChange}
              />
            )}

            {/* Sales Chart */}
            {results.sales_data && results.sales_data.timeline && (
              <SalesChart data={results.sales_data.timeline} />
            )}

            {/* Sales Trend Analysis */}
            {results.sales_trend && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2">
                  <SalesTrendChart salesTrend={results.sales_trend} />
                </div>
                <div>
                  <SeasonalityScoreBadge salesTrend={results.sales_trend} />
                </div>
              </div>
            )}

            {/* Insights */}
            {results.insights && (
              <InsightsPanel insights={results.insights} />
            )}

            {/* Secondary Analytics */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {results.forecast && (
                <ForecastWidget forecast={results.forecast} />
              )}
              {results.customer_segments && (
                <CustomerSegments segments={results.customer_segments} />
              )}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && !results && !error && (
          <div className="text-center py-16">
            <h2 className="text-2xl font-semibold text-gray-900 mb-3">
              Start Exploring
            </h2>
            <p className="text-gray-600">
              Search for any product to see sales analytics and AI-powered insights
            </p>
          </div>
        )}
      </div>
    </Layout>
  );
}
