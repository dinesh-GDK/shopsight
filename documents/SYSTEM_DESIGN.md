# ShopSight - System Design Document

**Version:** 1.0
**Date:** December 7, 2024
**Author:** Senior Engineering Team
**Status:** Approved for Implementation

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Requirements](#requirements)
3. [System Architecture](#system-architecture)
4. [Technology Stack](#technology-stack)
5. [Data Architecture](#data-architecture)
6. [LLM Integration Strategy](#llm-integration-strategy)
7. [Design Decisions & Tradeoffs](#design-decisions--tradeoffs)
8. [Implementation Phases](#implementation-phases)
9. [Risk Assessment](#risk-assessment)

---

## Executive Summary

ShopSight is an **agentic e-commerce analytics platform** that enables users to search for products using natural language and receive comprehensive insights including:
- Historical sales trends and patterns
- Demand forecasting predictions
- Customer segmentation analysis
- AI-generated actionable insights

This is an **internal MVP** designed to demonstrate the feasibility of LLM-powered analytics interfaces. The system will run entirely locally, making it suitable for rapid iteration and customer demos without cloud dependencies.

**Key Success Metrics:**
- ✅ Product search → sales visualization working end-to-end
- ✅ Sub-3 second query response time
- ✅ AI-generated insights that are accurate and actionable
- ✅ Demoable UI with professional polish

---

## Requirements

### Functional Requirements

#### FR1: Natural Language Product Search
- **Description:** Users can search for products using conversational queries
- **Examples:**
  - "Nike running shoes"
  - "Women's jackets under $50"
  - "Show me best-selling items from 2019"
- **Priority:** P0 (Must Have)
- **Implementation:** REAL

#### FR1.5: Confidence-Based Search Relevance Scoring
- **Description:** Each search result receives a confidence score (0.0-1.0) indicating how well it matches the user's query
- **Scoring Components:**
  - Brand match (35%): Word-boundary matching prevents false positives (e.g., "Nike" ≠ "Jannike")
  - Type match (30%): Product category alignment (e.g., "shoes", "jacket")
  - Color match (20%): Color attribute matching
  - Name match (15%): Keyword presence in product name
- **Features:**
  - Default minimum confidence threshold: 0.5 (50%)
  - Interactive confidence slider for dynamic filtering
  - Results sorted by confidence score (descending)
  - Visual confidence badges on product cards
- **Priority:** P0 (Must Have)
- **Implementation:** REAL
- **Benefits:**
  - Reduces irrelevant results in search
  - Improves user experience with quality filtering
  - Provides transparency in result relevance

#### FR2: Historical Sales Visualization
- **Description:** Display time-series charts of sales data for selected products
- **Metrics:** Revenue, transaction count, average price
- **Time Granularity:** Daily, Weekly, Monthly views
- **Priority:** P0 (Must Have)
- **Implementation:** REAL

#### FR3: AI-Generated Insights
- **Description:** LLM analyzes sales data and generates human-readable summaries
- **Examples:**
  - "Sales peaked during holiday season (Dec 2019) with 45% increase"
  - "Declining trend detected in Q2 2020, likely due to seasonal factors"
- **Priority:** P0 (Must Have)
- **Implementation:** REAL

#### FR3.5: Sales Trend & Seasonality Analysis
- **Description:** Compute and visualize monthly sales trends with seasonality scoring
- **Metrics:** Unit sales by month, seasonality score (peak ratio method), peak months identification
- **Formula:** `seasonality_score = max(monthly_sales) / mean(monthly_sales)`
- **Interpretation:**
  - < 1.5: Low seasonality (flat sales pattern)
  - 1.5-2.0: Moderate seasonality
  - > 2.0: Strong seasonality (significant peaks)
- **Priority:** P0 (Must Have)
- **Implementation:** REAL

#### FR4: Demand Forecasting
- **Description:** Predict future sales based on historical patterns
- **Time Horizon:** Next 1-3 months
- **Priority:** P1 (Should Have)
- **Implementation:** MOCKED (simple linear extrapolation)

#### FR5: Customer Segmentation
- **Description:** Show likely buyer demographics and segments
- **Segments:** Age groups, membership status, geographic distribution
- **Priority:** P1 (Should Have)
- **Implementation:** MOCKED (rule-based segments)

#### FR6: Product Catalog Browsing
- **Description:** Browse products with images, descriptions, and metadata
- **Priority:** P0 (Must Have)
- **Implementation:** REAL

### Non-Functional Requirements

#### NFR1: Performance
- **Search Latency:** < 2 seconds for product search
- **Query Response:** < 3 seconds for sales data aggregation
- **LLM Inference:** < 5 seconds for insight generation
- **Chart Rendering:** < 1 second for up to 2 years of data

#### NFR2: Scalability (Local Context)
- Handle 105K products in catalog
- Process 31.8M transactions efficiently
- Support concurrent queries (5+ simultaneous users for demo)

#### NFR3: Usability
- Intuitive search interface requiring zero training
- Clear visual hierarchy in dashboard
- Responsive design (desktop-first, 1920x1080 optimal)

#### NFR4: Maintainability
- Clean separation of concerns (frontend/backend/data)
- Well-documented APIs
- Type-safe contracts (Pydantic, TypeScript)

#### NFR5: Privacy & Security
- All data processing happens locally
- No external API calls (except local Ollama)
- No telemetry or tracking

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                           │
│              React SPA (localhost:5173)                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ HTTP/REST
                        │
┌───────────────────────┴────────────────────────────────────┐
│                  API GATEWAY LAYER                         │
│                FastAPI (localhost:8000)                    │
│                                                            │
│  ┌───────────────────────────────────────────────────┐     │
│  │         LLM AGENT ORCHESTRATOR                    │     │
│  │  ┌──────────────────────────────────────────┐     │     │
│  │  │  Query Understanding & Intent Detection  │     │     │
│  │  └──────────────────────────────────────────┘     │     │
│  │  ┌──────────────────────────────────────────┐     │     │
│  │  │  Tool Router & Execution Engine          │     │     │
│  │  └──────────────────────────────────────────┘     │     │
│  │  ┌──────────────────────────────────────────┐     │     │
│  │  │  Insight Generator & Summarizer          │     │     │
│  │  └──────────────────────────────────────────┘     │     │
│  └───────────────────────────────────────────────────┘     │
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Product    │  │    Sales     │  │  Analytics   │      │
│  │   Search     │  │   Analyzer   │  │   Services   │      │
│  │   Service    │  │   Service    │  │  (Forecast,  │      │
│  │   (REAL)     │  │   (REAL)     │  │  Segment)    │      │
│  │              │  │              │  │  (MOCKED)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────┬────────────────────────────────────┘
                        │
                        │ SQL Queries
                        │
┌───────────────────────┴──────────────────────────────────────┐
│                   DATA ACCESS LAYER                          │
│                  DuckDB In-Memory Engine                     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐      │
│  │  Parquet File Scanner (Zero-Copy Access)           │      │
│  └────────────────────────────────────────────────────┘      │
│                                                              │
│  Data Sources:                                               │
│  - ./hm_with_images/articles/*.parquet     (105K products)   │
│  - ./hm_with_images/customers/*.parquet    (1.37M customers) │
│  - ./hm_with_images/transactions/*.parquet (31.8M txns)      │
└──────────────────────────────────────────────────────────────┘

External Dependency (Local):
┌─────────────────────────────────────┐
│     Ollama LLM Runtime              │
│     (localhost:11434)               │
│     Model: Llama 3.2 (3B params)    │
└─────────────────────────────────────┘
```

### Component Interaction Flow

**Scenario: User searches "Nike running shoes"**

```
[User] → Types query in search bar
   ↓
[React App] → POST /api/search {"query": "Nike running shoes"}
   ↓
[FastAPI Router] → Receives request, validates input
   ↓
[LLM Agent] → Calls Ollama: "Parse this search query into structured filters"
   ↓
[Ollama] → Returns: {"brand": "Nike", "category": "running", "type": "shoes"}
   ↓
[Product Search Service] → DuckDB Query:
   SELECT article_id, prod_name, product_type_name, colour_group_name,
          department_name, index_name, image_url
   FROM read_parquet('./hm_with_images/articles/*.parquet')
   WHERE (LOWER(prod_name) LIKE '%nike%' OR LOWER(product_type_name) LIKE '%nike%')
      OR (LOWER(prod_name) LIKE '%running%' OR LOWER(product_type_name) LIKE '%running%')
   LIMIT ? OFFSET ?
   ↓
[Agent] → Found 12 products, now fetch sales data
   ↓
[Sales Analyzer Service] → DuckDB Query:
   SELECT DATE_TRUNC('month', t_dat) as month,
          COUNT(*) as transaction_count,
          SUM(price) as total_revenue,
          AVG(price) as avg_price
   FROM read_parquet('./hm_with_images/transactions/*.parquet')
   WHERE article_id IN (...)
   GROUP BY month
   ORDER BY month
   ↓
[Agent] → Calls Ollama: "Generate insights from this sales data"
   ↓
[Ollama] → Returns: "Nike running shoes show consistent demand with peak
              sales in December 2019 ($45K revenue, 230 transactions)..."
   ↓
[Forecaster Service] → Generates mock forecast (linear extrapolation)
   ↓
[Segmenter Service] → Returns mock customer segments
   ↓
[FastAPI] → Aggregates all responses into JSON:
   {
     "query": "Nike running shoes",
     "parsed_query": {"keywords": [...], "filters": {}, "intent": "..."},
     "products": [...],
     "pagination": {
       "current_page": 1,
       "page_size": 20,
       "total_items": 12,
       "total_pages": 1,
       "has_next": false,
       "has_prev": false
     },
     "sales_data": {
       "timeline": [...],
       "summary": {...}
     },
     "insights": {
       "text": "...",
       "key_findings": [...]
     },
     "forecast": {
       "predictions": [...],
       "note": "..."
     },
     "customer_segments": [...],
     "metadata": {
       "processing_time_ms": 1245,
       "product_count": 12,
       "llm_calls": 2
     }
   }
   ↓
[React App] → Renders dashboard with charts and insights
```

---

## Technology Stack

### Frontend Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Framework | React 18.2 | Industry standard, large ecosystem, simple for MVP |
| Build Tool | Vite 5.0 | Fast dev server, instant HMR, simple config |
| Language | JavaScript (ES6+) | Rapid development, optional TypeScript later |
| Styling | TailwindCSS 3.4 | Utility-first, rapid UI development |
| Charts | Recharts 2.10 | React-native, composable, good documentation |
| HTTP Client | Axios 1.6 | Simple API, better error handling than fetch |
| State Management | React Hooks (useState, useContext) | Built-in, sufficient for MVP complexity |
| Routing | React Router 6 | Standard SPA routing (if multi-page needed) |

### Backend Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Framework | FastAPI 0.104 | Fast dev, auto docs, async support, type hints |
| Language | Python 3.11 | Best LLM/data ecosystem, team expertise |
| Database | DuckDB 0.9 | Embedded, queries parquet directly, SQL interface |
| LLM Runtime | Ollama | Local execution, no API costs, privacy |
| LLM Model | Llama 3.2 (3B) | Fast inference on CPU, good reasoning, small footprint |
| Data Validation | Pydantic 2.5 | Type safety, auto validation, FastAPI integration |
| Environment | Conda | Better package management, dependency resolution |

### Data & Infrastructure

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Data Format | Parquet | Columnar, compressed, industry standard |
| Query Engine | DuckDB SQL | Zero-ETL, fast aggregations, SQL familiarity |
| File Storage | Local filesystem | No cloud needed for MVP |
| Containerization | Docker (optional) | Easy demo deployment |
| Development | Docker Compose | Single-command startup |

---

## Data Architecture

### Dataset Overview

**Source:** H&M E-commerce Dataset (s3://kumo-public-datasets/hm_with_images/)

| File | Records | Size | Schema Key Fields |
|------|---------|------|-------------------|
| articles/*.parquet | 105,542 products | ~50MB | article_id, prod_name, product_type_name, colour_group_name, department_name, index_name (image URL) |
| customers/*.parquet | 1,371,980 customers | ~80MB | customer_id, age, postal_code, club_member_status, fashion_news_frequency |
| transactions/*.parquet | 31,788,324 transactions | ~2GB | t_dat (date), article_id, customer_id, price, sales_channel_id |

**Date Range:** September 20, 2018 → September 22, 2020 (734 days)

**Partitioning Strategy:** Transactions partitioned by customer_id (68 files, hash-based distribution)

### Data Model

```sql
-- Products (Articles)
CREATE TABLE articles (
    article_id BIGINT PRIMARY KEY,
    prod_name VARCHAR,
    product_type_name VARCHAR,
    product_type_no INT,
    product_group_name VARCHAR,
    graphical_appearance_name VARCHAR,
    colour_group_name VARCHAR,
    perceived_colour_value_name VARCHAR,
    department_name VARCHAR,
    index_name VARCHAR,  -- Image URL
    section_name VARCHAR,
    garment_group_name VARCHAR
);

-- Customers
CREATE TABLE customers (
    customer_id VARCHAR PRIMARY KEY,
    age INT,
    postal_code VARCHAR,
    club_member_status VARCHAR,
    fashion_news_frequency VARCHAR,
    Active FLOAT,
    FN FLOAT
);

-- Transactions
CREATE TABLE transactions (
    transaction_id VARCHAR PRIMARY KEY,
    t_dat DATE,
    article_id BIGINT REFERENCES articles(article_id),
    customer_id VARCHAR REFERENCES customers(customer_id),
    price DECIMAL(10,2),
    sales_channel_id INT,
    analysis_column_30 INT,
    analysis_column_90 INT
);
```

### DuckDB Query Patterns

**Product Search:**
```sql
-- Full-text search on product names with pagination
SELECT article_id, prod_name, colour_group_name, department_name, index_name
FROM read_parquet('./hm_with_images/articles/*.parquet')
WHERE LOWER(prod_name) LIKE '%{keyword}%'
  OR LOWER(product_type_name) LIKE '%{keyword}%'
LIMIT ? OFFSET ?;
```

**Sales Aggregation:**
```sql
-- Monthly sales for specific products
SELECT
    DATE_TRUNC('month', t_dat) as month,
    COUNT(*) as transaction_count,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(price) as total_revenue,
    AVG(price) as avg_price
FROM read_parquet('./hm_with_images/transactions/*.parquet')
WHERE article_id IN (?, ?, ...)
GROUP BY month
ORDER BY month;
```

**Performance Characteristics:**
- **Product search:** ~50ms for keyword match across 105K products
- **Sales aggregation:** ~200ms for single product across 31M transactions
- **Multi-product queries:** ~500ms for 10 products with full date range
- **DuckDB caches parquet metadata:** Subsequent queries are faster

---

## LLM Integration Strategy

### Ollama Architecture

**Why Ollama?**
1. **Local Execution:** No API keys, no internet, complete privacy
2. **Model Management:** Easy model download and versioning (`ollama pull llama3.2`)
3. **REST API:** Simple HTTP interface on localhost:11434
4. **Python SDK:** Clean integration with FastAPI
5. **Performance:** Optimized inference, runs on CPU acceptably
6. **Cost:** Free and open-source

### Model Selection: Llama 3.2 (3B)

**Specifications:**
- **Parameters:** 3 billion
- **Quantization:** Q4_K_M (4-bit, medium quality) ~2GB disk
- **Inference Speed:** ~10-20 tokens/sec on modern CPU
- **Context Window:** 8K tokens (sufficient for our use case)
- **Capabilities:** Function calling, structured output, reasoning

**Alternatives Considered:**
| Model | Size | Pros | Cons | Decision |
|-------|------|------|------|----------|
| Llama 3.2 (3B) | 2GB | Fast, good reasoning | Limited context | ✅ **Selected** |
| Mistral 7B | 4GB | Better quality | Slower on CPU | Backup option |
| Phi-3 Mini | 2GB | Very fast | Weaker reasoning | Too limited |
| GPT-4 (API) | N/A | Best quality | Requires internet, costs $ | Violates local requirement |

### Agent Implementation Pattern

**Three Core Functions:**

#### 1. Query Understanding
```python
def parse_search_query_with_attributes(user_query: str) -> dict:
    """
    Convert natural language to structured search parameters with detailed attributes.

    Input: "Nike black jacket"
    Output: {
        "keywords": ["Nike", "black", "jacket"],
        "attributes": {
            "brand": "Nike",
            "type": "jacket",
            "color": "black",
            "style": null,
            "gender": null,
            "department": null
        },
        "filters": {},
        "intent": "product_search"
    }

    The 'attributes' field enables confidence scoring by providing
    structured data for brand, type, and color matching.
    """
    prompt = f"""
    Parse this e-commerce search query into structured filters with attributes.
    Query: "{user_query}"

    Return JSON with:
    - keywords (list): Main search terms
    - attributes (dict): Structured product attributes (brand, type, color, etc.)
    - filters (dict): Price/department constraints
    - intent (string): User's goal (product_search, sales_analysis, etc.)
    """
    response = ollama.chat(model='llama3.2', messages=[...])
    return json.loads(response['message']['content'])
```

**Enhanced for Confidence Scoring:**
The query parser now extracts structured attributes (brand, type, color) which are used by the ConfidenceScorer to calculate relevance scores. This enables intelligent result filtering and ranking based on attribute matching.

#### 2. Tool Orchestration
```python
def orchestrate_tools(parsed_query: dict) -> dict:
    """
    Decide which services to call based on user intent.

    Uses function calling to select appropriate tools:
    - search_products()
    - get_sales_history()
    - forecast_demand()
    - segment_customers()
    """
    tools = [
        {"type": "function", "function": {"name": "search_products", ...}},
        {"type": "function", "function": {"name": "get_sales_history", ...}},
        # ... other tools
    ]

    response = ollama.chat(
        model='llama3.2',
        messages=[{"role": "user", "content": f"Find and analyze: {parsed_query}"}],
        tools=tools
    )

    # Execute selected tools
    results = execute_tool_calls(response['tool_calls'])
    return results
```

#### 3. Insight Generation
```python
def generate_insights(sales_data: pd.DataFrame, products: list) -> str:
    """
    Analyze sales data and generate human-readable insights.

    Input: Sales time series + product metadata
    Output: "Nike running shoes show strong seasonal patterns with
             peak sales in December (45% above average)..."
    """
    context = f"""
    Products: {json.dumps(products)}
    Sales Summary:
    - Total Revenue: ${sales_data['revenue'].sum():,.2f}
    - Transaction Count: {sales_data['count'].sum()}
    - Date Range: {sales_data['date'].min()} to {sales_data['date'].max()}
    - Peak Month: {sales_data.loc[sales_data['revenue'].idxmax(), 'date']}

    Generate 2-3 actionable insights for a business user.
    """

    response = ollama.chat(model='llama3.2', messages=[...])
    return response['message']['content']
```

### Prompt Engineering Guidelines

**Best Practices:**
1. **Structured Output:** Always request JSON for parseable responses
2. **Few-Shot Examples:** Include 1-2 examples in system prompt
3. **Temperature:** Use 0.1-0.3 for deterministic outputs
4. **Token Limits:** Keep prompts under 2K tokens for fast inference
5. **Error Handling:** Validate LLM output with Pydantic schemas

---

## Design Decisions & Tradeoffs

### Decision 1: React vs Next.js

**Decision:** Use **React with Vite**

**Rationale:**
- ✅ MVP doesn't need SSR (server-side rendering)
- ✅ Simpler setup, faster iteration
- ✅ No deployment complexity (static build)
- ✅ Team familiarity with React SPA pattern
- ❌ Trade-off: No SEO optimization (not needed for internal tool)

### Decision 2: Local LLM vs Cloud APIs

**Decision:** Use **Ollama with Llama 3.2**

**Rationale:**
- ✅ Zero API costs (important for demo phase)
- ✅ Complete privacy (no data leaves localhost)
- ✅ No internet dependency (reliable demos)
- ✅ Fast iteration (no rate limits)
- ❌ Trade-off: Lower quality than GPT-4 (acceptable for MVP)
- ❌ Trade-off: Requires local setup (documented in README)

### Decision 3: DuckDB vs PostgreSQL vs Pandas

**Decision:** Use **DuckDB**

**Rationale:**
- ✅ Queries parquet files directly (zero ETL)
- ✅ Fast analytics (OLAP optimized)
- ✅ Embedded (no separate database server)
- ✅ SQL interface (team familiarity)
- ✅ Handles 31M rows easily in-memory
- ❌ Trade-off: Not for transactional workloads (not needed)

**Comparison:**
| Feature | DuckDB | PostgreSQL | Pandas |
|---------|--------|------------|--------|
| Setup Complexity | None (embedded) | High (server install) | None |
| Query Parquet | Native | Extension needed | Manual loading |
| Analytics Speed | Excellent | Good | Variable |
| SQL Interface | Yes | Yes | No (Python API) |
| **Decision** | ✅ Selected | Too heavy | Too low-level |

### Decision 4: Real vs Mocked Features

**Decision:** Real product search + sales viz, Mocked forecast + segmentation

**Rationale:**
- ✅ Core demo flow (search → chart) is end-to-end real
- ✅ Mocked features demonstrate UI/UX without ML complexity
- ✅ Clearly labeled in UI ("Forecasted data based on historical trends")
- ✅ Can upgrade mocked parts to real ML later

**What's REAL:**
1. Natural language product search with LLM parsing
2. Product catalog with 105K real items
3. Historical sales from 31.8M real transactions
4. AI-generated insights from actual data patterns

**What's MOCKED:**
1. Demand forecasting (linear extrapolation from last 3 months)
2. Customer segmentation (rule-based on age/demographics)
3. Advanced analytics (correlation, seasonality scores are simplified)

### Decision 5: Monorepo vs Separate Repos

**Decision:** Use **Monorepo** (single repo with `/frontend` and `/backend`)

**Rationale:**
- ✅ Easier for MVP (single clone, single README)
- ✅ Shared types can be synchronized
- ✅ Atomic commits across full stack
- ✅ Simpler Docker Compose setup
- ❌ Trade-off: Larger repo size (acceptable for demo)

---

## Implementation Phases

### Phase 1: Foundation (Days 1-2)
**Goal:** Setup development environment and data access

**Backend:**
- [ ] Initialize FastAPI project structure
- [ ] Setup DuckDB connection to parquet files
- [ ] Create health check endpoint
- [ ] Test basic parquet queries

**Frontend:**
- [ ] Initialize React + Vite project
- [ ] Setup TailwindCSS
- [ ] Create basic layout (header, search bar, content area)
- [ ] Test API connectivity

**LLM:**
- [ ] Install Ollama
- [ ] Download Llama 3.2 model
- [ ] Test basic chat completion

**Deliverable:** "Hello World" end-to-end (frontend calls backend health check)

### Phase 2: Core User Journey (Days 3-4)
**Goal:** Product search → sales chart working

**Backend:**
- [ ] Implement product search service (DuckDB query on articles)
- [ ] Implement sales analyzer service (DuckDB aggregation on transactions)
- [ ] Create `/api/search` endpoint
- [ ] Integrate Ollama for query parsing

**Frontend:**
- [ ] Build search bar component
- [ ] Build product grid component
- [ ] Build sales chart component (Recharts)
- [ ] Wire up API calls

**Deliverable:** User can search "Nike" → see products → see sales chart

### Phase 3: LLM Insights (Day 5)
**Goal:** AI-generated summaries and insights

**Backend:**
- [ ] Implement insight generation with Ollama
- [ ] Add insights to `/api/search` response
- [ ] Create prompt templates for different insight types

**Frontend:**
- [ ] Build insights panel component
- [ ] Add loading states for LLM processing
- [ ] Display insights with formatting

**Deliverable:** Search results include AI-generated insights

### Phase 4: Mocked Features (Day 6)
**Goal:** Add forecast and segmentation (mocked)

**Backend:**
- [ ] Implement forecaster service (simple linear extrapolation)
- [ ] Implement segmentation service (rule-based)
- [ ] Add forecast/segment data to API responses

**Frontend:**
- [ ] Build forecast widget (chart with projected values)
- [ ] Build customer segment cards
- [ ] Add visual indicators for "mocked data"

**Deliverable:** Full dashboard with all planned features

### Phase 5: Polish & Documentation (Day 7)
**Goal:** Production-ready demo

**Backend:**
- [ ] Add error handling and logging
- [ ] Write API documentation (FastAPI auto-docs)
- [ ] Add data validation (Pydantic schemas)
- [ ] Performance optimization (caching, query optimization)

**Frontend:**
- [ ] UI polish (spacing, colors, typography)
- [ ] Add loading skeletons
- [ ] Responsive design adjustments
- [ ] Error state handling

**Documentation:**
- [ ] Write comprehensive README
- [ ] Record demo video
- [ ] Take screenshots
- [ ] Document mocked vs real features

**Deliverable:** Demoable MVP with documentation

---

## Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| DuckDB performance issues with 31M rows | Low | High | Pre-test queries, add indexing if needed |
| Ollama inference too slow on CPU | Medium | Medium | Use smaller model (Phi-3), or switch to API for demo |
| LLM generates inaccurate insights | Medium | Medium | Add validation layer, fact-check against data |
| Parquet file loading errors | Low | High | Validate files early, add error handling |
| Frontend chart performance with large datasets | Medium | Low | Limit data points to 365 days max, aggregation |

### Project Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Scope creep beyond 2-hour estimate | High | Low | Strict prioritization, clear MVP definition |
| Ollama setup issues on demo machine | Medium | High | Document installation, test on multiple machines |
| Time constraint prevents polish | Medium | Medium | Focus on core flow first, polish is Phase 5 |

### Assumptions

1. **Data Quality:** Parquet files are well-formed and match documented schema
2. **Hardware:** Demo machine has 8GB+ RAM, modern CPU (2020+)
3. **Operating System:** Linux/macOS (primary), Windows (Docker fallback)
4. **Network:** Ollama model download requires one-time internet access (~2GB)
5. **User Expertise:** Demo audience has basic e-commerce domain knowledge

---

## Success Criteria

### Must-Have (P0)
- ✅ User can search products with natural language
- ✅ Sales history charts render correctly with real data
- ✅ AI insights are generated and displayed
- ✅ Application runs locally with single command (docker-compose up)
- ✅ README explains what's real vs mocked

### Should-Have (P1)
- ✅ Forecasting widget displays future predictions
- ✅ Customer segmentation panel shows demographics
- ✅ UI is polished and professional
- ✅ Demo video showcases key features

### Nice-to-Have (P2)
- Product comparison feature
- Advanced filtering (price range, date range)
- Export data to CSV
- Dark mode

---

## Appendix

### Glossary

- **Agentic:** AI system that can autonomously plan and execute tasks using tools
- **DuckDB:** Embedded analytical database optimized for OLAP queries
- **Ollama:** Local LLM runtime for running open-source models
- **Parquet:** Columnar storage format optimized for analytics
- **LLM:** Large Language Model (e.g., Llama, GPT, Claude)

### References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [DuckDB Documentation](https://duckdb.org/docs/)
- [Ollama Documentation](https://ollama.ai/docs)
- [Recharts Documentation](https://recharts.org/)
- [H&M Dataset Information](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations)

---

**Document Control:**
- Last Updated: December 7, 2024
- Review Cycle: Weekly during development
- Approvers: Engineering Lead, Product Manager
- Next Review: Upon Phase 2 completion
