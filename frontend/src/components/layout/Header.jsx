import React from 'react';
import { BarChart3 } from 'lucide-react';

export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <BarChart3 className="w-8 h-8 text-primary-600" />
            <div>
              <h1 className="text-2xl font-bold text-primary-700">
                ShopSight
              </h1>
              <p className="text-xs text-gray-500">
                AI-Powered E-commerce Analytics
              </p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
