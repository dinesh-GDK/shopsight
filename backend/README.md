# ShopSight Backend

Agentic e-commerce analytics platform with LLM-powered insights.

## Features

- **Natural Language Search**: Search products using conversational queries
- **Real-time Analytics**: Historical sales trends and patterns
- **AI Insights**: LLM-generated actionable business insights
- **Demand Forecasting**: Predict future sales (mocked with linear extrapolation)
- **Customer Segmentation**: Buyer demographics analysis (mocked with rule-based segmentation)

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **Database**: DuckDB 0.9.2 (queries parquet files directly)
- **LLM**: Ollama with Llama 3.2
- **Language**: Python 3.11
- **Data Validation**: Pydantic 2.5

## Quick Start

### Prerequisites

- Conda (Miniconda or Anaconda)
- Ollama installed and running
- H&M dataset at `../hm_with_images/`

### Installation

#### Option 1: Automated Setup (Recommended)

Simply run the startup script:
```bash
./start.sh
```

This will:
- Create conda environment from `environment.yml`
- Install all dependencies
- Check Ollama connection
- Start the FastAPI server

#### Option 2: Manual Setup

1. Create conda environment:
```bash
conda env create -f environment.yml
conda activate shopsight
```

2. Setup environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Install and start Ollama:
```bash
# Install Ollama from https://ollama.ai
ollama serve

# In another terminal, pull the model
ollama pull llama3.2
```

### Running the Application

```bash
# Activate conda environment
conda activate shopsight

# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the startup script
./start.sh
```

The API will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Docker Deployment

```bash
# Build image
docker build -t shopsight-backend .

# Run container
docker run -p 8000:8000 \
  -v $(pwd)/../hm_with_images:/data \
  -e ARTICLES_PATH=/data/articles/*.parquet \
  -e CUSTOMERS_PATH=/data/customers/*.parquet \
  -e TRANSACTIONS_PATH=/data/transactions/*.parquet \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  shopsight-backend
```

## API Endpoints

### Health Check
```
GET /health
```

Returns service health status.

### Search Products
```
POST /api/search
```

Search products with natural language queries.

**Request Body:**
```json
{
  "query": "Nike running shoes",
  "limit": 20,
  "include_sales": true,
  "include_forecast": true,
  "include_segments": true,
  "date_range": {
    "start": "2019-01-01",
    "end": "2020-09-22"
  }
}
```

**Response:**
```json
{
  "query": "Nike running shoes",
  "parsed_query": {
    "keywords": ["Nike", "running", "shoes"],
    "filters": {},
    "intent": "product_search"
  },
  "products": [...],
  "sales_data": {...},
  "insights": {...},
  "forecast": {...},
  "customer_segments": [...],
  "metadata": {
    "processing_time_ms": 1245,
    "product_count": 12,
    "llm_calls": 2
  }
}
```

### Get Product Details
```
GET /api/products/{article_id}?include_sales=true
```

Get detailed information about a specific product.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration
│   ├── dependencies.py         # Dependency injection
│   │
│   ├── api/
│   │   ├── routes.py           # API endpoints
│   │   └── middleware.py       # CORS, error handlers
│   │
│   ├── agents/
│   │   ├── orchestrator.py     # LLM agent
│   │   └── prompts.py          # Prompt templates
│   │
│   ├── services/
│   │   ├── product_search.py   # Product search (REAL)
│   │   ├── sales_analyzer.py   # Sales analytics (REAL)
│   │   ├── forecaster.py       # Forecasting (MOCKED)
│   │   └── segmenter.py        # Segmentation (MOCKED)
│   │
│   ├── db/
│   │   └── duckdb_client.py    # DuckDB client
│   │
│   ├── models/
│   │   ├── entities.py         # Domain entities
│   │   ├── requests.py         # Request models
│   │   └── responses.py        # Response models
│   │
│   └── utils/
│       ├── logger.py           # Logging
│       └── exceptions.py       # Custom exceptions
│
├── tests/
│   ├── test_api.py
│   ├── test_services.py
│   └── test_agents.py
│
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_api.py -v
```

## Development

### Code Formatting

```bash
# Format code with black
black app/

# Lint with ruff
ruff check app/
```

### Adding New Features

1. Define models in `app/models/`
2. Implement service logic in `app/services/`
3. Add API endpoint in `app/api/routes.py`
4. Write tests in `tests/`

## Architecture

### Request Flow

```
HTTP Request
    ↓
[FastAPI Router] → Validate request (Pydantic)
    ↓
[API Handler] → Extract parameters
    ↓
[Agent Orchestrator] → Parse query with LLM
    ↓
[Services Layer] → Execute business logic
    ↓
[DuckDB Client] → Query parquet files
    ↓
[Response Builder] → Format response (Pydantic)
    ↓
HTTP Response (JSON)
```

### LLM Integration

The application uses Ollama for two main tasks:

1. **Query Parsing**: Convert natural language to structured search parameters
2. **Insight Generation**: Analyze sales data and generate human-readable summaries

Both operations include fallback mechanisms for robustness.

## Performance

Expected performance on modern hardware (8GB RAM, 4-core CPU):

| Operation | Target | Note |
|-----------|--------|------|
| Product search | < 100ms | DuckDB query on 105K products |
| Sales aggregation | < 300ms | Single product, 2 years |
| LLM query parsing | < 3s | Depends on Ollama performance |
| LLM insight generation | < 5s | Depends on Ollama performance |
| Full search request | < 8s | Including all operations |

## Real vs Mocked Features

### REAL (Production-Ready)
- Product search with natural language parsing
- Historical sales data from 31.8M transactions
- AI-generated insights from actual patterns
- Product catalog with 105K items

### MOCKED (Demo/Prototype)
- Demand forecasting (linear extrapolation)
- Customer segmentation (rule-based on age)

All mocked features are clearly labeled in API responses.

## Troubleshooting

### Ollama Connection Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve
```

### DuckDB Query Errors
- Verify parquet file paths in `.env`
- Check file permissions
- Ensure files match expected schema

### Performance Issues
- Adjust `DUCKDB_THREADS` and `DUCKDB_MEMORY_LIMIT` in `.env`
- Consider using a smaller LLM model (e.g., Phi-3 Mini)
- Add query result caching

## License

Internal use only. Not for distribution.

## Support

For issues or questions, contact the engineering team.
