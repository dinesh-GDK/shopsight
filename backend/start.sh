#!/bin/bash

# ShopSight Backend Startup Script (Conda)

set -e

echo "Starting ShopSight Backend..."

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "Error: conda is not installed or not in PATH"
    echo "Please install Miniconda or Anaconda first:"
    echo "  https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Initialize conda for bash (if not already done)
eval "$(conda shell.bash hook)"

# Check if environment exists
if conda env list | grep -q "^shopsight-backend "; then
    echo "Activating existing 'shopsight' conda environment..."
    conda activate shopsight-backend
else
    echo "Creating 'shopsight' conda environment from environment.yml..."
    conda env create -f environment.yml
    conda activate shopsight-backend
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Please configure .env file with your settings"
fi

# Check if Ollama is running
echo "Checking Ollama connection..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✓ Ollama is running"
else
    echo "✗ Ollama is not running. Please start Ollama:"
    echo "  ollama serve"
    echo ""
    echo "And pull the model:"
    echo "  ollama pull llama3.2"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Start the application
echo ""
echo "Starting FastAPI application..."
echo "API will be available at: http://localhost:8000"
echo "Interactive docs at: http://localhost:8000/docs"
echo ""
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
