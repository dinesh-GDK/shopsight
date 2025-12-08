#!/bin/bash

echo "================================"
echo "ShopSight Frontend Setup Verification"
echo "================================"
echo ""

# Check Node.js version
echo "Checking Node.js version..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js installed: $NODE_VERSION"
else
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

# Check npm version
echo ""
echo "Checking npm version..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "✅ npm installed: $NPM_VERSION"
else
    echo "❌ npm not found"
    exit 1
fi

# Check if node_modules exists
echo ""
echo "Checking dependencies..."
if [ -d "node_modules" ]; then
    echo "✅ Dependencies installed (node_modules found)"
else
    echo "⚠️  Dependencies not installed"
    echo "   Run: npm install"
fi

# Check if .env exists
echo ""
echo "Checking environment configuration..."
if [ -f ".env" ]; then
    echo "✅ Environment file exists (.env)"
    cat .env
else
    echo "⚠️  No .env file found (optional)"
    echo "   Default API URL: http://localhost:8000"
fi

# Count components
echo ""
echo "Verifying component files..."
COMPONENT_COUNT=$(find src/components -name "*.jsx" 2>/dev/null | wc -l)
echo "✅ Found $COMPONENT_COUNT component files"

# List key files
echo ""
echo "Key files verification:"
FILES=(
    "package.json"
    "vite.config.js"
    "tailwind.config.js"
    "src/App.jsx"
    "src/main.jsx"
    "index.html"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (missing)"
    fi
done

echo ""
echo "================================"
echo "Setup Verification Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Install dependencies (if not done):"
echo "   npm install"
echo ""
echo "2. Start development server:"
echo "   npm run dev"
echo ""
echo "3. Open browser to:"
echo "   http://localhost:5173"
echo ""
