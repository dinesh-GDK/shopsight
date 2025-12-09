# ShopSight - AI-Powered E-commerce Analytics

[![Status](https://img.shields.io/badge/status-prototype-blue)](https://github.com/yourusername/shopsight)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**An agentic e-commerce analytics platform that enables natural language product search with AI-powered insights, sales forecasting, and customer segmentation.**

<p align="center">
  <video src="assets/demo.mp4" controls width="75%">
    Your browser does not support the video tag.
  </video>
</p>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Thought Process & Prioritization](#thought-process--prioritization)
- [Key Features](#key-features)
- [What's Real vs. What's Mocked](#whats-real-vs-whats-mocked)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Assumptions](#assumptions)
- [Implementation Gaps & Future Work](#implementation-gaps--future-work)
- [Documentation](#documentation)

---

## 🎯 Overview

ShopSight is a prototype e-commerce analytics platform built. It demonstrates an end-to-end agentic workflow where users can:

1. **Search products** using natural language (e.g., "Sports equipment")
2. **View historical sales** trends with interactive charts
3. **Get AI-generated insights** explaining sales patterns and opportunities
4. **See demand forecasts** and customer segmentation analysis
5. **Filter by confidence** to see only the most relevant results

The platform processes **31.8M transactions**, **105K products**, and **1.37M customers** from the H&M dataset to deliver real-time analytics.

---

## 💭 Thought Process & Prioritization

### What I Prioritized (and Why)

#### 1. **Core User Journey First** ✅
I focused on implementing one complete, working flow end-to-end:
- **Product search → Sales visualization → AI insights**

**Rationale:** This represents the most valuable user journey and demonstrates all key technical capabilities:
- Natural language processing (LLM)
- Database querying at scale (DuckDB on 31M rows)
- Real-time data visualization
- AI-powered analysis

#### 2. **Real Data with Simple UX** ✅
Rather than spending time on pixel-perfect UI, I prioritized:
- Querying actual transactional data (31.8M rows)
- Real LLM integration (Ollama with Llama 3.2)
- Accurate analytics computation
- Simple intuitive UI for smooth experience

**Rationale:** For a technical demo, showing the system works with real data at scale is more impressive than animations and polish.

#### 3. **Clear Separation: Real vs. Mocked** ✅
All mocked features are clearly labeled with:
- Orange "FORECASTED" badges
- Disclaimer text in the UI
- Documentation in README

**Rationale:** Reviewers should immediately understand what's real vs. demo-quality.

#### 4. **LLM Integration as Core Differentiator** ✅
I used LLMs for:
- **Query parsing:** "Nike running shoes" → `{brand: "Nike", type: "shoes", category: "running"}`
- **Insight generation:** Analyzing sales data and generating human-readable summaries
- **Confidence scoring:** Intelligent search relevance ranking

**Rationale:** This is what makes the platform "agentic" rather than just another analytics dashboard.

#### 5. **Advanced Features for Delight** ✨
Beyond the base requirements, I added:
- **Confidence-based filtering** with interactive slider (see `FEATURE_CONFIDENCE_SCORING.md`)
- **Seasonality analysis** with peak month detection (see `FEATURE_SALES_TREND.md`)
- **Pagination** for large result sets
- **Markdown rendering** in AI insights for rich formatting

**Rationale:** These "thoughtful touches" show engineering maturity and attention to user experience.

### What I Deprioritized

- ❌ **Product comparison feature** - Nice-to-have, not core to demo
- ❌ **Advanced filters** (price range, date range UI) - Can be added in 30 mins
- ❌ **Export to CSV** - Simple to add, but not differentiating
- ❌ **Dark mode** - Polish, not substance
- ❌ **Docker Compose** - Manual setup is acceptable for prototype

---

## ✨ Key Features

### Core Features (Fully Functional)

| Feature | Description | Status |
|---------|-------------|--------|
| **Natural Language Search** | Search products using conversational queries powered by Llama 3.2 | ✅ REAL |
| **Product Catalog** | Browse 105,542 products with images and metadata | ✅ REAL |
| **Historical Sales Visualization** | Interactive charts showing revenue, transactions, and trends | ✅ REAL |
| **AI-Generated Insights** | LLM analyzes sales data and generates business insights | ✅ REAL |
| **Confidence Scoring** | Search results ranked by relevance (0-100%) with interactive filtering | ✅ REAL |
| **Seasonality Analysis** | Automatic detection of seasonal patterns with peak month identification | ✅ REAL |
| **Sales Trend Analysis** | Monthly sales visualization with data quality indicators | ✅ REAL |
| **Pagination** | Navigate through large result sets efficiently | ✅ REAL |

### Mocked Features (Demo Quality)

| Feature | Description | Status |
|---------|-------------|--------|
| **Demand Forecasting** | Next 3 months predictions using linear extrapolation | 🟡 MOCKED |
| **Customer Segmentation** | Age-based buyer demographics using rule-based logic | 🟡 MOCKED |

All mocked features are clearly labeled in the UI with badges and disclaimers.

---

## 🔍 What's Real vs. What's Mocked

### ✅ REAL

#### 1. Product Search with LLM Query Parsing
- **Data:** 105,542 real products from H&M dataset
- **Implementation:**
  - Ollama LLM (Llama 3.2) extracts brand, type, color from natural language
  - DuckDB performs optimized keyword search with word-boundary matching
  - Returns results in <100ms
- **Example:** "Nike running shoes" → Finds products matching Nike brand AND running/shoes type

#### 2. Confidence Scoring System
- **Algorithm:** Multi-factor weighted scoring
  - Brand match: 35%
  - Type match: 30%
  - Color match: 20%
  - Name match: 15%
- **Features:**
  - Word-boundary matching prevents false positives (e.g., "Nike" ≠ "Jannike")
  - Interactive slider for real-time filtering
  - Results sorted by relevance
- **See:** `FEATURE_CONFIDENCE_SCORING.md` for details

#### 3. Historical Sales Analytics
- **Data:** 31,788,324 real transactions spanning Sept 2018 - Sept 2020
- **Queries:**
  - Aggregate sales by month/week/day
  - Calculate revenue, transaction count, average price
  - Join with customer data for demographics
- **Performance:** Queries 31M rows in ~200ms using DuckDB's columnar engine

#### 4. Seasonality Detection
- **Formula:** `seasonality_score = max(monthly_sales) / mean(monthly_sales)`
- **Interpretation:**
  - < 1.5: Low seasonality (flat sales)
  - 1.5-2.0: Moderate seasonality
  - \> 2.0: Strong seasonality (significant peaks)
- **Implementation:** Real-time computation from transaction data
- **See:** `FEATURE_SALES_TREND.md` for details

#### 5. AI-Powered Insights
- **LLM:** Llama 3.2 (3B parameters) running locally via Ollama
- **Process:**
  1. Extract sales metrics (total revenue, peak month, growth rate)
  2. Send to LLM with structured prompt
  3. Generate 2-3 actionable insights
- **Fallback:** If LLM fails, returns basic statistical summary
- **Latency:** ~4 seconds for insight generation

### 🟡 MOCKED (Demo/Prototype Quality)

These features use simplified algorithms to demonstrate UI/UX:

#### 1. Demand Forecasting
- **Algorithm:** Linear extrapolation from last 3 months
  ```python
  avg_growth = (month_3_sales - month_1_sales) / 2
  forecast[i] = last_month_sales + (avg_growth * i)
  ```
- **Why Mocked:** True forecasting requires:
  - Time series models (ARIMA, Prophet, LSTMs)
  - Seasonality adjustment
  - External factors (promotions, holidays, trends)
  - Validation on holdout sets
- **How to Make Real:** Use Prophet or statsmodels with 12+ months training data

#### 2. Customer Segmentation
- **Algorithm:** Rule-based age grouping
  ```python
  if age < 30: segment = "Young Professionals"
  elif age < 50: segment = "Established Adults"
  else: segment = "Mature Customers"
  ```
- **Why Mocked:** Real segmentation requires:
  - Clustering algorithms (K-means, DBSCAN)
  - Multi-dimensional features (RFM, purchase patterns, CLV)
  - Behavioral analysis
- **How to Make Real:** Implement RFM analysis with K-means clustering on customer transaction history

---

## 🛠 Tech Stack

### Frontend
- **Framework:** React 18.2 with Vite 5.0 (fast HMR, optimized builds)
- **Styling:** TailwindCSS 3.4 (utility-first, rapid development)
- **Charts:** Recharts 2.10 (React-native, composable)
- **Icons:** Lucide React (lightweight, tree-shakeable)
- **Markdown:** react-markdown (for rich AI insights)

### Backend
- **Framework:** FastAPI 0.104.1 (async, auto-docs, type hints)
- **Language:** Python 3.11
- **Database:** DuckDB 0.9.2 (embedded, queries Parquet directly)
- **LLM:** Ollama with Llama 3.2 (3B params, local execution)
- **Data:** Pandas 2.1.3, NumPy 1.26.2

### Data
- **Format:** Parquet (columnar, compressed)
- **Size:** ~2.2GB (105K products, 1.37M customers, 31.8M transactions)
- **Storage:** Local filesystem (no cloud dependencies)

### Infrastructure
- **Development:** Conda environments for reproducibility
- **Deployment:** Docker support (optional)
- **API Docs:** Auto-generated via FastAPI (Swagger + ReDoc)

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:
- **Python 3.11+** (with Conda recommended)
- **Node.js 18+** and npm
- **Ollama** ([download here](https://ollama.ai))
- **H&M Dataset** at `./hm_with_images/` (downloaded via `explore/download_s3_files.py`)

### Quick Start (Recommended)

#### 1. Download Dataset (First Time Only)

```bash
# Navigate to explore directory
cd explore

# Download dataset from S3 
python download_s3_files.py

```

#### 2. Start Backend

```bash
# Navigate to backend
cd backend

# Option A: Automated setup (recommended)
./start.sh

# Option B: Manual setup
conda env create -f environment.yml
conda activate shopsight
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### 3. Start Ollama (Separate Terminal)

```bash
# Start Ollama server
ollama serve

# In another terminal, pull the model (one-time, ~2GB)
ollama pull llama3.2

# Verify model is available
ollama list
```

#### 4. Start Frontend

```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start dev server
npm run dev
```

The frontend will be available at: http://localhost:5173

### Verification

1. Open http://localhost:5173 in your browser
2. Try searching for "Nike running shoes"
3. You should see:
   - Product results with confidence scores
   - Historical sales chart
   - AI-generated insights
   - Seasonality analysis

### Troubleshooting

**Backend won't start:**
```bash
# Check if port 8000 is in use
lsof -i :8000

# Verify data files exist
ls -lh ../hm_with_images/articles/*.parquet
ls -lh ../hm_with_images/transactions/*.parquet
```

**Ollama connection failed:**
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
pkill ollama
ollama serve
```

**Frontend API errors:**
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check environment variables
cat frontend/.env
# Should contain: VITE_API_URL=http://localhost:8000
```

---

## 📁 Project Structure

```
shopsight/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── agents/          # LLM agent orchestration
│   │   ├── api/             # API routes and middleware
│   │   ├── db/              # DuckDB client
│   │   ├── models/          # Pydantic models
│   │   ├── services/        # Business logic
│   │   │   ├── product_search.py        # Search (REAL)
│   │   │   ├── confidence_scorer.py     # Scoring (REAL)
│   │   │   ├── sales_analyzer.py        # Analytics (REAL)
│   │   │   ├── forecaster.py            # Forecast (MOCKED)
│   │   │   └── segmenter.py             # Segments (MOCKED)
│   │   └── utils/           # Helpers and validators
│   ├── tests/               # Unit and integration tests
│   ├── start.sh             # Automated startup script
│   └── README.md            # Backend documentation
│
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── analytics/   # Charts and metrics
│   │   │   ├── insights/    # AI insights panels
│   │   │   ├── products/    # Product cards and grids
│   │   │   ├── search/      # Search bar and filters
│   │   │   └── common/      # Reusable components
│   │   ├── services/        # API client
│   │   ├── hooks/           # Custom React hooks
│   │   └── App.jsx          # Main application
│   └── README.md            # Frontend documentation
│
├── hm_with_images/          # Dataset (downloaded separately)
│   ├── articles/            # Product catalog (105K products)
│   ├── customers/           # Customer data (1.37M customers)
│   └── transactions/        # Sales history (31.8M transactions)
│
├── documents/               # Design documentation
│   ├── ASSIGNMENT.md        # Original take-home requirements
│   ├── SYSTEM_DESIGN.md     # Architecture and design decisions
│   ├── BACKEND_SPEC.md      # Backend technical specification
│   └── FRONTEND_SPEC.md     # Frontend technical specification
│
├── explore/                 # Dataset exploration scripts
│   ├── download_s3_files.py # Download H&M dataset from S3
│   └── explore.py           # Data exploration utilities
│
└── README.md                # This file
```

---

## 📝 Assumptions

### Dataset Assumptions

1. **Data Quality:** Parquet files are well-formed and match the documented schema
2. **Completeness:** All transactions have valid `article_id` and `customer_id` foreign keys
3. **Date Range:** All analysis is scoped to the available range (Sept 2018 - Sept 2020)
4. **Price Normalization:** Prices in the dataset are already normalized/converted to a common currency

### Infrastructure Assumptions

1. **Local Execution:** Demo runs entirely on localhost (no cloud services required)
2. **Hardware:** Development machine has:
   - 8GB+ RAM (for DuckDB in-memory processing)
   - 4+ CPU cores (for parallel query execution)
   - ~5GB disk space (dataset + models)
3. **Network:** One-time internet access required to:
   - Download H&M dataset (~2.2GB)
   - Pull Ollama model (~2GB)
   - Install dependencies

### User Assumptions

1. **Search Queries:** Users will use natural language (not SQL or structured queries)
2. **Domain Knowledge:** Users understand basic e-commerce concepts (revenue, transactions, SKUs)
3. **Browser:** Modern browser with JavaScript enabled (Chrome, Firefox, Safari, Edge)

### Scope Assumptions

1. **Single Product Analysis:** For MVP, analyzing one product or product category at a time
2. **Read-Only:** No mutations or data writes (pure analytics platform)
3. **English Only:** LLM prompts and responses are in English
4. **Desktop-First:** UI optimized for desktop (1920x1080), responsive design for mobile is basic

---

## 🔧 Implementation Gaps & Future Work

### Gaps in Current Implementation

#### 1. **Search Results**

**Current State:** We get the search query and extract the keyworkds using LLM. Using the keywords we do search.

**Limitations:**
- Doesn't account for complete context of the search query. If we search 'Nike running shoes', we might some running shoes other than Nike (But the confidence score will be low).

**Improvements:**
- Use vector search
  - Convert the atributes of the product to vector and store it in vector database.
  - Conver the incoming search query to vector.
  - Find vectors in the vector database that are similar to search query vector.
  - Use the resultant vectors and fetch the corresponding product.

#### 2. **Forecasting is Oversimplified**

**Current State:** Linear extrapolation from last 3 months
```python
forecast = last_revenue + avg_growth_rate * months_ahead
```

**Limitations:**
- Doesn't account for seasonality (Christmas vs. July)
- Ignores external factors (promotions, market trends)
- No confidence intervals or uncertainty quantification

**How to Build Real Forecasting:**

```python
# Option 1: Prophet (Facebook's time series library)
from prophet import Prophet

def forecast_with_prophet(sales_history):
    df = pd.DataFrame({
        'ds': sales_history['date'],
        'y': sales_history['revenue']
    })

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        changepoint_prior_scale=0.05
    )
    model.fit(df)

    future = model.make_future_dataframe(periods=90, freq='D')
    forecast = model.predict(future)

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

# Option 2: ARIMA for statistical modeling
from statsmodels.tsa.arima.model import ARIMA

def forecast_with_arima(sales_history, order=(2,1,2)):
    model = ARIMA(sales_history['revenue'], order=order)
    fitted = model.fit()
    forecast = fitted.forecast(steps=90)
    return forecast
```

#### 3. **Customer Segmentation Lacks Sophistication**

**Current State:** Rule-based age grouping
```python
if age < 30: return "Young Professionals"
```

**Limitations:**
- Only uses age (ignores purchase behavior, CLV, frequency)
- Fixed segments (no data-driven clustering)
- Doesn't identify high-value customers

**How to Build Real Segmentation:**

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def rfm_segmentation(transactions, customers):
    # 1. Calculate RFM metrics
    rfm = transactions.groupby('customer_id').agg({
        't_dat': lambda x: (pd.Timestamp.now() - x.max()).days,  # Recency
        'transaction_id': 'count',                                 # Frequency
        'price': 'sum'                                            # Monetary
    })
    rfm.columns = ['recency', 'frequency', 'monetary']

    # 2. Normalize features
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm)

    # 3. K-means clustering
    kmeans = KMeans(n_clusters=4, random_state=42)
    rfm['segment'] = kmeans.fit_predict(rfm_scaled)

    # 4. Label segments
    segment_labels = {
        0: "Champions",      # High R, F, M
        1: "Loyal Customers", # High F, M
        2: "At Risk",        # Low R, High F, M
        3: "Lost"            # Low R, F, M
    }

    return rfm.assign(segment_name=rfm['segment'].map(segment_labels))
```

#### 4. **No Product Comparison Feature**

**Gap:** Users can't compare 2+ products side-by-side

**How to Build:**

1. **UI Component:**
   - Multi-select product cards
   - "Compare" button appears when 2+ selected
   - Modal/page showing side-by-side comparison

2. **API Endpoint:**
   ```python
   @router.post("/api/compare")
   async def compare_products(article_ids: List[int]):
       products = [get_product(id) for id in article_ids]
       sales = [get_sales_history(id) for id in article_ids]

       return {
           "products": products,
           "comparison": {
               "revenue": [s.total_revenue for s in sales],
               "growth_rate": [calculate_growth(s) for s in sales],
               "seasonality": [s.seasonality_score for s in sales]
           }
       }
   ```

#### 5. **Limited Search Filters**

**Gap:** No UI for advanced filters (price range, date range, department)

**Current State:** Filters are supported in backend API but not exposed in frontend

**How to Build:**

1. Add filter panel component in frontend
2. Wire up to existing backend endpoints (already support filters)
3. Update search request to include filter parameters

#### 6. **No Data Export**

**Gap:** Users can't export charts or data to CSV/Excel

**How to Build:**

```javascript
// Frontend: Export to CSV
function exportToCSV(data, filename) {
    const csv = data.map(row => Object.values(row).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
}

// Backend: PDF report generation
from fpdf import FPDF

@router.get("/api/export/pdf/{article_id}")
async def export_product_report(article_id: int):
    product = get_product(article_id)
    sales = get_sales_history(article_id)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Product Report: {product.name}", ln=True)
    # Add sales charts, metrics, insights...

    return Response(content=pdf.output(dest='S'), media_type="application/pdf")
```

### Future Enhancements

#### Machine Learning Opportunities

1. **Product Recommendations:** "Customers who bought X also bought Y"
2. **Churn Prediction:** Identify customers likely to stop purchasing
3. **Price Optimization:** Suggest optimal pricing based on demand elasticity
4. **Inventory Optimization:** Predict stock needs based on forecasted demand
5. **Anomaly Detection:** Alert on unusual sales patterns

#### User Experience Improvements

1. **Search History:** Save and recall previous searches
2. **Dashboards:** Customizable widgets and layouts
3. **Alerts:** Set thresholds and get notifications (email, Slack)
4. **Mobile App:** Native iOS/Android experience
5. **Collaborative Features:** Share insights with team members

#### Infrastructure Enhancements

1. **Caching:** Redis layer for frequent queries
2. **Background Jobs:** Celery for long-running analytics
3. **Multi-Tenancy:** Support multiple companies/datasets
4. **SSO Integration:** Okta, Auth0 for enterprise auth
5. **Monitoring:** Datadog, New Relic for observability

---

### Example Queries to Try

1. **"Black jackets"** - Tests filters and price constraints
2. **"Women's winter clothing"** - Tests gender + season detection
3. **"Sportswear"** - Tests department + age group

### Expected Results

- **Products Found:** 10-50 products (depending on query specificity)
- **Response Time:** 2-6 seconds (including LLM processing)
- **Confidence Scores:** Typically 60-95% for relevant results
- **Sales Data:** Monthly aggregations from Sept 2018 - Sept 2020
- **AI Insights:** 2-3 bullet points highlighting trends and opportunities

---

## 📚 Documentation

Detailed technical documentation is available in the `documents/` directory:

- **[ASSIGNMENT.md](documents/ASSIGNMENT.md)** - Original take-home exercise requirements
- **[SYSTEM_DESIGN.md](documents/SYSTEM_DESIGN.md)** - Architecture, design decisions, and tradeoffs
- **[BACKEND_SPEC.md](documents/BACKEND_SPEC.md)** - Backend API specification and implementation guide
- **[FRONTEND_SPEC.md](documents/FRONTEND_SPEC.md)** - Frontend component specifications and UI guidelines

---

### Optimization Techniques

1. **DuckDB Columnar Queries:** Parquet files enable zero-ETL analytics
2. **In-Memory Processing:** DuckDB loads hot data into RAM for fast aggregations
3. **LLM Caching:** Repeated queries hit cache instead of re-running inference
4. **Parallel Execution:** Backend uses async/await for concurrent operations
5. **Frontend Debouncing:** Search input debounced to 500ms to reduce API calls


### Code Style

- **Backend:** Follow PEP 8, use `black` for formatting, `ruff` for linting
- **Frontend:** Use ESLint with React plugin, Prettier for formatting
- **Commits:** Use conventional commits (feat, fix, docs, style, refactor, test, chore)

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- **H&M Dataset:** [Kaggle H&M Personalized Fashion Recommendations](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations)
- **Ollama:** Local LLM runtime for privacy-preserving AI
- **DuckDB:** Embedded analytical database enabling zero-ETL workflows
- **Kumo AI:** For the opportunity to build this prototype
