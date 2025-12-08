import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

export default function Pagination({ pagination, onPageChange }) {
  const { current_page, total_pages, has_next, has_prev } = pagination;

  if (total_pages <= 1) {
    return null; // Don't show pagination if there's only one page
  }

  // Generate page numbers to display
  const getPageNumbers = () => {
    const pages = [];
    const maxVisible = 5; // Maximum number of page buttons to show

    if (total_pages <= maxVisible) {
      // Show all pages if total is less than max
      for (let i = 1; i <= total_pages; i++) {
        pages.push(i);
      }
    } else {
      // Always show first page
      pages.push(1);

      // Calculate range around current page
      let start = Math.max(2, current_page - 1);
      let end = Math.min(total_pages - 1, current_page + 1);

      // Adjust range if near the beginning or end
      if (current_page <= 3) {
        end = 4;
      } else if (current_page >= total_pages - 2) {
        start = total_pages - 3;
      }

      // Add ellipsis if there's a gap
      if (start > 2) {
        pages.push('...');
      }

      // Add middle pages
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }

      // Add ellipsis if there's a gap
      if (end < total_pages - 1) {
        pages.push('...');
      }

      // Always show last page
      pages.push(total_pages);
    }

    return pages;
  };

  const pageNumbers = getPageNumbers();

  return (
    <div className="flex items-center justify-center space-x-2 mt-8">
      {/* Previous Button */}
      <button
        onClick={() => onPageChange(current_page - 1)}
        disabled={!has_prev}
        className={`
          flex items-center px-3 py-2 rounded-md text-sm font-medium
          transition-colors
          ${has_prev
            ? 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
            : 'bg-gray-100 text-gray-400 cursor-not-allowed border border-gray-200'
          }
        `}
        aria-label="Previous page"
      >
        <ChevronLeft className="w-4 h-4 mr-1" />
        Previous
      </button>

      {/* Page Numbers */}
      <div className="flex items-center space-x-1">
        {pageNumbers.map((page, index) => {
          if (page === '...') {
            return (
              <span
                key={`ellipsis-${index}`}
                className="px-3 py-2 text-gray-500"
              >
                ...
              </span>
            );
          }

          const isActive = page === current_page;

          return (
            <button
              key={page}
              onClick={() => onPageChange(page)}
              className={`
                px-4 py-2 rounded-md text-sm font-medium
                transition-colors
                ${isActive
                  ? 'bg-primary-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
                }
              `}
              aria-label={`Page ${page}`}
              aria-current={isActive ? 'page' : undefined}
            >
              {page}
            </button>
          );
        })}
      </div>

      {/* Next Button */}
      <button
        onClick={() => onPageChange(current_page + 1)}
        disabled={!has_next}
        className={`
          flex items-center px-3 py-2 rounded-md text-sm font-medium
          transition-colors
          ${has_next
            ? 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
            : 'bg-gray-100 text-gray-400 cursor-not-allowed border border-gray-200'
          }
        `}
        aria-label="Next page"
      >
        Next
        <ChevronRight className="w-4 h-4 ml-1" />
      </button>
    </div>
  );
}
