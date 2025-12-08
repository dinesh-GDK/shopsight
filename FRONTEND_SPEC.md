# ShopSight - Frontend Specification

**Version:** 1.0
**Date:** December 7, 2024
**Target Audience:** Frontend Engineers
**Tech Stack:** React 18, Vite, TailwindCSS, Recharts

---

## Table of Contents
1. [Project Setup](#project-setup)
2. [Application Architecture](#application-architecture)
3. [Component Specifications](#component-specifications)
4. [State Management](#state-management)
5. [API Integration](#api-integration)
6. [UI/UX Guidelines](#uiux-guidelines)
7. [Styling System](#styling-system)
8. [Data Visualization](#data-visualization)
9. [Performance Optimization](#performance-optimization)
10. [Testing Strategy](#testing-strategy)

---

## Project Setup

### Directory Structure

```
frontend/
├── public/
│   ├── favicon.ico
│   └── logo.png
│
├── src/
│   ├── assets/
│   │   └── images/
│   │       └── placeholder.png
│   │
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── Layout.jsx
│   │   │
│   │   ├── search/
│   │   │   ├── SearchBar.jsx
│   │   │   └── SearchSuggestions.jsx
│   │   │
│   │   ├── products/
│   │   │   ├── ProductCard.jsx
│   │   │   ├── ProductGrid.jsx
│   │   │   └── ProductDetails.jsx
│   │   │
│   │   ├── analytics/
│   │   │   ├── SalesChart.jsx
│   │   │   ├── ForecastWidget.jsx
│   │   │   └── MetricsCard.jsx
│   │   │
│   │   ├── insights/
│   │   │   ├── InsightsPanel.jsx
│   │   │   ├── KeyFindingsCard.jsx
│   │   │   └── CustomerSegments.jsx
│   │   │
│   │   └── common/
│   │       ├── LoadingSpinner.jsx
│   │       ├── ErrorMessage.jsx
│   │       └── Badge.jsx
│   │
│   ├── services/
│   │   └── api.js
│   │
│   ├── hooks/
│   │   ├── useSearch.js
│   │   └── useDebounce.js
│   │
│   ├── utils/
│   │   ├── formatters.js
│   │   └── constants.js
│   │
│   ├── styles/
│   │   └── index.css
│   │
│   ├── App.jsx
│   └── main.jsx
│
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

### Dependencies (package.json)

```json
{
  "name": "shopsight-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext js,jsx"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.2",
    "recharts": "^2.10.3",
    "lucide-react": "^0.294.0",
    "clsx": "^2.0.0",
    "react-markdown": "^9.0.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.8",
    "tailwindcss": "^3.4.0",
    "@tailwindcss/typography": "^0.5.10",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "eslint": "^8.55.0",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0"
  }
}
```

### Configuration Files

**vite.config.js**
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

**tailwind.config.js**
```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        accent: {
          500: '#8b5cf6',
          600: '#7c3aed',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
```

---

## Application Architecture

### Component Hierarchy

```
App
├── Layout
│   ├── Header
│   │   └── Logo + Title
│   │
│   ├── Main Content
│   │   ├── SearchBar
│   │   │   └── SearchSuggestions (conditional)
│   │   │
│   │   ├── Dashboard (conditional: when search results exist)
│   │   │   ├── ProductGrid
│   │   │   │   └── ProductCard (multiple)
│   │   │   │
│   │   │   ├── Analytics Section
│   │   │   │   ├── MetricsCard (multiple)
│   │   │   │   └── SalesChart
│   │   │   │
│   │   │   ├── InsightsPanel
│   │   │   │   └── KeyFindingsCard (multiple)
│   │   │   │
│   │   │   └── Secondary Analytics
│   │   │       ├── ForecastWidget
│   │   │       └── CustomerSegments
│   │   │
│   │   └── EmptyState (conditional: when no search)
│   │
│   └── Footer
│       └── Credits + Links
```

### Data Flow

```
User Action (Search)
    ↓
SearchBar Component
    ↓
useSearch Hook
    ↓
API Service (axios)
    ↓
Backend API
    ↓
Response
    ↓
useState Update
    ↓
Re-render Dashboard Components
    ↓
Display Results
```

---

## Component Specifications

### 1. Layout Components

#### Header Component

**File:** `src/components/layout/Header.jsx`

**Purpose:** Top navigation with branding

**Props:** None

**Design Specs:**
- Height: 64px
- Background: White with bottom border (gray-200)
- Logo: Left-aligned
- Title: "ShopSight" in primary-700 color
- Subtitle: "AI-Powered E-commerce Analytics"

**Implementation:**
```jsx
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
```

---

### 2. Search Components

#### SearchBar Component

**File:** `src/components/search/SearchBar.jsx`

**Purpose:** Natural language search input

**Props:**
- `onSearch: (query: string) => void` - Callback when search is submitted
- `loading: boolean` - Loading state
- `placeholder: string` - Input placeholder text

**Design Specs:**
- Width: Full width (max 600px centered)
- Height: 56px
- Border: 2px primary-500 on focus
- Icon: Search icon (left)
- Button: Search button (right) or Enter key
- Loading: Show spinner in button

**Features:**
- Debounced input (500ms)
- Enter key submits
- Clear button when text exists
- Auto-focus on mount

**Implementation:**
```jsx
import React, { useState } from 'react';
import { Search, X, Loader2 } from 'lucide-react';

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
        {['Nike running shoes', 'Women jackets', 'Sports equipment'].map((example) => (
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
```

---

### 3. Product Components

#### ProductCard Component

**File:** `src/components/products/ProductCard.jsx`

**Purpose:** Display individual product with image and metadata

**Props:**
```typescript
{
  product: {
    article_id: number;
    name: string;
    type: string;
    color: string;
    department: string;
    image_url: string;
  }
}
```

**Design Specs:**
- Card: White background, rounded-lg, shadow-sm
- Image: 16:9 aspect ratio, object-cover
- Hover: Shadow-md, slight scale (1.02)
- Transition: All 200ms

**Implementation:**
```jsx
import React from 'react';
import { Package } from 'lucide-react';

export default function ProductCard({ product }) {
  const {
    article_id,
    name,
    type,
    color,
    department,
    image_url
  } = product;

  return (
    <div className="bg-white rounded-lg shadow-sm hover:shadow-md transition-all duration-200
                    hover:scale-[1.02] overflow-hidden cursor-pointer">
      {/* Image */}
      <div className="aspect-[4/3] bg-gray-100 relative">
        {image_url ? (
          <img
            src={image_url}
            alt={name}
            className="w-full h-full object-cover"
            onError={(e) => {
              e.target.style.display = 'none';
              e.target.nextSibling.style.display = 'flex';
            }}
          />
        ) : null}
        {/* Fallback */}
        <div className={`absolute inset-0 flex items-center justify-center ${image_url ? 'hidden' : ''}`}>
          <Package className="w-12 h-12 text-gray-400" />
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <h3 className="font-semibold text-gray-900 line-clamp-2 mb-2">
          {name}
        </h3>

        <div className="flex flex-wrap gap-2 text-sm text-gray-600">
          <span className="px-2 py-1 bg-blue-50 text-blue-700 rounded-md">
            {type}
          </span>
          {color && (
            <span className="px-2 py-1 bg-gray-50 text-gray-700 rounded-md">
              {color}
            </span>
          )}
        </div>

        <p className="mt-2 text-xs text-gray-500">
          {department} • ID: {article_id}
        </p>
      </div>
    </div>
  );
}
```

#### ProductGrid Component

**File:** `src/components/products/ProductGrid.jsx`

**Purpose:** Grid layout for product cards

**Props:**
```typescript
{
  products: Product[];
  loading?: boolean;
}
```

**Design Specs:**
- Grid: 4 columns on desktop, 2 on tablet, 1 on mobile
- Gap: 24px
- Loading: Show skeleton cards

**Implementation:**
```jsx
import React from 'react';
import ProductCard from './ProductCard';

export default function ProductGrid({ products, loading }) {
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

  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-900 mb-4">
        Products ({products.length})
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {products.map((product) => (
          <ProductCard key={product.article_id} product={product} />
        ))}
      </div>
    </div>
  );
}
```

---

### 4. Analytics Components

#### SalesChart Component

**File:** `src/components/analytics/SalesChart.jsx`

**Purpose:** Time-series visualization of sales data

**Props:**
```typescript
{
  data: Array<{
    date: string;
    revenue: number;
    transactions: number;
  }>;
  title?: string;
}
```

**Chart Specs:**
- Type: Line chart (revenue) + Bar chart (transactions, optional)
- X-axis: Dates
- Y-axis: Revenue ($)
- Colors: Primary-600 for line, gray-300 for bars
- Tooltip: Show date, revenue, transaction count
- Responsive: Full width

**Implementation:**
```jsx
import React from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function SalesChart({ data, title = "Sales History" }) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
        <p className="text-gray-500 text-center py-8">No sales data available</p>
      </div>
    );
  }

  // Format data for chart
  const chartData = data.map(d => ({
    date: new Date(d.date).toLocaleDateString('en-US', { month: 'short', year: '2-digit' }),
    revenue: d.revenue,
    transactions: d.transactions
  }));

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0
    }).format(value);
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="date"
            tick={{ fill: '#6b7280', fontSize: 12 }}
          />
          <YAxis
            tick={{ fill: '#6b7280', fontSize: 12 }}
            tickFormatter={formatCurrency}
          />
          <Tooltip
            formatter={(value, name) => {
              if (name === 'revenue') return formatCurrency(value);
              return value.toLocaleString();
            }}
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px'
            }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="revenue"
            stroke="#2563eb"
            strokeWidth={2}
            dot={{ fill: '#2563eb', r: 4 }}
            activeDot={{ r: 6 }}
            name="Revenue"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
```

#### MetricsCard Component

**File:** `src/components/analytics/MetricsCard.jsx`

**Purpose:** Display single KPI metric

**Props:**
```typescript
{
  title: string;
  value: string | number;
  icon?: ReactNode;
  trend?: {
    value: number;
    direction: 'up' | 'down';
  };
  color?: 'blue' | 'green' | 'purple';
}
```

**Implementation:**
```jsx
import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

export default function MetricsCard({ title, value, icon, trend, color = 'blue' }) {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    purple: 'bg-purple-50 text-purple-600'
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm text-gray-600 mb-1">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>

          {trend && (
            <div className={`flex items-center mt-2 text-sm ${
              trend.direction === 'up' ? 'text-green-600' : 'text-red-600'
            }`}>
              {trend.direction === 'up' ? (
                <TrendingUp className="w-4 h-4 mr-1" />
              ) : (
                <TrendingDown className="w-4 h-4 mr-1" />
              )}
              <span>{Math.abs(trend.value)}%</span>
            </div>
          )}
        </div>

        {icon && (
          <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
            {icon}
          </div>
        )}
      </div>
    </div>
  );
}
```

#### ForecastWidget Component

**File:** `src/components/analytics/ForecastWidget.jsx`

**Purpose:** Display forecasted demand (mocked data)

**Props:**
```typescript
{
  forecast: {
    predictions: Array<{
      date: string;
      predicted_revenue: number;
      confidence: string;
    }>;
    note: string;
  }
}
```

**Design Specs:**
- Badge: "FORECASTED" in orange
- Chart: Dashed line for predictions
- Note: Display mock disclaimer

**Implementation:**
```jsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { AlertCircle } from 'lucide-react';

export default function ForecastWidget({ forecast }) {
  if (!forecast || !forecast.predictions || forecast.predictions.length === 0) {
    return null;
  }

  const chartData = forecast.predictions.map(f => ({
    date: f.date,
    revenue: f.predicted_revenue
  }));

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 border-2 border-orange-200">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Demand Forecast</h3>
        <span className="px-3 py-1 bg-orange-100 text-orange-700 text-xs font-semibold rounded-full">
          FORECASTED
        </span>
      </div>

      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={chartData}>
          <XAxis dataKey="date" tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="revenue"
            stroke="#f97316"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ fill: '#f97316' }}
          />
        </LineChart>
      </ResponsiveContainer>

      {forecast.note && (
        <div className="mt-4 flex items-start space-x-2 text-sm text-gray-600 bg-orange-50 p-3 rounded-md">
          <AlertCircle className="w-4 h-4 text-orange-600 mt-0.5 flex-shrink-0" />
          <p>{forecast.note}</p>
        </div>
      )}
    </div>
  );
}
```

#### SalesTrendChart Component

**File:** `src/components/analytics/SalesTrendChart.jsx`

**Purpose:** Display monthly sales trend with unit count visualization

**Props:**
```typescript
{
  salesTrend: {
    monthly_sales: Array<{ month: string, sales: number }>,
    data_quality: { months_observed: number, sparse_data: boolean }
  },
  title?: string
}
```

**Design Specs:**
- Chart: Bar chart showing monthly unit sales
- X-axis: Months (rotated -45° for readability)
- Y-axis: Unit count
- Colors: Purple theme (#8b5cf6)
- Data quality badge for sparse data warnings
- Responsive width

**Implementation:**
```jsx
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { AlertCircle } from 'lucide-react';

export default function SalesTrendChart({ salesTrend, title = "Sales Trend Analysis" }) {
  if (!salesTrend || !salesTrend.monthly_sales || salesTrend.monthly_sales.length === 0) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        {salesTrend.data_quality?.sparse_data && (
          <span className="px-3 py-1 bg-yellow-100 text-yellow-700 text-xs font-semibold rounded-full">
            Limited Data
          </span>
        )}
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={salesTrend.monthly_sales}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="month"
            tick={{ fill: '#6b7280', fontSize: 12 }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis
            tick={{ fill: '#6b7280', fontSize: 12 }}
            label={{ value: 'Units Sold', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px'
            }}
          />
          <Bar dataKey="sales" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
```

#### SeasonalityScoreBadge Component

**File:** `src/components/analytics/SeasonalityScoreBadge.jsx`

**Purpose:** Display seasonality score with color-coded interpretation

**Props:**
```typescript
{
  salesTrend: {
    seasonality_score: number,
    peak_months: Array<string>
  }
}
```

**Design Specs:**
- Color-coded badges:
  - Green (< 1.5): Low seasonality
  - Orange (1.5 - 2.0): Moderate seasonality
  - Red (> 2.0): Strong seasonality
- Icon indicators based on level
- Peak month badges
- Score explanation

**Implementation:**
```jsx
import React from 'react';
import { TrendingUp, Activity, Minus } from 'lucide-react';

export default function SeasonalityScoreBadge({ salesTrend }) {
  if (!salesTrend || salesTrend.seasonality_score === undefined) {
    return null;
  }

  const { seasonality_score, peak_months } = salesTrend;

  const getSeasonalityLevel = (score) => {
    if (score < 1.5) {
      return {
        level: 'Low',
        color: 'bg-green-50 border-green-200 text-green-700',
        icon: <Minus className="w-5 h-5" />
      };
    } else if (score < 2.0) {
      return {
        level: 'Moderate',
        color: 'bg-orange-50 border-orange-200 text-orange-700',
        icon: <Activity className="w-5 h-5" />
      };
    } else {
      return {
        level: 'Strong',
        color: 'bg-red-50 border-red-200 text-red-700',
        icon: <TrendingUp className="w-5 h-5" />
      };
    }
  };

  const { level, color, icon } = getSeasonalityLevel(seasonality_score);

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 h-full">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Seasonality Analysis</h3>

      <div className={`border-2 rounded-lg p-4 mb-4 ${color}`}>
        <div className="flex items-center space-x-2 mb-2">
          {icon}
          <span className="font-semibold text-lg">{level} Seasonality</span>
        </div>
        <div className="text-2xl font-bold">
          {seasonality_score.toFixed(2)}
        </div>
        <p className="text-sm mt-2">
          Peak is {seasonality_score.toFixed(1)}x the average
        </p>
      </div>

      {peak_months && peak_months.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm font-semibold text-gray-700">Peak Months:</p>
          <div className="flex flex-wrap gap-2">
            {peak_months.map((month, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-purple-100 text-purple-700 text-sm rounded-md"
              >
                {month}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="mt-4 pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-500">
          <strong>Reference:</strong> 1.0 = flat sales, 2.0+ = strong seasonal pattern
        </p>
      </div>
    </div>
  );
}
```

---

### 5. Insights Components

#### InsightsPanel Component

**File:** `src/components/insights/InsightsPanel.jsx`

**Purpose:** Display AI-generated insights with markdown rendering support

**Props:**
```typescript
{
  insights: {
    text: string;          // Supports markdown formatting
    key_findings: string[]; // Each finding supports markdown
  };
  loading?: boolean;
}
```

**Design Specs:**
- Icon: Sparkles (AI indicator)
- Background: Purple gradient
- Loading: Shimmer animation
- Markdown rendering: Supports bold, italic, links, code blocks, lists, etc.
- Typography styling: Uses Tailwind's prose classes for beautiful text formatting

**Implementation:**
```jsx
import React from 'react';
import { Sparkles, Lightbulb } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function InsightsPanel({ insights, loading }) {
  if (loading) {
    return (
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg shadow-sm p-6">
        <div className="animate-pulse space-y-3">
          <div className="h-4 bg-purple-200 rounded w-3/4"></div>
          <div className="h-4 bg-purple-200 rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  if (!insights) {
    return null;
  }

  return (
    <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg shadow-sm p-6">
      <div className="flex items-center space-x-2 mb-4">
        <Sparkles className="w-5 h-5 text-purple-600" />
        <h3 className="text-lg font-semibold text-gray-900">AI Insights</h3>
      </div>

      <div className="text-gray-700 mb-4 leading-relaxed prose prose-sm max-w-none">
        <ReactMarkdown>{insights.text}</ReactMarkdown>
      </div>

      {insights.key_findings && insights.key_findings.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm font-semibold text-gray-700 flex items-center space-x-2">
            <Lightbulb className="w-4 h-4" />
            <span>Key Findings:</span>
          </p>
          <ul className="space-y-2">
            {insights.key_findings.map((finding, index) => (
              <li key={index} className="flex items-start space-x-2 text-sm text-gray-700">
                <span className="text-purple-600 font-bold">•</span>
                <div className="prose prose-sm max-w-none">
                  <ReactMarkdown>{finding}</ReactMarkdown>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
```

#### CustomerSegments Component

**File:** `src/components/insights/CustomerSegments.jsx`

**Purpose:** Display customer demographic segments

**Props:**
```typescript
{
  segments: Array<{
    segment: string;
    percentage: number;
    avg_age: number;
  }>;
}
```

**Implementation:**
```jsx
import React from 'react';
import { Users } from 'lucide-react';

export default function CustomerSegments({ segments }) {
  if (!segments || segments.length === 0) {
    return null;
  }

  const colors = [
    'bg-blue-500',
    'bg-purple-500',
    'bg-green-500',
    'bg-orange-500'
  ];

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex items-center space-x-2 mb-4">
        <Users className="w-5 h-5 text-gray-700" />
        <h3 className="text-lg font-semibold text-gray-900">Customer Segments</h3>
      </div>

      <div className="space-y-4">
        {segments.map((segment, index) => (
          <div key={index}>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">
                {segment.segment}
              </span>
              <span className="text-sm text-gray-600">
                {segment.percentage}% • Avg age: {segment.avg_age}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`${colors[index % colors.length]} h-2 rounded-full transition-all duration-500`}
                style={{ width: `${segment.percentage}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>

      <p className="mt-4 text-xs text-gray-500 italic">
        Segments based on customer demographics (mocked data)
      </p>
    </div>
  );
}
```

---

### 6. Common Components

#### LoadingSpinner Component

**File:** `src/components/common/LoadingSpinner.jsx`

```jsx
import React from 'react';
import { Loader2 } from 'lucide-react';

export default function LoadingSpinner({ size = 'md', text }) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  return (
    <div className="flex flex-col items-center justify-center py-12">
      <Loader2 className={`${sizeClasses[size]} text-primary-600 animate-spin`} />
      {text && <p className="mt-3 text-gray-600">{text}</p>}
    </div>
  );
}
```

#### ErrorMessage Component

**File:** `src/components/common/ErrorMessage.jsx`

```jsx
import React from 'react';
import { AlertCircle } from 'lucide-react';

export default function ErrorMessage({ message, onRetry }) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-6">
      <div className="flex items-center space-x-3">
        <AlertCircle className="w-6 h-6 text-red-600 flex-shrink-0" />
        <div className="flex-1">
          <h3 className="text-sm font-semibold text-red-900">Error</h3>
          <p className="text-sm text-red-700 mt-1">{message}</p>
        </div>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
        >
          Try Again
        </button>
      )}
    </div>
  );
}
```

#### Pagination Component

**File:** `src/components/common/Pagination.jsx`

**Purpose:** Navigate through paginated product results

**Props:**
```typescript
{
  pagination: {
    current_page: number;
    page_size: number;
    total_items: number;
    total_pages: number;
    has_next: boolean;
    has_prev: boolean;
  };
  onPageChange: (page: number) => void;
}
```

**Features:**
- Smart page number display (max 5 pages with ellipsis)
- Previous/Next buttons with disabled states
- Accessible navigation with ARIA labels
- Auto-hides when only one page exists

**Implementation:**
```jsx
import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

export default function Pagination({ pagination, onPageChange }) {
  const { current_page, total_pages, has_next, has_prev } = pagination;

  if (total_pages <= 1) {
    return null;
  }

  const getPageNumbers = () => {
    const pages = [];
    const maxVisible = 5;

    if (total_pages <= maxVisible) {
      for (let i = 1; i <= total_pages; i++) {
        pages.push(i);
      }
    } else {
      pages.push(1);

      let start = Math.max(2, current_page - 1);
      let end = Math.min(total_pages - 1, current_page + 1);

      if (current_page <= 3) {
        end = 4;
      } else if (current_page >= total_pages - 2) {
        start = total_pages - 3;
      }

      if (start > 2) {
        pages.push('...');
      }

      for (let i = start; i <= end; i++) {
        pages.push(i);
      }

      if (end < total_pages - 1) {
        pages.push('...');
      }

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
        className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors
          ${has_prev
            ? 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
            : 'bg-gray-100 text-gray-400 cursor-not-allowed border border-gray-200'
          }`}
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
              <span key={`ellipsis-${index}`} className="px-3 py-2 text-gray-500">
                ...
              </span>
            );
          }

          const isActive = page === current_page;

          return (
            <button
              key={page}
              onClick={() => onPageChange(page)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors
                ${isActive
                  ? 'bg-primary-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
                }`}
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
        className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors
          ${has_next
            ? 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
            : 'bg-gray-100 text-gray-400 cursor-not-allowed border border-gray-200'
          }`}
        aria-label="Next page"
      >
        Next
        <ChevronRight className="w-4 h-4 ml-1" />
      </button>
    </div>
  );
}
```

---

## State Management

### App-Level State (App.jsx)

```jsx
import React, { useState } from 'react';
import Layout from './components/layout/Layout';
import SearchBar from './components/search/SearchBar';
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
    loading: false,
    loadingProducts: false,  // Separate loading state for pagination
    error: null,
    results: null
  });

  const handleSearch = async (query, page = 1, isPagination = false) => {
    setSearchState(prev => ({
      ...prev,
      query,
      currentPage: page,
      loading: !isPagination,        // Only show full loading for new searches
      loadingProducts: true,          // Always show product loading
      error: null
    }));

    try {
      const results = await searchProducts({
        query,
        page,
        page_size: searchState.pageSize,
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

  const { loading, loadingProducts, error, results } = searchState;

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Section */}
        <div className="mb-12">
          <SearchBar
            onSearch={handleSearch}
            loading={loading}
            placeholder="Search products using natural language..."
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
```

---

## API Integration

### API Service (src/services/api.js)

```javascript
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
```

---

## UI/UX Guidelines

### Design Principles

1. **Clarity Over Complexity**
   - Prioritize readability and scanability
   - Use clear visual hierarchy
   - Avoid unnecessary ornamentation

2. **Progressive Disclosure**
   - Show most important info first (products, sales)
   - Secondary analytics below the fold
   - Expandable sections for details

3. **Feedback & Responsiveness**
   - Loading states for all async operations
   - Error messages with retry actions
   - Success indicators after actions

4. **Accessibility**
   - Semantic HTML
   - ARIA labels where needed
   - Keyboard navigation support
   - Color contrast ratio ≥ 4.5:1

### Color Palette

```css
/* Primary (Blue) */
--primary-50: #eff6ff;
--primary-600: #2563eb;
--primary-700: #1d4ed8;

/* Accent (Purple) */
--accent-600: #7c3aed;

/* Success (Green) */
--success-600: #16a34a;

/* Warning (Orange) */
--warning-600: #ea580c;

/* Error (Red) */
--error-600: #dc2626;

/* Neutral (Gray) */
--gray-50: #f9fafb;
--gray-600: #4b5563;
--gray-900: #111827;
```

### Typography

```css
/* Headings */
h1: 2rem (32px), font-bold
h2: 1.5rem (24px), font-semibold
h3: 1.25rem (20px), font-semibold

/* Body */
p: 1rem (16px), font-normal
small: 0.875rem (14px), font-normal

/* Font Family */
font-family: 'Inter', system-ui, sans-serif
```

### Spacing

```css
/* Consistent spacing scale (Tailwind) */
1 = 4px
2 = 8px
3 = 12px
4 = 16px
6 = 24px
8 = 32px
12 = 48px
```

---

## Performance Optimization

### Best Practices

1. **Code Splitting**
   - Lazy load routes if app grows
   - Dynamic imports for heavy components

2. **Image Optimization**
   - Lazy load product images
   - Use placeholder while loading
   - Error fallback for broken images

3. **Data Fetching**
   - Debounce search input (500ms)
   - Cache API responses (future: React Query)
   - Cancel pending requests on new search

4. **Rendering Optimization**
   - Memoize expensive calculations
   - Use React.memo for pure components
   - Virtual scrolling for large product lists (future)

### Performance Targets

| Metric | Target |
|--------|--------|
| First Contentful Paint | < 1.5s |
| Time to Interactive | < 3s |
| Search Result Render | < 100ms |
| Chart Render | < 200ms |

---

## Testing Strategy

### Component Tests

```javascript
// Example: SearchBar.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import SearchBar from './SearchBar';

test('calls onSearch when form is submitted', () => {
  const handleSearch = jest.fn();
  render(<SearchBar onSearch={handleSearch} />);

  const input = screen.getByPlaceholderText(/search products/i);
  const button = screen.getByRole('button', { name: /search/i });

  fireEvent.change(input, { target: { value: 'Nike shoes' } });
  fireEvent.click(button);

  expect(handleSearch).toHaveBeenCalledWith('Nike shoes');
});
```

### Integration Tests

- Test full search flow: input → API call → render results
- Test error handling: API failure → error message → retry
- Test loading states: API pending → spinner → results

---

## Deployment

### Build Process

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

### Environment Variables

```bash
# .env
VITE_API_URL=http://localhost:8000
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

RUN npm install -g serve

CMD ["serve", "-s", "dist", "-l", "5173"]
```

---

**End of Frontend Specification**

For questions or clarifications, contact the frontend lead.
