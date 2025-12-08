# ShopSight Frontend

AI-Powered E-commerce Analytics Platform - Frontend Application

## Technology Stack

- **React 18.2** - UI framework
- **Vite 5.0** - Build tool and dev server
- **TailwindCSS 3.4** - Utility-first CSS framework
- **Recharts 2.10** - Chart library for data visualization
- **Axios 1.6** - HTTP client for API calls
- **Lucide React** - Icon library

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── assets/          # Images and other assets
│   ├── components/      # React components
│   │   ├── analytics/   # Chart and metrics components
│   │   ├── common/      # Reusable components
│   │   ├── insights/    # AI insights components
│   │   ├── layout/      # Layout components
│   │   ├── products/    # Product display components
│   │   └── search/      # Search components
│   ├── hooks/           # Custom React hooks
│   ├── services/        # API services
│   ├── styles/          # CSS files
│   ├── utils/           # Utility functions
│   ├── App.jsx          # Main application component
│   └── main.jsx         # Application entry point
├── index.html           # HTML template
├── package.json         # Dependencies
├── vite.config.js       # Vite configuration
└── tailwind.config.js   # Tailwind configuration
```

## Setup Instructions

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file (optional):
```bash
cp .env.example .env
```

4. Update `.env` with your backend API URL:
```
VITE_API_URL=http://localhost:8000
```

### Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Build

Create a production build:
```bash
npm run build
```

The build output will be in the `dist` directory.

### Preview Production Build

Preview the production build locally:
```bash
npm run preview
```

### Linting

Run ESLint:
```bash
npm run lint
```

## Features

### Core Features (Real Implementation)
- Natural language product search
- Product catalog display with images
- Historical sales visualization with interactive charts
- AI-generated insights from sales data
- Responsive design for desktop and mobile

### Mocked Features
- Demand forecasting (linear extrapolation)
- Customer segmentation (rule-based)

These features are clearly labeled in the UI with badges and disclaimers.

## Component Overview

### Layout Components
- **Header** - Application header with branding
- **Footer** - Application footer with credits
- **Layout** - Main layout wrapper

### Search Components
- **SearchBar** - Natural language search input with examples

### Product Components
- **ProductCard** - Individual product display card
- **ProductGrid** - Responsive grid layout for products

### Analytics Components
- **SalesChart** - Line chart for sales history
- **MetricsCard** - KPI metric display cards
- **ForecastWidget** - Forecast visualization (mocked)

### Insights Components
- **InsightsPanel** - AI-generated insights display
- **CustomerSegments** - Customer segment visualization

### Common Components
- **LoadingSpinner** - Loading state indicator
- **ErrorMessage** - Error display with retry option
- **Badge** - Reusable badge component

## API Integration

The frontend communicates with the backend API through the `services/api.js` module:

- `searchProducts()` - Search for products and get analytics
- `getProduct()` - Get individual product details
- `checkHealth()` - Check API health status

## Styling

The application uses TailwindCSS for styling with a custom configuration:

- Primary color: Blue (#2563eb)
- Accent color: Purple (#8b5cf6)
- Font: Inter (Google Fonts)

Custom styles are defined in `src/styles/index.css`

## Performance Optimization

- Lazy loading for images
- Debounced search input
- Optimized chart rendering
- Skeleton loading states
- Error boundaries

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development Guidelines

1. **Component Structure**: Follow the existing component structure
2. **Styling**: Use Tailwind utility classes, avoid inline styles
3. **State Management**: Use React hooks (useState, useEffect)
4. **API Calls**: Use the centralized API service
5. **Error Handling**: Always handle errors gracefully
6. **Loading States**: Show loading indicators for async operations

## Troubleshooting

### Port Already in Use
If port 5173 is already in use, you can change it in `vite.config.js`:
```javascript
server: {
  port: 3000, // Change to your preferred port
}
```

### API Connection Issues
Ensure the backend API is running on `http://localhost:8000` or update the `VITE_API_URL` in your `.env` file.

### Build Errors
Clear the cache and reinstall dependencies:
```bash
rm -rf node_modules dist
npm install
npm run build
```

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please refer to the main project README or contact the development team.
