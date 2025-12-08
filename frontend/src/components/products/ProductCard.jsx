import React from 'react';
import { Package } from 'lucide-react';

export default function ProductCard({ product }) {
  const {
    article_id,
    name: prod_name,
    department: department_name,
    type: product_type_name,
    color: colour_group_name,
    price_range,
    image_url,
  } = product;

  return (
    <div className="bg-white rounded-lg shadow-sm hover:shadow-md transition-all duration-200
                    hover:scale-[1.02] overflow-hidden cursor-pointer">
      {/* Image */}
      <div className="aspect-[4/3] bg-gray-100 relative">
        {image_url && (
          <img
            src={image_url}
            alt={prod_name}
            className="w-full h-full object-cover"
            onError={(e) => {
              console.error('Image failed to load:', image_url);
              console.error('Error event:', e);

              // Hide the image if it fails
              e.currentTarget.style.display = "none";

              // Show the fallback
              const fallback = e.currentTarget.parentNode.querySelector(".fallback");
              if (fallback) fallback.classList.remove("hidden");
            }}
          />
        )}

        {/* Fallback icon (initially visible ONLY if no image_url) */}
        <div
          className={`fallback absolute inset-0 flex items-center justify-center ${
            image_url ? "hidden" : ""
          }`}
        >
          <Package className="w-12 h-12 text-gray-400" />
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <h3 className="font-semibold text-gray-900 line-clamp-2 mb-2">
          {prod_name}
        </h3>

        <div className="flex flex-wrap gap-2 text-sm text-gray-600">
          <span className="px-2 py-1 bg-blue-50 text-blue-700 rounded-md">
            {product_type_name}
          </span>
          {colour_group_name && (
            <span className="px-2 py-1 bg-gray-50 text-gray-700 rounded-md">
              {colour_group_name}
            </span>
          )}
        </div>

        <p className="mt-2 text-xs text-gray-500">
          {department_name} • ID: {article_id}
        </p>
      </div>
    </div>
  );
}
