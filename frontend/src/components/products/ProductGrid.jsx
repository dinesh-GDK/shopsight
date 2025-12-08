import React from 'react';
import ProductCard from './ProductCard';

export default function ProductGrid({ products, loading, pagination }) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {[...Array(8)].map((_, i) => (
          <div key={i} className="bg-gray-100 rounded-lg animate-pulse">
            <div className="aspect-[4/3] bg-gray-200"></div>
            <div className="p-4 space-y-3">
              <div className="h-4 bg-gray-200 rounded w-3/4"></div>
              <div className="h-3 bg-gray-200 rounded w-1/2"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (!products || products.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No products found</p>
      </div>
    );
  }

  // Calculate range for "Showing X-Y of Z products"
  const getProductRange = () => {
    if (!pagination) {
      return `Products (${products.length})`;
    }

    const { current_page, page_size, total_items } = pagination;
    const start = (current_page - 1) * page_size + 1;
    const end = Math.min(current_page * page_size, total_items);

    return `Showing ${start}-${end} of ${total_items.toLocaleString()} products`;
  };

  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-900 mb-4">
        {getProductRange()}
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {products.map((product) => (
          <ProductCard key={product.article_id} product={product} />
        ))}
      </div>
    </div>
  );
}
