# StockSense AI
### Stock Market Intelligence & Portfolio Analytics Platform

StockSense AI is an institutional-grade, full-stack financial data analytics, econometric forecasting, and portfolio management web application built with **Python 3.13**, **Django 5.0**, **Django REST Framework**, **Pandas**, **Scikit-learn**, **Statsmodels**, **TensorFlow/Keras**, and **Plotly.js**.

Designed as a modern financial terminal, the platform integrates live and historical market data from Indian National Stock Exchange (NSE) equities, US large-caps (NASDAQ & NYSE), and broad-market ETFs alongside econometric time-series forecasting, quantitative indicator modeling, double-entry portfolio accounting, and lexical news sentiment analysis.

---

## Project Overview

* **Project Title:** StockSense AI — Stock Market Intelligence & Portfolio Analytics Platform
* **Target Roles:** Python Full Stack Developer, Django Architect, Machine Learning Engineer, Financial Data Analyst
* **Core Mission:** Eliminate information fragmentation and deliver an institutional-grade trading terminal experience featuring auditable machine learning models with zero data leakage.

### Problem Statement
Retail market participants face severe information fragmentation: price charts, technical indicators, portfolio transactions, media headlines, and predictive analytics are typically scattered across multiple proprietary websites. Furthermore, existing student and commercial trading dashboards frequently suffer from two major flaws:
1. **Superficial "Black-Box" AI:** Fabricated "98% accuracy" claims or random price generators without verifiable mathematical methodology.
2. **Subtle Data Leakage:** Models fit on unpartitioned or future data, producing artificial backtest scores that collapse during live trading.

### Real-World Solution
StockSense AI bridges this gap by unifying multi-market quotes, technical analysis, leakage-free time-series forecasting, live news sentiment, and portfolio accounting into a single production-ready web platform with 22 automated integration tests.

---

## System Architecture Diagram

```text
+---------------------------------------------------------------------------------------------------+
|                                       PRESENTATION TIER                                           |
|  Bootstrap 5 CSS  *  Vanilla JS (ES6+)  *  Lucide SVG Icons  *  Plotly.js Hardware-Accelerated Charts |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                        HTTP / JSON (REST API)
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                   DJANGO APPLICATION TIER                                         |
|  URL Routing  *  EmailOrUsernameModelBackend  *  SessionMiddleware  *  CSRF / Security Middleware  |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                   DOMAIN BUSINESS LOGIC LAYER                                     |
|  * MarketDataService          : Live Quotes, In-Memory Caching (LocMemCache), Trading Hours       |
|  * TechnicalIndicatorService  : SMA, EMA, RSI (Wilder's), MACD, Bollinger Bands, ATR, Volatility  |
|  * ForecastingService         : Linear, Random Forest, ARIMA(2,1,1), Deep LSTM, Hybrid Ensemble   |
|  * TimeSeriesDataPipeline     : Chronological 80/20 Partitioning, Zero-Leakage MinMax Scaling     |
|  * NewsSentimentService       : Google News RSS / NewsAPI Ingestion, VADER Polarity Scoring       |
|  * PortfolioAnalyticsService  : Transaction Ledger, FIFO Cost Basis, Overselling Prevention       |
|  * WatchlistService           : Custom Watchlists, Toggle Tracking                                |
|  * PriceAlertService          : Threshold Breaches, Alert Evaluation                              |
|  * ResearchAssistantService   : Tool-Grounded Copilot via Google Gemini with Deterministic Engine |
+---------------------------------------------------------------------------------------------------+
            |                                     |                                    |
            v                                     v                                    v
+-----------------------+             +-----------------------+             +-----------------------+
|   PERSISTENCE TIER    |             |  EXTERNAL DATA FEEDS  |             |      CACHING LAYER    |
|  SQLite 3 (Dev/Test)  |             |  Yahoo Finance (NSE)  |             |  Django LocMemCache   |
|  PostgreSQL (Prod)    |             |  Google News RSS      |             |  Quotes: 60s TTL      |
|  Django ORM & Models  |             |  NewsAPI.org (Opt)    |             |  History: 300s TTL    |
|  django_session       |             |  Google Gemini (AI)   |             |  News: 300s TTL       |
+-----------------------+             +-----------------------+             +-----------------------+
```

---

## Complete Project Flow & Data Lifecycle

The application executes through a deterministic, end-to-end data lifecycle:

```text
User Request
    │
    ▼
Frontend Browser (UI Event / Fetch API)
    │
    ▼
Django Backend (URL Routing, Auth Middleware, CSRF Verification)
    │
    ▼
Service Layer & External Feeds (Yahoo Finance, Google News RSS, LocMemCache)
    │
    ▼
Data Processing & Modeling (Pandas Indicators, VADER Sentiment, ML Pipeline)
    │
    ▼
Database Persistence (SQLite/PostgreSQL Models via Django ORM)
    │
    ▼
Structured JSON Response / Server-Rendered HTML Template
    │
    ▼
Frontend Render (Plotly.js Interactive Candlestick Charts & Metric Cards)
```

1. **User Signs In:** Submits credentials via `/login/`. Custom `EmailOrUsernameModelBackend` checks username or email, verifies salted PBKDF2-SHA256 password hash, assigns an HTTP-only `stocksense_sessionid` cookie, and redirects to `/dashboard/`.
2. **Search & Select Stock:** User searches for a symbol (e.g., `TCS.NS`). `/api/stocks/?q=TCS` queries database records in <10ms.
3. **Market Data Fetch & Cache:** `MarketDataService` checks `LocMemCache`. On a cache miss, it calls Yahoo Finance for 2-year daily OHLCV candles, updates local database records, and caches the frame for 300s.
4. **Technical Indicator Processing:** `TechnicalIndicatorService` computes vectorized 20/50/200 SMAs, 12/26/50 EMAs, 14-day RSI (Wilder's smoothing `alpha=1/14`), MACD (12, 26, 9), and 2-standard-deviation Bollinger Bands.
5. **Interactive Chart Display:** Timestamps and OHLC arrays are rendered by Plotly.js on client side with zoom, pan, and volume subplots.
6. **Machine Learning Forecasting:** Selecting a model and horizon triggers `/api/predictions/<symbol>/`. `TimeSeriesDataPipeline` splits data chronologically (80% train / 20% test), fits scalers strictly on training data, executes recursive projections, and reports MAE, RMSE, and Directional Accuracy.
7. **News Sentiment Ingestion:** `NewsSentimentService` queries Google News Financial RSS, extracts verified headlines and descriptions, runs VADER lexical sentiment analysis, upserts records into `NewsArticle`, and aggregates positive/neutral/negative consensus.
8. **Portfolio & Ledger:** User submits trades. `PortfolioAnalyticsService` validates positive shares, prevents overselling open balances, and updates FIFO cost basis and realized profit/loss.

---

## Key Features

### 1. Market Intelligence & Benchmark Overview
- Real-time benchmark index tracking for **NIFTY 50**, **BSE SENSEX**, **S&P 500**, and **NASDAQ Composite**.
- Automated market status detection (trading hours beacon for Indian IST and US EST sessions).
- Market movers scanner identifying top gainers, losers, and most active equities.
- Caching layer (`LocMemCache`) preventing API rate-limiting and provider throttling.

### 2. Deep Equity Workspace & Interactive Charting
- High-performance **Plotly.js** interactive financial charts (Candlestick and Line view with Volume subplots).
- Timeframe filters: 1 Month, 3 Months, 6 Months, 1 Year, 5 Years.
- Technical Indicator Overlays:
  - Simple Moving Averages: **SMA 20**, **SMA 50**, **SMA 200**
  - Exponential Moving Averages: **EMA 12**, **EMA 26**, **EMA 50**
  - Relative Strength Index: **RSI (14)** with Wilder's exponential smoothing and overbought/oversold bands
  - Moving Average Convergence Divergence: **MACD (12, 26, 9)** line, signal line, and histogram
  - **Bollinger Bands (20-day, 2 standard deviations)** with volatility bandwidth
  - **Average True Range (ATR 14)**
  - Annualized rolling historical volatility (21-day log returns)
- Plain-English educational interpretations and explicit risk disclaimers for every indicator.

### 3. Database-Backed Portfolio Accounting
- Persistent relational transaction ledger (`BUY` and `SELL` executions).
- Accurate position accounting based on **average cost basis**.
- Realized profit/loss calculation on executed sales.
- Live mark-to-market unrealized profit/loss valuation and return percentages.
- Strict server-side validation preventing short-selling or overselling shares.
- Dual-currency support: Indian holdings in **INR (₹)** and US holdings in **USD ($)** with exchange rate translation.
- Asset diversification donut charts by equity position and industry sector.

### 4. Machine Learning & Econometric Forecasting
- Structured, leakage-free time-series pipeline:
  - Chronological 80/20 train-test splitting.
  - Scalers fit **exclusively on the training partition** to eliminate look-ahead bias.
  - Multi-step forward horizon projections (7, 14, 30 trading days).
- Supported Model Architectures:
  1. **Linear Regression Baseline** (Autoregressive lag features)
  2. **Random Forest Regressor** (Non-linear decision trees with volatility features)
  3. **ARIMA (2, 1, 1)** (Autoregressive Integrated Moving Average on log returns)
  4. **LSTM Deep Neural Network** (TensorFlow/Keras with Dropout and Early Stopping)
  5. **Hybrid LSTM-ARIMA Ensemble** (Optimized blend minimizing validation MSE)
- Honest out-of-sample evaluation metrics: **MAE**, **RMSE**, and **Directional Accuracy (%)** on actual held-out test data.
- Side-by-side model comparison leaderboard ranking architectures by test error.

### 5. Financial Media & Sentiment NLP
- Multi-tier live news ingestion: Google News Financial RSS as default, NewsAPI.org as optional, and SQLite as offline fallback.
- Natural Language Processing via **VADER Sentiment Engine**:
  - Positive sentiment ($\ge +0.05$): Bullish market consensus
  - Neutral sentiment ($-0.05$ to $+0.05$): Factual reports & disclosures
  - Negative sentiment ($\le -0.05$): Bearish or cautionary news
- Aggregate distribution metrics: Positive %, Neutral %, Negative %, and Net Compound Sentiment score.
- Direct links to original publishers and clean article summaries.
- Graceful handling of zero-news edge cases without crashing or showing blank pages.

### 6. Grounded AI Financial Research Assistant
- Tool-grounded retrieval architecture querying live platform stock quotes, technical indicator computations, and authenticated portfolio holdings.
- Synthesis powered by **Google Gemini API** (`gemini-2.5-flash` via `google.genai` SDK) using environment variable configuration.
- Deterministic fallback research engine ensuring full functionality without external API keys.
- Strictly avoids hallucinated stock prices or fake returns.

---

## Technologies Used

| Layer | Technologies |
|---|---|
| **Programming Language** | Python 3.13 |
| **Web Framework** | Django 5.0, Django REST Framework 3.14+ |
| **Database** | SQLite 3 (Development/Testing), PostgreSQL (Production ready) |
| **Market Data Ingestion** | yfinance 0.2.35+, Google News Financial RSS, NewsAPI.org |
| **Data Manipulation** | Pandas 2.1+, NumPy 1.26+ |
| **Machine Learning** | Scikit-learn 1.3+, Statsmodels 0.14+, TensorFlow/Keras 2.15+ |
| **Natural Language Processing** | vaderSentiment 3.3.2 |
| **AI Synthesis** | Google Gemini API (`google.genai` SDK) with deterministic quantitative fallback |
| **Frontend & UI** | HTML5, CSS3 Custom Properties, Vanilla JavaScript (ES6+), Bootstrap 5 |
| **Charting Engine** | Plotly.js 2.35+ (Candlesticks, Indicators, Subplots) |
| **Icons & Assets** | Lucide Icons (SVG) |
| **Production Serving** | WhiteNoise 6.6+, Gunicorn 21.2+ |

---

## Directory & Folder Structure

```text
StockSense AI/
│
├── config/                     # Django master project configuration
│   ├── settings.py             # Project settings, middleware, caches, DRF config
│   ├── urls.py                 # Master URL routing table
│   ├── wsgi.py                 # WSGI production server entry point
│   └── asgi.py                 # ASGI entry point for async operations
│
├── apps/                       # Modular Django domain applications
│   ├── accounts/               # Custom user model, EmailOrUsernameModelBackend, views
│   ├── market/                 # Stock quotes, historical prices, screener, MarketDataService
│   ├── portfolio/              # Portfolio ledger, Transaction model, PortfolioAnalyticsService
│   ├── watchlists/             # Watchlist models, dynamic toggle, PriceAlertService
│   ├── analytics/              # TechnicalIndicatorService (SMA, EMA, RSI, MACD, Bollinger)
│   ├── predictions/            # ForecastingService, TimeSeriesDataPipeline, ML models
│   ├── news/                   # NewsArticle model, NewsSentimentService, VADER NLP
│   └── assistant/              # ResearchAssistantService, Google Gemini copilot
│
├── templates/                  # Server-rendered HTML templates
│   ├── base.html               # Master layout shell (Sidebar, Navbar, Flash messages)
│   ├── components/             # Reusable navigation components (sidebar.html, navbar.html)
│   ├── accounts/               # login.html, register.html, profile.html
│   ├── market/                 # dashboard.html, explorer.html, screener.html, compare.html
│   ├── portfolio/              # portfolio.html, transactions.html
│   ├── watchlists/             # watchlists.html, alerts.html
│   ├── predictions/            # predictions.html
│   └── news/                   # news.html
│
├── static/                     # Static CSS stylesheets and JavaScript assets
│   ├── css/stocksense.css      # Dark-mode financial terminal styling
│   └── js/
│       ├── stocksense.js       # Core DOM interactions, CSRF helpers, toast alerts
│       └── charts.js           # Plotly.js candlestick and financial charting engine
│
├── tests/                      # Automated test suite
│   └── test_platform.py        # 22 integration tests (Auth, Market, ML, News, Portfolio)
│
├── ml_models/                  # Serialized ML model artifacts and weights
├── db.sqlite3                  # Local SQLite database with demo trader account
├── requirements.txt            # Pinned Python package dependencies
├── .env.example                # Example environment variables template
└── README.md                   # Complete platform documentation
```

---

## Installation & Setup Guide

### 1. Prerequisites
Ensure you have **Python 3.10+** (Python 3.13 recommended) and **Git** installed on your system.

### 2. Clone the Repository
```bash
git clone <repository-url>
cd "Final year project"
```

### 3. Create and Activate a Virtual Environment
* **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy the `.env.example` file to create your `.env`:
* **Windows (PowerShell):**
  ```powershell
  Copy-Item .env.example .env
  ```
* **macOS / Linux:**
  ```bash
  cp .env.example .env
  ```
*(Optional: Add your `GEMINI_API_KEY` or `NEWS_API_KEY` in `.env`. By default, Google News RSS and deterministic AI work out of the box with zero keys).*

### 6. Apply Database Migrations & Seed Universe
```bash
python manage.py migrate
python manage.py seed_stocks
```

### 7. Run Automated Tests
Verify that all subsystems pass cleanly:
```bash
python manage.py test tests.test_platform
```
*(Expected: `Ran 22 tests in ...s - OK`)*

### 8. Start the Development Server
```bash
python manage.py runserver 8000
```
Open your browser and navigate to: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## Default Demo Credentials

For immediate evaluation, a pre-configured demo account is available:
* **Username:** `demo_trader`
* **Password:** `StockSense@2026`
*(You can also click the **"Use Demo Credentials (demo_trader)"** button on the login page).*

---

## How to Test Each Feature

1. **Authentication:**
   - Go to `http://127.0.0.1:8000/login/`. Click "Use Demo Credentials" and submit.
   - Verify you are redirected to the Dashboard and session cookie `stocksense_sessionid` is assigned.
2. **Stock Explorer & Interactive Charts:**
   - Navigate to `/stocks/TCS.NS/`.
   - Verify Plotly candlestick chart renders with green/red candles, volume subplots, and technical overlays.
   - Switch timeframes (1M, 6M, 1Y) and toggle indicators (RSI, MACD, Bollinger Bands).
3. **ML Forecasting:**
   - Navigate to `/predictions/?symbol=TCS.NS`.
   - Select model (e.g., `Hybrid LSTM-ARIMA Ensemble`) and horizon (`30 Trading Days`).
   - Click "Execute Model". Verify forecast projection curve renders and evaluation metrics (MAE, RMSE, Directional Accuracy) populate.
4. **News Sentiment Analysis:**
   - Navigate to `/news/?symbol=TCS.NS`.
   - Verify 25 verified articles render with source publishers, UTC timestamps, VADER polarity badges, and summaries.
   - Click quick ticker chips (`AAPL`, `RELIANCE.NS`, `Market Macro`) to verify instant filtering.
5. **Portfolio & Transactions:**
   - Navigate to `/portfolio/transactions/`. Record a BUY transaction (e.g., 5 shares of TCS.NS at Rs 3,400).
   - Verify portfolio summary updates in `/portfolio/` with mark-to-market valuation.
   - Attempt to sell 100 shares. Verify the system raises a validation error blocking the trade.

---

## Common Errors & Troubleshooting

| Error | Root Cause | Solution |
|---|---|---|
| `SyntaxError: Unexpected token '<'` on ML page | Endpoint returned HTML error instead of JSON | Fixed by ensuring prediction views return strict `JsonResponse` and frontend checks `response.ok` before parsing. |
| `curl: (56) Connection closed abruptly` on News | Yahoo Finance blocked private API connection on Windows | Replaced with Google News Financial RSS multi-tier pipeline with SQLite caching. |
| `Invalid username/email or password` with special chars | Default auth backend treated `@` strictly as email | Resolved via `EmailOrUsernameModelBackend` supporting dual Q-object lookups. |
| `No module named 'config'` | Python path root not set | Run commands from the project root directory or set `DJANGO_SETTINGS_MODULE=config.settings`. |
| `Database locked` in SQLite | Multiple processes writing simultaneously | Atomic transaction blocks and WAL mode configured; use PostgreSQL for production. |

---

## Future Improvements

1. **Live Order Book WebSockets:** Integrate Django Channels with Redis to stream sub-second tick-level order book depth.
2. **Broker API Paper Trading:** Connect to Zerodha Kite Connect or Alpaca API for automated simulated execution.
3. **FinBERT Sentiment Fine-Tuning:** Deploy a domain-specific BERT Transformer model fine-tuned on Indian business filings.
4. **Portfolio Optimization:** Implement Black-Litterman and Markowitz Efficient Frontier models for automated risk-weighted asset rebalancing.

---

## Disclaimers & Regulatory Notice
All technical indicators, mathematical metrics, and machine learning forecasts provided by StockSense AI are for **educational and research purposes only**. They do not constitute financial advice, investment recommendations, or guaranteed price targets.
