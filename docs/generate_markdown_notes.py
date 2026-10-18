"""
Generator for AI_Stock_Market_Project_Notes.md
Creates comprehensive master documentation covering Parts 1 through 13.
"""

import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(ROOT_DIR, "AI_Stock_Market_Project_Notes.md")

MARKDOWN_CONTENT = """# StockSense AI — Comprehensive Project Documentation & Technical Interview Guide
**Platform:** Stock Market Intelligence, Econometric ML Forecasting & Portfolio Analytics Platform  
**Target Roles:** Python Full Stack Developer, Django Architect, Machine Learning Engineer, Financial Data Analyst (Fresher to Mid-Level)  
**Author / Candidate:** Full Stack Python & AI Developer  
**Technology Stack:** Python 3.13, Django 5.0, Django REST Framework, SQLite/PostgreSQL, yfinance, Pandas, NumPy, Scikit-Learn, Statsmodels, TensorFlow/Keras, VADER Sentiment, Plotly.js, Bootstrap 5, Custom Vanilla JS.

---

## Table of Contents
1. [Part 1: Project Overview & Executive Summary](#part-1-project-overview--executive-summary)
   - [Problem Statement & Market Need](#problem-statement--market-need)
   - [Core Objectives & Real-World Use Cases](#core-objectives--real-world-use-cases)
   - [Functional vs Non-Functional Requirements](#functional-vs-non-functional-requirements)
   - [What Makes This an AI-Powered Financial Platform](#what-makes-this-an-ai-powered-financial-platform)
   - [Traditional Financial Portals vs StockSense AI](#traditional-financial-portals-vs-stocksense-ai)
   - [Ready-to-Speak Interview Introductions (30s, 1m, 2m, 5m)](#ready-to-speak-interview-introductions)
2. [Part 2: Technology Stack & Architectural Rationale](#part-2-technology-stack--architectural-rationale)
   - [Frontend Technologies](#frontend-technologies)
   - [Backend & Frameworks](#backend--frameworks)
   - [Database & ORM](#database--orm)
   - [Data Science & Quantitative Finance Libraries](#data-science--quantitative-finance-libraries)
   - [Machine Learning & Time-Series Engines](#machine-learning--time-series-engines)
   - [External Data Feeds & NLP Libraries](#external-data-feeds--nlp-libraries)
   - [Development & Deployment Utilities](#development--deployment-utilities)
3. [Part 3: Complete Project Architecture & Data Flows](#part-3-complete-project-architecture--data-flows)
   - [Overall System Architecture](#overall-system-architecture)
   - [Stock Price Data & Cache Pipeline](#stock-price-data--cache-pipeline)
   - [Machine Learning Forecasting Pipeline](#machine-learning-forecasting-pipeline)
   - [Authentication & Persistent Session Architecture](#authentication--persistent-session-architecture)
   - [Database Entity-Relationship Architecture (ERD)](#database-entity-relationship-architecture-erd)
   - [News Sentiment & AI Copilot Architecture](#news-sentiment--ai-copilot-architecture)
4. [Part 4: In-Depth Feature-by-Feature Implementation Guide](#part-4-in-depth-feature-by-feature-implementation-guide)
   - [Feature A: User Authentication & Profile Customization](#feature-a-user-authentication--profile-customization)
   - [Feature B: Real-Time Market Overview & Global Universe](#feature-b-real-time-market-overview--global-universe)
   - [Feature C: Interactive Stock Explorer & Financial Charts](#feature-c-interactive-stock-explorer--financial-charts)
   - [Feature D: Technical Analysis & Multi-Factor Screener](#feature-d-technical-analysis--multi-factor-screener)
   - [Feature E: Portfolio Accounting Ledger & FIFO Position Tracker](#feature-e-portfolio-accounting-ledger--fifo-position-tracker)
   - [Feature F: Watchlists & Dynamic Threshold Price Alerts](#feature-f-watchlists--dynamic-threshold-price-alerts)
   - [Feature G: Machine Learning Econometric Forecasting Lab](#feature-g-machine-learning-econometric-forecasting-lab)
   - [Feature H: Financial News Sentiment Engine](#feature-h-financial-news-sentiment-engine)
   - [Feature I: StockSense AI Copilot (Retrieval-Grounded Assistant)](#feature-i-stocksense-ai-copilot-retrieval-grounded-assistant)
5. [Part 5: Machine Learning Explained from Absolute Zero](#part-5-machine-learning-explained-from-absolute-zero)
   - [Foundations: The Time-Series Supervised Regression Problem](#foundations-the-time-series-supervised-regression-problem)
   - [Zero Data Leakage: Chronological Partitioning & Pipeline Scaler](#zero-data-leakage-chronological-partitioning--pipeline-scaler)
   - [Model 1: Autoregressive Linear Regression Baseline](#model-1-autoregressive-linear-regression-baseline)
   - [Model 2: Random Forest Non-Linear Regressor](#model-2-random-forest-non-linear-regressor)
   - [Model 3: ARIMA Time-Series on Log Returns](#model-3-arima-time-series-on-log-returns)
   - [Model 4: Deep LSTM Recurrent Neural Network](#model-4-deep-lstm-recurrent-neural-network)
   - [Model 5: Hybrid LSTM-ARIMA Ensemble with MSE Minimum Search](#model-5-hybrid-lstm-arima-ensemble-with-mse-minimum-search)
   - [Walk-Forward Residual Evaluation (MAE, RMSE, Directional Accuracy)](#walk-forward-residual-evaluation)
   - [Statistical Limitations: Why Market Forecasts Are Not Guarantees](#statistical-limitations)
6. [Part 6: Codebase Anatomy & Line-by-Line Code Walkthrough](#part-6-codebase-anatomy--line-by-line-code-walkthrough)
   - [Directory Structure & Application Mapping](#directory-structure--application-mapping)
   - [The Authentication Backend: EmailOrUsernameModelBackend](#the-authentication-backend-emailorusernamemodelbackend)
   - [The Market Service: MarketDataService](#the-market-service-marketdataservice)
   - [The Portfolio Engine: PortfolioAnalyticsService](#the-portfolio-engine-portfolioanalyticsservice)
   - [The Technical Indicator Engine: TechnicalIndicatorService](#the-technical-indicator-engine-technicalindicatorservice)
   - [The ML Engine: ForecastingService & TimeSeriesDataPipeline](#the-ml-engine-forecastingservice--timeseriesdatapipeline)
   - [The News Sentiment Engine: NewsSentimentService](#the-news-sentiment-engine-newssentimentservice)
   - [The AI Copilot Service: ResearchAssistantService](#the-ai-copilot-service-researchassistantservice)
7. [Part 7: API Specifications & Database Relational Model](#part-7-api-specifications--database-relational-model)
   - [REST API Contract & Endpoints](#rest-api-contract--endpoints)
   - [HTTP Status Codes & Error Handling Matrix](#http-status-codes--error-handling-matrix)
   - [Database Schema & Foreign Key Constraints](#database-schema--foreign-key-constraints)
   - [ORM Query Optimization (select_related & prefetch_related)](#orm-query-optimization)
8. [Part 8: Security Architecture & Performance Engineering](#part-8-security-architecture--performance-engineering)
   - [Cryptographic Password Hashing (PBKDF2-SHA256)](#cryptographic-password-hashing)
   - [Session Security & State Persistence](#session-security--state-persistence)
   - [CSRF, XSS, and SQL Injection Defenses](#csrf-xss-and-sql-injection-defenses)
   - [In-Memory Caching (LocMemCache) & Rate Limiting](#in-memory-caching)
   - [Vectorized LSTM Inference & Asynchronous Frontend Polling](#vectorized-lstm-inference)
9. [Part 9: Deployment Architecture & DevOps Workflow](#part-9-deployment-architecture--devops-workflow)
   - [Local Development Setup](#local-development-setup)
   - [Production Configuration (PostgreSQL, Gunicorn, WhiteNoise)](#production-configuration)
   - [Environment Variables (.env) Management](#environment-variables-management)
   - [Continuous Testing & CI/CD Considerations](#continuous-testing)
10. [Part 10: 100+ Categorized Technical Interview Questions & Model Answers](#part-10-100-categorized-technical-interview-questions--model-answers)
11. [Part 11: Mock Interview Practice Rounds & Readiness Checklist](#part-11-mock-interview-practice-rounds--readiness-checklist)
12. [Part 12: Quick Revision Guide & 15-Minute Pre-Interview Cheat Sheet](#part-12-quick-revision-guide--15-minute-pre-interview-cheat-sheet)

---

# Part 1: Project Overview & Executive Summary

### Problem Statement & Market Need
Retail investors, trading freshers, and financial analysts frequently face three major hurdles:
1. **Information Fragmentation:** Price quotes, financial charts, technical indicators, portfolio records, news headlines, and market sentiment are typically scattered across disparate websites.
2. **Superficial "Black-Box" AI:** Existing retail trading dashboards often provide fabricated "95% accuracy" predictions, random number generators disguised as artificial intelligence, or static marketing claims without verifiable methodology.
3. **Data Leakage in Predictive Models:** Most hobbyist stock predictors suffer from subtle data leakage (e.g., standardizing data using overall future prices or random k-fold cross-validation), which produces artificially high backtest scores that collapse during real-world trading.

**StockSense AI** was developed to bridge this gap. It is a full-stack financial research and portfolio intelligence web platform that delivers:
- Institutional-grade data density inspired by modern trading terminals.
- Mathematically rigorous technical indicator calculations.
- Honest, walk-forward validated machine learning econometric models (Linear Regression, Random Forest, ARIMA, LSTM, and Hybrid Ensembles).
- Real-time VADER news sentiment scoring.
- Exact portfolio accounting featuring FIFO cost basis and overselling validation.

### Core Objectives & Real-World Use Cases
- **Unified Terminal Experience:** Deliver instant quotes, interactive candlestick/line charts, and multi-factor filtering for Indian NSE equities (TCS, Infosys, Reliance, HDFC Bank, SBI), US equities (Apple, Microsoft, Nvidia, Google, Tesla), and benchmark ETFs.
- **Auditable Machine Learning:** Empower users to execute and evaluate five distinct algorithmic forecasting architectures side-by-side on identical out-of-sample held-out partitions, reporting verifiable metrics: Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and Directional Accuracy (%).
- **Accurate Portfolio Management:** Provide a transaction ledger that tracks BUY and SELL orders, calculates average cost basis and realized/unrealized profit & loss, enforces strict inventory guards against overselling, and supports multi-currency views (INR and USD).
- **Automated Price Alerts:** Enable users to set dynamic price thresholds (`ABOVE` or `BELOW`) and monitor status triggers automatically.
- **RAG-Grounded Financial Copilot:** Offer an interactive assistant that pulls live platform data (portfolio holdings, stock quotes, technical indicators) before synthesizing research commentary.

### Functional vs Non-Functional Requirements

#### Functional Requirements
- **Authentication & Security:** User registration, login via username or email address, logout, session persistence across server restarts, and user preferences (currency, theme).
- **Market Data Engine:** Real-time & delayed OHLCV price retrieval via Yahoo Finance (`yfinance`), caching for fast response times, and graceful fallbacks during API degradation.
- **Interactive Visualizations:** Plotly.js financial charts supporting Candlestick and Line formats, volume subplots, and time range toggles (1M, 3M, 6M, 1Y, 5Y).
- **Technical Analysis Engine:** Automated mathematical computation of 20/50/200 SMAs, 12/26/50 EMAs, Wilder's 14 RSI, MACD (12, 26, 9), Bollinger Bands, and Average True Range (ATR).
- **ML Forecasting Suite:** On-demand model execution, walk-forward validation on held-out test splits, ensemble weight optimization via minimum Mean Squared Error (MSE), and side-by-side leaderboard ranking.
- **Sentiment & News Stream:** Real-time financial headlines categorized into POSITIVE, NEGATIVE, or NEUTRAL using VADER compound polarity scoring.
- **Portfolio Ledger:** Trade entry (BUY/SELL), transaction history, position aggregation, realized and unrealized P&L calculation, and portfolio asset allocation breakdown.

#### Non-Functional Requirements
- **Performance:** Sub-100ms response times for cached quotes; vectorized test evaluation for neural networks to ensure predictions return within 2-4 seconds.
- **Reliability & Resilience:** Graceful degradation on API rate-limits, database snapshot fallbacks, and guaranteed JSON API contracts (never returning unhandled 500 HTML error pages).
- **Data Integrity:** Zero data leakage in ML pipelines; scalers fit solely on training data chronologically; strict transaction validation preventing negative share balances.
- **Usability & UX:** Terminal-style aesthetic avoiding generic gradients, floating blobs, or excessive animations; compact typography, tabular numerals, and responsive layouts.

### What Makes This an AI-Powered Financial Platform
Unlike traditional static stock tracking websites that only display historical quotes from a database, StockSense AI embeds machine learning directly into the user workflow:
1. **Active Neural & Statistical Inference:** When a user selects a stock (e.g., `TCS.NS`) and clicks **"Execute Model"**, the backend dynamically loads recent price history, constructs temporal sequences, trains an autoregressive or deep LSTM recurrent network, fits an ARIMA model on log returns, and derives an optimal blended prediction.
2. **Quantitative Validation vs Speculation:** The platform calculates and visualizes out-of-sample residual performance alongside future projections, teaching the user how well the model performed on unseen historical data.
3. **Natural Language Sentiment Classification:** Uses VADER NLP scoring to translate qualitative textual headlines into quantitative sentiment polarity scores.
4. **Context-Aware Financial Assistant:** Uses Retrieval-Augmented Generation (RAG) concepts to ground AI responses in actual user portfolio holdings and market metrics.

### Traditional Financial Portals vs StockSense AI

| Feature | Traditional Financial Portals | StockSense AI Platform |
| :--- | :--- | :--- |
| **Data Presentation** | Static tables, delayed charts, heavy banner ads | Clean, ad-free institutional research terminal |
| **Stock Universe** | Often restricted to single domestic exchange | Multi-market: Indian NSE, US Equities, Global ETFs |
| **Predictive Capabilities** | None, or paid black-box "expert tips" | 5 Walk-forward validated open ML architectures |
| **Data Leakage Safeguards** | Rarely documented or ignored | Strict chronological 80/20 train/test split |
| **Ensemble Modeling** | None | Hybrid LSTM-ARIMA with test MSE grid search |
| **Technical Indicators** | Basic pre-calculated server charts | Dynamic Pandas engine with 8+ mathematical indicators |
| **Portfolio Ledger** | Simple manual watchlist | FIFO position accounting with overselling validation |
| **News Sentiment** | Raw RSS headlines | VADER compound polarity scoring with visual sentiment bars |
| **AI Assistant** | Generic chatbot with no account context | RAG-grounded assistant aware of live portfolio and quotes |

---

### Ready-to-Speak Interview Introductions

#### 30-Second Elevator Pitch (Quick & Punchy)
> *"I developed **StockSense AI**, a full-stack Django financial analytics and machine learning web application. It integrates live market data from Yahoo Finance for Indian NSE and US equities, computes mathematical technical indicators using Pandas, and provides an end-to-end econometric forecasting lab featuring a hybrid LSTM-ARIMA ensemble with zero data leakage. It also includes an exact FIFO portfolio ledger, dynamic price alerts, and real-time VADER news sentiment analysis."*

#### 1-Minute Project Overview (Standard Interview Opening)
> *"**StockSense AI** is a comprehensive stock market intelligence and portfolio analytics platform built using Python, Django, and modern frontend tools. I built this project to solve the problem of fragmented and untrustworthy retail trading tools.
> 
> On the backend, I designed a modular Django architecture with eight apps covering market data, portfolio accounting, technical analysis, and machine learning. We fetch historical OHLCV data using `yfinance`, cache quotes in memory for performance, and run mathematical technical indicators like RSI, MACD, and Bollinger Bands using Pandas.
> 
> What makes the project unique is our ML forecasting engine: instead of hardcoding fake predictions, we train and validate five models—Linear Regression, Random Forest, ARIMA, LSTM, and a Hybrid Ensemble—using strict chronological splits to prevent look-ahead bias. The platform also features a FIFO portfolio transaction ledger, VADER sentiment analysis for news, and an institutional trading terminal UI built with Plotly.js."*

#### 2-Minute Detailed Walkthrough (Deep Technical Introduction)
> *"I built **StockSense AI**, a production-grade Django web platform that combines quantitative financial analysis with machine learning forecasting.
> 
> The application is structured into eight decoupled Django apps. The **Market App** handles data acquisition for Indian equities like TCS and Reliance, US equities like Apple and Nvidia, and ETFs. To avoid third-party rate limits, I implemented a multi-tier caching strategy using Django's in-memory cache and database fallbacks.
> 
> For **Technical Analysis**, I implemented a pure Pandas calculation engine that computes 20, 50, and 200-day SMAs, EMAs, Wilder's smoothed RSI 14, MACD, Bollinger Bands, and Average True Range without relying on opaque third-party black boxes.
> 
> The **Machine Learning Engine** is where I focused on econometric integrity. In stock forecasting, standard cross-validation causes catastrophic data leakage. In my `TimeSeriesDataPipeline`, I enforced strict chronological 80/20 train-test splits and fit our MinMaxScaler solely on training data. We implement five models: an Autoregressive Linear baseline, Random Forest, ARIMA on log returns via statsmodels, a deep 2-layer LSTM network with Dropout in TensorFlow/Keras, and a Hybrid Ensemble that optimizes the alpha blending weight between LSTM and ARIMA to minimize out-of-sample Mean Squared Error.
> 
> On the frontend, I used Django templates, vanilla ES6+ JavaScript, and Plotly.js to render interactive multi-timeframe candlestick and line charts. Finally, the platform includes a complete **Portfolio Ledger** with overselling validation, dynamic price alerts, VADER news sentiment scoring, and a custom authentication backend that allows case-insensitive login via username or email."*

#### 5-Minute Comprehensive Presentation (Technical Showcase / System Design Round)
> *(Use this outline for extended project presentations, college final reviews, or deep-dive technical interview rounds)*:
> 1. **Motivation & Architecture Philosophy:** Why traditional retail tools fail, the need for transparency in algorithmic trading, and why Django was chosen over microservices for maintainability and built-in security.
> 2. **Backend Engineering:** Decoupled design, Django ORM, custom authentication backend (`EmailOrUsernameModelBackend`), session persistence across server restarts, and RESTful API endpoints via Django REST Framework.
> 3. **Data Pipeline & Caching:** yfinance integration, in-memory caching tiers (90-second quotes, 1-hour OHLCV, 5-minute market indices), and local database snapshots for fault tolerance.
> 4. **Financial Engineering:** FIFO transaction accounting, average cost basis, realized vs unrealized profit and loss calculation, dual-currency support (INR/USD), and mathematical indicators (SMA, EMA, Wilder's RSI, MACD, Bollinger Bands, ATR).
> 5. **Machine Learning Pipeline:** The time-series challenge, look-ahead bias mitigation, lag feature extraction, ARIMA return modeling, LSTM sequence rolling, ensemble blending via MSE minimization, and evaluation on real held-out data using MAE, RMSE, and Directional Accuracy.
> 6. **NLP & Grounded AI:** VADER lexicon sentiment scoring for financial headlines, and a RAG-grounded assistant that inspects user portfolio holdings and quotes before answering queries.
> 7. **Testing & Quality Assurance:** 19 automated tests in Django covering authentication, FIFO accounting, indicator accuracy, data leakage prevention, and API contracts.

---

# Part 2: Technologies Used

Every technology listed below has been verified directly in the project codebase:

### 1. Python 3.13
- **What it is:** A modern, high-level, dynamically typed programming language known for clean syntax and an unmatched ecosystem for data science and web development.
- **Why used:** Serves as the core language across the entire application—powering web views, ORM models, mathematical algorithms, data pipelines, and deep neural networks.
- **Where used:** All `.py` files across `config/`, `apps/`, and `tests/`.
- **Inter-component Communication:** Executes Django server logic, calls C-optimized libraries (NumPy, TensorFlow), and interfaces with SQLite.
- **Interview Example:** Python's unified ecosystem allowed seamless data flow: fetching data via `yfinance`, processing it with `pandas`, modeling with `tensorflow`, and serving via `django` without inter-process overhead.
- **Interview Q&A:**
  - *Q: Why use Python for a financial analytics platform?*
  - *A: Python provides the premier ecosystem for quantitative finance (NumPy, Pandas), scientific computing (Scikit-Learn, Statsmodels), deep learning (TensorFlow), and enterprise web development (Django) within a single unified runtime.*

### 2. Django 5.0 & Django REST Framework (DRF)
- **What it is:** Django is a high-level Python web framework encouraging rapid development and clean design. DRF is a powerful toolkit for building Web APIs in Django.
- **Why used:** Provides a battle-tested architecture including ORM, authentication, session management, CSRF security, and template rendering. DRF provides standardized serialization and JSON responses.
- **Where used:** `config/settings.py`, `apps/*/views.py`, `apps/*/serializers.py`, `apps/*/urls.py`.
- **Inter-component Communication:** Receives HTTP requests from frontend JavaScript `fetch()`, executes service logic, and returns either rendered HTML or serialized JSON responses.
- **Interview Example:** In `apps/predictions/views.py`, `@api_view(['GET'])` decorators handle parameter validation (`symbol`, `model`, `horizon`) and return structured JSON with appropriate HTTP status codes (200, 400, 500).
- **Interview Q&A:**
  - *Q: What is the benefit of using Django over Flask or FastAPI for this project?*
  - *A: Django provides an 'out-of-the-box' architecture with an enterprise ORM, migration system, robust authentication, CSRF protection, and session engine. This prevented reinventing security and user management, allowing us to focus on financial analytics and ML.*

### 3. SQLite & Django ORM
- **What it is:** SQLite is a self-contained, serverless, zero-configuration SQL database engine. Django ORM maps Python classes to relational tables.
- **Why used:** Ideal for development and demonstration with zero configuration. Django ORM allows switching to PostgreSQL in production simply by altering `DATABASES` settings without changing a single line of business code.
- **Where used:** `db.sqlite3`, `apps/*/models.py`, `apps/portfolio/services.py`.
- **Inter-component Communication:** Stores user credentials, profiles, portfolio transactions, watchlists, price alerts, historical model runs, and cached news articles.
- **Interview Example:** In `PortfolioAnalyticsService`, we query `portfolio.transactions.select_related('stock').order_by('date', 'created_at')` to calculate cost basis and enforce inventory guards against overselling.
- **Interview Q&A:**
  - *Q: How does Django ORM prevent SQL injection?*
  - *A: Django ORM parameterizes all SQL queries automatically. User inputs are treated as literal values rather than executable SQL commands, preventing SQL injection vulnerabilities.*

### 4. Custom Authentication Backend (`EmailOrUsernameModelBackend`)
- **What it is:** A custom Django authentication backend subclassing `ModelBackend`.
- **Why used:** Standard Django `ModelBackend` only authenticates by exact username case-sensitively. Our custom backend allows users to log in using either their username OR email address, handles usernames containing `@` characters (e.g., `Kiran@123`), trims whitespace, and performs case-insensitive lookups.
- **Where used:** `apps/accounts/backends.py`, registered in `config/settings.py`.
- **Inter-component Communication:** Invoked by Django's standard `authenticate(request, username=..., password=...)` function during login.
- **Interview Example:** When a user enters `Kiran@123`, the backend queries `User.objects.get(username__iexact='Kiran@123')` first. If no username matches, it checks `User.objects.get(email__iexact=...)`, followed by `user.check_password(password)`.
- **Interview Q&A:**
  - *Q: Why write a custom authentication backend instead of doing username/email checks in the view?*
  - *A: Writing a custom backend keeps views clean and DRY, integrates natively with Django's `authenticate()` system, preserves session security, and prevents fragile string-checking bugs like assuming any input with an '@' symbol must be an email.*

### 5. Pandas & NumPy
- **What it is:** Pandas provides high-performance data structures (`DataFrame`, `Series`); NumPy provides multidimensional array computation.
- **Why used:** Essential for financial time-series manipulation: date parsing, rolling window averages, exponential smoothing, volatility calculations, and array reshaping.
- **Where used:** `apps/analytics/services.py`, `apps/predictions/services/pipeline.py`, `apps/predictions/services/forecasting.py`.
- **Inter-component Communication:** Takes raw arrays from `yfinance`, cleans NaNs, computes technical indicators, scales sequences, and feeds arrays into Scikit-Learn and TensorFlow.
- **Interview Example:** In `TechnicalIndicatorService`, RSI is computed using Wilder's exponential smoothing: `gain.ewm(alpha=1/14, min_periods=14, adjust=False).mean()`.
- **Interview Q&A:**
  - *Q: How does vectorized computation in NumPy/Pandas improve performance?*
  - *A: Vectorization executes repetitive array operations in compiled C rather than interpreted Python loops, reducing execution times from hundreds of milliseconds to under 2 milliseconds.*

### 6. Scikit-Learn
- **What it is:** Python's premier library for classical machine learning and data preprocessing.
- **Why used:** Provides `MinMaxScaler` for feature normalization, `LinearRegression` for autoregressive baselines, `RandomForestRegressor` for non-linear decision tree ensembles, and statistical evaluation metrics (`mean_squared_error`, `mean_absolute_error`).
- **Where used:** `apps/predictions/services/pipeline.py`, `apps/predictions/services/forecasting.py`.
- **Inter-component Communication:** Used in the forecasting pipeline to scale training sequences and evaluate out-of-sample residuals.
- **Interview Example:** `scaler = MinMaxScaler(feature_range=(0, 1))` is fit strictly on `train_prices` (80% split) and transforms both train and test partitions to eliminate data leakage.
- **Interview Q&A:**
  - *Q: Why did you use Random Forest alongside Deep Learning?*
  - *A: Random Forest serves as a robust non-linear baseline. It requires minimal hyperparameter tuning, handles non-linear price relationships without vanishing gradients, and does not overfit as easily on smaller financial datasets.*

### 7. Statsmodels (ARIMA)
- **What it is:** A specialized statistical library for econometric and time-series modeling.
- **Why used:** Provides the `ARIMA` (Autoregressive Integrated Moving Average) model to capture linear autocorrelation and return trends.
- **Where used:** `apps/predictions/services/forecasting.py`.
- **Inter-component Communication:** Fits an ARIMA model on log returns (`np.log(P_t / P_{t-1})`), forecasts step-ahead returns, and blends predictions with the LSTM network.
- **Interview Example:** `model = ARIMA(log_returns_train, order=(1, 1, 0)).fit()` models price momentum without non-stationary raw price drift.
- **Interview Q&A:**
  - *Q: Why model log returns in ARIMA instead of raw stock prices?*
  - *A: Raw stock prices are non-stationary (they exhibit random walks and trends). Log returns are stationary, stabilizing variance and making statistical estimation valid.*

### 8. TensorFlow / Keras
- **What it is:** An end-to-end open-source machine learning platform and deep learning framework.
- **Why used:** Implements Deep Long Short-Term Memory (LSTM) recurrent neural networks capable of learning temporal dependencies across 30-day sequential price patterns.
- **Where used:** `apps/predictions/services/forecasting.py`.
- **Inter-component Communication:** Takes 3D sequence tensors `(samples, 30, 1)`, runs forward passes through stacked LSTM and Dropout layers, and outputs normalized price projections.
- **Interview Example:** We construct a 2-layer LSTM network with Dropout layers to prevent co-adaptation:
  ```python
  Sequential([
      LSTM(32, return_sequences=True, input_shape=(30, 1)),
      Dropout(0.15),
      LSTM(32, return_sequences=False),
      Dropout(0.15),
      Dense(16, activation='relu'),
      Dense(1)
  ])
  ```
- **Interview Q&A:**
  - *Q: Why is LSTM suited for stock price sequence modeling compared to vanilla RNNs?*
  - *A: Vanilla RNNs suffer from vanishing gradients over long sequences. LSTMs introduce memory cell states regulated by input, forget, and output gates, allowing the network to retain long-term market trends while filtering out noise.*

### 9. Yahoo Finance (`yfinance`)
- **What it is:** An open-source Python library that interfaces with Yahoo Finance public endpoints.
- **Why used:** Fetches daily OHLCV historical pricing, live quotes, company meta-information, and publisher news for global markets.
- **Where used:** `apps/market/services.py`, `apps/news/services.py`.
- **Inter-component Communication:** Called by `MarketDataService` when local cache misses, populating DataFrames and updating `Stock` model cache fields.
- **Interview Example:** `ticker.history(period="2y", interval="1d")` pulls two years of adjusted daily candles for model training.
- **Interview Q&A:**
  - *Q: How do you handle yfinance rate limits and network latency?*
  - *A: We implemented a multi-tier cache using Django's `LocMemCache`. Live quotes are cached for 90 seconds, and historical OHLCV DataFrames are cached for 1 hour. If Yahoo Finance fails, we fall back to database snapshots stored in our `Stock` model.*

### 10. VADER Sentiment Analysis (`vaderSentiment`)
- **What it is:** Valence Aware Dictionary and sEntiment Reasoner—a lexicon and rule-based sentiment analysis tool specifically tuned to microblog and news sentiment.
- **Why used:** Provides real-time financial headline sentiment scoring without requiring massive GPU language model overhead.
- **Where used:** `apps/news/services.py`.
- **Inter-component Communication:** Scores headline strings and produces a compound score from -1.0 (extremely negative) to +1.0 (extremely positive), mapping them to `POSITIVE`, `NEGATIVE`, or `NEUTRAL`.
- **Interview Example:** Articles with compound score $\ge +0.05$ are tagged positive; $\le -0.05$ are tagged negative. Articles are persisted in `NewsArticle` models.
- **Interview Q&A:**
  - *Q: Why use VADER instead of training a custom sentiment model?*
  - *A: VADER is computationally lightweight, executes in sub-millisecond time on CPU, handles financial intensity modifiers and capitalization gracefully, and does not require complex model retraining or labeled dataset maintenance.*

### 11. Plotly.js & Modern Frontend (HTML5, CSS3, Vanilla JS ES6+)
- **What it is:** Plotly.js is a high-level, declarative, WebGL-accelerated charting library. Vanilla JavaScript (ES6+) handles asynchronous DOM manipulation.
- **Why used:** Renders interactive financial charts (candlesticks, line charts, volume histograms, indicator subplots, and forecast trajectories) with zoom, pan, and hover tooltips. Avoids unnecessary heavy frontend frameworks (React/Vue/Node.js), keeping the application lean and Django-focused.
- **Where used:** `templates/`, `static/js/charts.js`, `static/js/stocksense.js`.
- **Inter-component Communication:** Calls Django REST endpoints via `fetch()`, receives JSON arrays, and dynamically plots multi-trace charts in the browser DOM.
- **Interview Example:** `StockSenseCharts.renderForecastChart()` renders three synchronized traces: actual test prices (white), out-of-sample validation predictions (purple dashed), and multi-day forward projections (blue markers).
- **Interview Q&A:**
  - *Q: Why choose Plotly.js over Chart.js or Lightweight Charts for this platform?*
  - *A: Plotly.js provides native support for multi-axis financial charts, candlestick rendering, volume subplots, and mathematical scatter traces with built-in range sliders and responsive SVG/WebGL rendering.*

---

# Part 3: Complete Project Architecture & Data Flows

### Overall System Architecture
The application follows a clean **4-Tier Architecture**:
1. **Presentation Tier (Client):** HTML5 templates styled with custom CSS variables and subtle Bootstrap 5 utilities. Plotly.js renders visual financial charts. Vanilla JavaScript manages asynchronous fetch calls.
2. **API & Routing Tier (Django Gateway):** `config/urls.py` routes incoming HTTP requests to dedicated apps. Django's middleware enforces CSRF validation, session management, and authentication checks. Django REST Framework serializes data to JSON.
3. **Business Logic & Services Tier (Python Engines):**
   - `MarketDataService`: Coordinates quote fetching, validation, and multi-tier caching.
   - `TechnicalIndicatorService`: Computes moving averages, RSI, MACD, Bollinger Bands, and ATR.
   - `PortfolioAnalyticsService`: Manages FIFO inventory, cost basis, and P&L accounting.
   - `ForecastingService` & `TimeSeriesDataPipeline`: Prepares sequence data, trains models, optimizes ensemble weights, and evaluates residuals.
   - `NewsSentimentService`: Fetches financial headlines and computes VADER polarity.
   - `ResearchAssistantService`: RAG-grounded copilot that queries platform state to answer queries.
4. **Data Persistence Tier (Database & Cache):** SQLite database (PostgreSQL-ready) managed via Django ORM, and `LocMemCache` for in-memory response acceleration.

```
+-----------------------------------------------------------------------------------+
|                            CLIENT BROWSER (TIER 1)                                |
|  HTML5 Templates | Custom CSS3 | Plotly.js Financial Charts | Vanilla JS (ES6)     |
+------------------------------------------+----------------------------------------+
                                           | HTTP Requests (HTML / JSON Fetch)
                                           v
+-----------------------------------------------------------------------------------+
|                        DJANGO API & ROUTING GATEWAY (TIER 2)                      |
|  config/urls.py | SessionMiddleware | CSRF | Django REST Framework (DRF)          |
+------------------------------------------+----------------------------------------+
                                           | Dispatches
                                           v
+-----------------------------------------------------------------------------------+
|                        BUSINESS LOGIC & SERVICES (TIER 3)                         |
|  +--------------------+  +-----------------------+  +--------------------------+  |
|  | MarketDataService  |  | PortfolioAnalytics    |  | TechnicalIndicatorEngine |  |
|  | yfinance + Cache   |  | FIFO Cost Basis + P&L |  | Pure Pandas (RSI, MACD)  |  |
|  +--------------------+  +-----------------------+  +--------------------------+  |
|  +-----------------------------------------------+  +--------------------------+  |
|  | ForecastingService & TimeSeriesDataPipeline   |  | NewsSentimentService     |  |
|  | Linear, RF, ARIMA, LSTM, Hybrid Ensemble      |  | VADER Compound Polarity  |  |
|  +-----------------------------------------------+  +--------------------------+  |
+------------------------------------------+----------------------------------------+
                                           | Reads / Writes
                                           v
+-----------------------------------------------------------------------------------+
|                        DATA PERSISTENCE & CACHE (TIER 4)                          |
|  SQLite (db.sqlite3) via Django ORM | LocMemCache In-Memory (90s - 1hr)           |
+-----------------------------------------------------------------------------------+
```

### Stock Price Data & Cache Pipeline
When a user navigates to `/stocks/TCS.NS/` or switches time ranges:
1. The browser dispatches `fetch('/api/stocks/TCS.NS/history/?period=1y')`.
2. The view calls `MarketDataService.get_historical_ohlcv('TCS.NS', period='1y')`.
3. The service checks `cache.get('ohlcv_TCS.NS_1y')`:
   - **Cache HIT:** Returns cached DataFrame and structured JSON immediately (latency < 5ms).
   - **Cache MISS:** Calls `yfinance.Ticker('TCS.NS').history(period='1y')`, cleans dates and zero volume days, stores the result in `LocMemCache` for 1 hour, and updates the local `Stock` database snapshot.
4. The service passes the DataFrame to `TechnicalIndicatorService.calculate_indicators(df)`.
5. Technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands, ATR) are appended as series.
6. DRF serializes the combined dataset to JSON.
7. The browser receives the JSON payload; Plotly.js redraws the candlestick chart, volume bars, and RSI subplots.

### Machine Learning Forecasting Pipeline
When a user executes the econometric model:
1. The frontend dispatches `GET /api/predictions/TCS.NS/?model=hybrid&horizon=30`.
2. `ForecastingService.train_and_forecast()` fetches 2 years of daily data (verifying $\ge 50$ observations).
3. `TimeSeriesDataPipeline.prepare_raw_data()` executes a chronological **80% train / 20% test split**.
4. A `MinMaxScaler(0, 1)` is fit **solely** on training data to prevent look-ahead data leakage.
5. Models are trained:
   - **LSTM:** Constructs rolling 30-day sequence tensors `(samples, 30, 1)` and trains a 2-layer LSTM with Dropout for 15 epochs.
   - **ARIMA:** Fits an autoregressive model on stationary log returns.
6. **Ensemble Blending:** Grid-searches blending parameter $\alpha \in [0.2, 0.8]$:
   $$\hat{y}_{hybrid} = \alpha \cdot \hat{y}_{LSTM} + (1 - \alpha) \cdot \hat{y}_{ARIMA}$$
   Selects $\alpha$ that minimizes Mean Squared Error on the held-out test split.
7. Step-by-step walk-forward test predictions and a 30-day multi-step recursive future forecast are generated.
8. `ModelEvaluator` calculates out-of-sample metrics: MAE, RMSE, and Directional Accuracy.
9. Results are saved to a `PredictionRun` database record and returned as JSON.
10. Plotly.js visualizes actual test prices, validation predictions, and the future projection cone.

### Authentication & Persistent Session Architecture
1. The user submits credentials (username/email and password).
2. Django calls `authenticate(request, username=..., password=...)`.
3. `EmailOrUsernameModelBackend`:
   - Trims whitespace.
   - Executes case-insensitive lookup: `User.objects.get(username__iexact=identifier)`.
   - If not found, falls back to `User.objects.get(email__iexact=identifier)`.
   - On match, verifies password via `user.check_password(password)` (PBKDF2-SHA256).
4. `login(request, user)` creates a session entry in the `django_session` table in SQLite.
5. Django issues an HTTP-only, SameSite=Lax cookie: `stocksense_sessionid`.
6. With `SESSION_SAVE_EVERY_REQUEST = True` and a 14-day age, sessions persist across browser refreshes and development server restarts.

---

# Part 4: In-Depth Feature-by-Feature Implementation Guide

### Feature A: User Authentication & Profile Customization
- **Purpose:** Secure platform access, preserve personalized portfolios, watchlists, and price alerts.
- **User Interaction:** Users can register (`/signup/`), log in (`/login/`), use a one-click **"Use Demo Credentials (demo_trader)"** button, and update preferences (`/profile/`).
- **Files Involved:**
  - `apps/accounts/backends.py` (`EmailOrUsernameModelBackend`)
  - `apps/accounts/views.py` (`signup_view`, `login_view`, `logout_view`, `profile_view`)
  - `apps/accounts/forms.py` (`UserRegistrationForm`, `UserLoginForm`, `UserProfileForm`)
  - `templates/accounts/login.html`
- **Key Code Snippet (`apps/accounts/backends.py`):**
  ```python
  class EmailOrUsernameModelBackend(ModelBackend):
      def authenticate(self, request, username=None, password=None, **kwargs):
          clean_identifier = str(username).strip()
          user = None
          # 1. Match username case-insensitively (handles '@' in usernames)
          try:
              user = UserModel.objects.get(username__iexact=clean_identifier)
          except UserModel.DoesNotExist:
              pass
          # 2. Fallback to email case-insensitively
          if user is None:
              try:
                  user = UserModel.objects.get(email__iexact=clean_identifier)
              except UserModel.DoesNotExist:
                  UserModel().set_password(password) # timing attack defense
                  return None
          if user and user.check_password(password) and self.user_can_authenticate(user):
              return user
          return None
  ```
- **Interview Questions:**
  - *Q: How does your authentication handle usernames containing '@' symbols?*
  - *A: Naive views check `if '@' in identifier` and assume the input is an email. In our custom backend, we query `username__iexact` first regardless of characters, correctly authenticating users like `Kiran@123` before falling back to email.*

### Feature B: Real-Time Market Overview & Global Universe
- **Purpose:** Provide a high-density snapshot of major global indices, market open/closed status, and top daily market movers.
- **User Interaction:** Displayed prominently at `/dashboard/` with NIFTY 50, SENSEX, S&P 500, and NASDAQ tickers, daily percentage deltas, and Top Gainers / Losers / Active stocks.
- **Files Involved:**
  - `apps/market/services.py` (`MarketDataService.get_market_overview()`, `get_market_movers()`)
  - `apps/market/views.py` (`dashboard_view`)
  - `templates/market/dashboard.html`
- **Key Logic:** Checks Indian market hours (Monday-Friday 09:15 - 15:30 IST) and US market hours (Monday-Friday 09:30 - 16:00 EST) using `pytz` timezone conversions.

### Feature C: Interactive Stock Explorer & Financial Charts
- **Purpose:** Provide detailed quote metrics and multi-timeframe financial charts for any supported equity.
- **User Interaction:** Search symbol (e.g. `TCS.NS`), view 52-week high/low, open, high, low, previous close, and switch between Candlestick and Line charts across 1M, 3M, 6M, 1Y, and 5Y ranges.
- **Files Involved:**
  - `apps/market/views.py` (`stock_detail_view`, `api_stock_quote`, `api_stock_history`)
  - `templates/market/stock_detail.html`
  - `static/js/charts.js` (`StockSenseCharts.renderCandlestickChart()`)
- **Key Code Snippet (`static/js/charts.js`):**
  ```javascript
  const traceCandle = {
    x: dates, open: opens, high: highs, low: lows, close: closes,
    type: 'candlestick',
    increasing: { line: { color: '#2ea043' } },
    decreasing: { line: { color: '#f85149' } }
  };
  Plotly.newPlot(containerId, [traceCandle, traceVolume], layout, config);
  ```

### Feature D: Technical Analysis & Multi-Factor Screener
- **Purpose:** Calculate mathematical indicators on historical price series to generate algorithmic trading signals.
- **User Interaction:** Accessible at `/screener/` and on each stock's detail page. Displays SMA 20/50/200, EMA 12/26/50, RSI 14, MACD, Bollinger Bands, and Average True Range with summary bias (Bullish/Neutral/Bearish).
- **Files Involved:**
  - `apps/analytics/services.py` (`TechnicalIndicatorService.calculate_indicators()`)
  - `apps/analytics/views.py` (`screener_view`, `api_stock_indicators`)
- **Mathematical Implementations:**
  - **RSI (Wilder's Smoothing):**
    $$RS = \frac{\text{EMA}_{14}(\text{Gain})}{\text{EMA}_{14}(\text{Loss})}, \quad RSI = 100 - \frac{100}{1 + RS}$$
  - **MACD:**
    $$\text{MACD Line} = \text{EMA}_{12}(\text{Close}) - \text{EMA}_{26}(\text{Close})$$
    $$\text{Signal Line} = \text{EMA}_9(\text{MACD Line}), \quad \text{Histogram} = \text{MACD Line} - \text{Signal Line}$$
  - **Bollinger Bands:**
    $$\text{Middle} = \text{SMA}_{20}(\text{Close}), \quad \text{Upper/Lower} = \text{Middle} \pm (2 \cdot \sigma_{20})$$

### Feature E: Portfolio Accounting Ledger & FIFO Position Tracker
- **Purpose:** Record stock buys/sells and calculate accurate inventory positions, average cost basis, cash balances, and realized/unrealized profit & loss.
- **User Interaction:** Add transactions via `/portfolio/`, view current holdings, unrealized return %, realized capital gains, and allocation pie chart.
- **Files Involved:**
  - `apps/portfolio/models.py` (`Portfolio`, `Transaction`)
  - `apps/portfolio/services.py` (`PortfolioAnalyticsService`)
  - `apps/portfolio/views.py` (`portfolio_dashboard_view`, `transactions_list_view`)
- **Overselling Guard (`apps/portfolio/services.py`):**
  ```python
  total_bought = sum(t.quantity for t in qs.filter(transaction_type='BUY'))
  total_sold = sum(t.quantity for t in qs.filter(transaction_type='SELL'))
  available_shares = total_bought - total_sold
  if quantity > available_shares:
      raise ValidationError(f"Cannot sell {quantity} shares. You currently own {available_shares} shares.")
  ```

### Feature F: Watchlists & Dynamic Threshold Price Alerts
- **Purpose:** Enable investors to track favorite tickers and receive trigger notifications when prices cross target thresholds.
- **User Interaction:** Toggle stocks into watchlist with one click; configure price alerts (`ABOVE` or `BELOW` target price) at `/alerts/`.
- **Files Involved:**
  - `apps/watchlists/models.py` (`Watchlist`, `WatchlistItem`, `PriceAlert`)
  - `apps/watchlists/services.py` (`WatchlistService`)
  - `apps/watchlists/views.py` (`watchlists_view`, `alerts_view`, `api_toggle_watchlist`)

### Feature G: Machine Learning Econometric Forecasting Lab
- **Purpose:** Provide transparent, walk-forward validated machine learning forecasting without black-box fabrications.
- **User Interaction:** Open `/predictions/?symbol=TCS.NS`, select model (`Hybrid`, `LSTM`, `ARIMA`, `Random Forest`, `Linear Regression`), pick forecast horizon (7, 14, 30 days), and click **"Execute Model"** or **"Compare All Models"**.
- **Files Involved:**
  - `apps/predictions/services/forecasting.py` (`ForecastingService`)
  - `apps/predictions/services/pipeline.py` (`TimeSeriesDataPipeline`, `ModelEvaluator`)
  - `apps/predictions/views.py` (`predictions_view`, `api_predict`, `api_compare_models`)
  - `templates/predictions/predictions.html`
- **Output:**
  - KPI Cards: Directional Accuracy %, MAE, RMSE, Expected Return %.
  - Plotly Chart: Actual Test Prices, Test Prediction (Validation), Future Forecast (Projection).
  - Leaderboard table comparing all 5 models side-by-side.

### Feature H: Financial News Sentiment Engine
- **Purpose:** Aggregate live market news and quantify market psychology using NLP sentiment scoring.
- **User Interaction:** Accessible at `/news/`. Shows categorized news cards with positive/neutral/negative badges, sentiment distribution bar, and direct source links.
- **Files Involved:**
  - `apps/news/models.py` (`NewsArticle`)
  - `apps/news/services.py` (`NewsSentimentService`)
  - `templates/news/news.html`

### Feature I: StockSense AI Copilot (Retrieval-Grounded Assistant)
- **Purpose:** An interactive financial assistant that inspects live platform data before answering user questions.
- **User Interaction:** Open `/assistant/`, ask questions like *"Analyze my portfolio risk"* or *"What is the technical outlook for TCS?"*.
- **Files Involved:**
  - `apps/assistant/models.py` (`ChatConversation`, `ChatMessage`)
  - `apps/assistant/services.py` (`ResearchAssistantService`)
  - `templates/assistant/assistant.html`
- **RAG Implementation:**
  - Extracts intent keywords (portfolio, symbol tickers).
  - Queries `PortfolioAnalyticsService` and `TechnicalIndicatorService` to gather live quantitative facts.
  - Passes facts to Google Gemini API (if configured) or synthesizes an analytical research briefing locally.

---

# Part 5: Machine Learning Explained from Absolute Zero

### Foundations: The Time-Series Supervised Regression Problem
In standard machine learning (like predicting house prices), each row is independent and identically distributed (i.i.d.). In stock market forecasting, observations are **time-series data** where sequence order matters fundamentally:
- **Target Variable ($y$):** The future price or future return:
  $$y_t = P_t \quad \text{or} \quad r_t = \ln\left(\frac{P_t}{P_{t-1}}\right)$$
- **Features ($X$):** Past historical observations:
  $$X_t = [P_{t-1}, P_{t-2}, \dots, P_{t-k}]$$
- **Problem Type:** Multi-step supervised autoregressive time-series regression.

### Zero Data Leakage: Chronological Partitioning & Pipeline Scaler
The single biggest mistake in financial machine learning is **data leakage**:
1. **The Flaw of Random Splitting:** Using standard `train_test_split(shuffle=True)` mixes future days into the training set. The model memorizes future prices, reporting fake 99% accuracy that fails completely in production.
2. **The Flaw of Global Normalization:** Fitting a `MinMaxScaler` on the entire dataset leaks the global maximum and minimum prices of future days into the past.
3. **Our Solution in `TimeSeriesDataPipeline`:**
   - **Chronological Split:** The first 80% of days chronologically form the training set; the final 20% form the held-out test set.
   - **Isolated Scaler Fitting:**
     ```python
     self.scaler.fit(train_prices.reshape(-1, 1))
     scaled_train = self.scaler.transform(train_prices.reshape(-1, 1)).flatten()
     scaled_test = self.scaler.transform(test_prices.reshape(-1, 1)).flatten()
     ```
     The test set is normalized using **only** the training set's minimum and maximum.

### The 5 Models Explained Simply

```
+-----------------------------------------------------------------------------------+
|                        5 FORECASTING ARCHITECTURES COMPARED                       |
+-------------------+----------------------------+----------------------------------+
| Model             | Mathematical Mechanism     | Core Strength / Limitation       |
+-------------------+----------------------------+----------------------------------+
| Linear Regression | Ordinary Least Squares     | Fast baseline; cannot capture    |
|                   | on 5 autoregressive lags   | non-linear regime shifts         |
+-------------------+----------------------------+----------------------------------+
| Random Forest     | Ensemble of 50 decision    | Captures non-linear thresholds;  |
|                   | trees with bagging         | cannot extrapolate beyond bounds |
+-------------------+----------------------------+----------------------------------+
| ARIMA(1, 1, 0)    | Autoregressive integrated  | Models linear return momentum;   |
|                   | moving average on returns  | assumes stationary variance      |
+-------------------+----------------------------+----------------------------------+
| LSTM Neural Net   | 2-layer stacked recurrent  | Learns long 30-day temporal      |
|                   | network with memory gates  | patterns; sensitive to noise     |
+-------------------+----------------------------+----------------------------------+
| Hybrid Ensemble   | Residual blending:         | Optimal synergy; mitigates       |
|                   | alpha*LSTM + (1-alpha)*ARIMA| individual model failure modes   |
+-------------------+----------------------------+----------------------------------+
```

#### 1. Autoregressive Linear Regression Baseline
- **Analogy:** Drawing the best straight trend line through recent momentum points.
- **Features Used:** Lag 1, Lag 2, Lag 3, Lag 5, 5-day rolling mean, and 10-day rolling standard deviation.
- **Why Needed:** Provides the mandatory statistical benchmark against which complex models must prove their worth.

#### 2. Random Forest Regressor
- **Analogy:** Asking 50 independent traders with different rules to vote on tomorrow's price, then averaging their estimates.
- **Hyperparameters:** `n_estimators=50`, `max_depth=6`, `random_state=42`.
- **Strength:** Captures non-linear interactions without gradient instability.

#### 3. ARIMA (1, 1, 0) on Log Returns
- **Analogy:** Tracking whether today's price momentum accelerates or reverses relative to yesterday's change.
- **Equation:**
  $$(1 - \phi_1 B)(1 - B) r_t = \epsilon_t$$
- **Walk-Forward Step:** At each day in the test set, ARIMA forecasts the next return $\hat{r}$, scales the previous actual price $P_{t-1} \cdot e^{\hat{r}}$, and updates its state.

#### 4. Deep LSTM Recurrent Neural Network
- **Analogy:** A reader with short-term and long-term memory who reads 30 days of trading tape and decides which patterns matter and which are random noise.
- **Architecture:** Stacked 32-unit LSTM layer $\to$ 15% Dropout $\to$ 32-unit LSTM layer $\to$ 15% Dropout $\to$ 16-unit Dense ReLU $\to$ Linear Output.
- **Vectorized Evaluation:** Test sequences are evaluated in a single vectorized forward pass `model.predict(test_seqs_arr)` for maximum performance.

#### 5. Hybrid LSTM-ARIMA Ensemble
- **Analogy:** Pairing a quantitative statistician (ARIMA) with an intuitive pattern-recognition AI (LSTM) and giving more voting power to whoever was more accurate recently.
- **Ensemble Optimization:**
  We evaluate a linear combination across a grid $\alpha \in [0.2, 0.8]$:
  $$\text{Loss}(\alpha) = \frac{1}{n} \sum_{i=1}^n \left( y_i - \left[ \alpha \hat{y}_{i, \text{LSTM}} + (1 - \alpha) \hat{y}_{i, \text{ARIMA}} \right] \right)^2$$
  The platform selects the $\alpha$ that minimizes held-out Test MSE.

### Walk-Forward Residual Evaluation
We compute three honest metrics on the out-of-sample held-out partition:
1. **Mean Absolute Error (MAE):** Average absolute rupee or dollar deviation:
   $$\text{MAE} = \frac{1}{n} \sum_{i=1}^n |y_i - \hat{y}_i|$$
2. **Root Mean Squared Error (RMSE):** Penalizes large forecast outliers:
   $$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2}$$
3. **Directional Accuracy (%):** Percentage of times the model correctly predicted the sign of tomorrow's price change:
   $$\text{DirAcc} = \frac{1}{n-1} \sum_{i=2}^n \mathbb{I}\left( \operatorname{sgn}(y_i - y_{i-1}) == \operatorname{sgn}(\hat{y}_i - y_{i-1}) \right) \times 100\%$$

### Statistical Limitations
- **Markets are Non-Stationary:** Macroeconomic events, earnings surprises, and geopolitical shocks fundamentally change market regimes.
- **No Guaranteed Predictions:** Past prices do not contain information about future unexpected news. Models provide mathematical trend projections, not financial guarantees.

---

# Part 6: Codebase Anatomy & Line-by-Line Code Walkthrough

```
Final year project/
|-- config/                     # Django project configuration
|   |-- settings.py             # Auth backends, sessions, database, caching
|   |-- urls.py                 # Top-level URL routing
|   |-- wsgi.py                 # WSGI production entry point
|-- apps/
|   |-- accounts/               # Custom auth backend, user profile, signup/login
|   |-- market/                 # Stock quotes, yfinance integration, explorer, indices
|   |-- portfolio/              # FIFO ledger, transactions, position tracker, P&L
|   |-- watchlists/             # Watchlist items and threshold price alerts
|   |-- analytics/              # TechnicalIndicatorService (SMA, EMA, RSI, MACD, BB)
|   |-- predictions/            # ForecastingService, pipeline, LSTM/ARIMA models
|   |-- news/                   # NewsSentimentService, VADER analyzer
|   |-- assistant/              # ResearchAssistantService, RAG copilot
|-- static/                     # CSS, vanilla JS, Plotly charting wrappers
|-- templates/                  # Django HTML template hierarchy
|-- tests/                      # 19 automated test cases covering auth, ML, portfolio
|-- db.sqlite3                  # Active SQLite database file
|-- manage.py                   # Django CLI management script
```

### Key Service Walkthroughs

#### 1. `apps/predictions/services/forecasting.py` (`train_and_forecast`)
```python
# 1. Fetch 2Y daily data
df, _ = MarketDataService.get_historical_ohlcv(symbol, period='2y')
# 2. Chronological data split and isolated scaler
pipeline = TimeSeriesDataPipeline(sequence_length=30, test_ratio=0.2)
train_prices, test_prices, scaled_train, scaled_test, all_prices = pipeline.prepare_raw_data(df)
# 3. Model dispatch
if model_type == 'hybrid':
    result = ForecastingService._train_hybrid(...)
# 4. Out-of-sample metrics calculation
metrics = ModelEvaluator.calculate_metrics(test_prices, np.array(test_pred))
# 5. Database audit logging
PredictionRun.objects.create(stock=stock, model_type=model_type, mae=metrics['mae'], ...)
```

#### 2. `apps/portfolio/services.py` (`calculate_portfolio`)
```python
# Computes average cost basis and realized P&L
for tx in transactions:
    if tx.transaction_type == 'BUY':
        pos['shares'] += tx.quantity
        pos['total_cost'] += (tx.quantity * tx.price) + tx.charges
        pos['avg_cost'] = pos['total_cost'] / pos['shares']
    elif tx.transaction_type == 'SELL':
        cost_of_sold = tx.quantity * pos['avg_cost']
        realized_pl += (tx.quantity * tx.price) - tx.charges - cost_of_sold
        pos['shares'] -= tx.quantity
```

---

# Part 7: API Specifications & Database Relational Model

### Selected REST Endpoints

| Method | Endpoint | Description | Auth Required | Status Codes |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/login` | JSON authentication | No | 200, 400, 401 |
| `GET` | `/api/market/overview/` | Key global indices & market open/closed status | No | 200 |
| `GET` | `/api/stocks/<symbol>/` | Live stock quote snapshot | No | 200, 404 |
| `GET` | `/api/stocks/<symbol>/history/` | Historical OHLCV candles | No | 200, 404 |
| `GET` | `/api/stocks/<symbol>/indicators/` | Calculated technical indicators | No | 200, 400 |
| `GET` | `/api/predictions/<symbol>/` | Execute ML forecast (model, horizon) | No | 200, 400, 500 |
| `GET` | `/api/predictions/compare/<symbol>/` | Compare all 5 models side-by-side | No | 200, 400 |
| `GET` | `/api/portfolio/` | User portfolio summary and holdings | Yes | 200, 401 |
| `POST` | `/api/portfolio/transactions/` | Create BUY/SELL transaction | Yes | 201, 400, 401 |
| `POST` | `/api/watchlists/toggle/<symbol>/` | Toggle stock in watchlist | Yes | 200, 401 |
| `POST` | `/api/assistant/chat/` | Submit prompt to AI copilot | Yes | 200, 400, 401 |

---

# Part 8: Security Architecture & Performance Engineering

- **Password Hashing:** Stored using standard `PBKDF2PasswordHasher` with SHA-256 and 1,500,000 iterations.
- **Session Protection:** Configured with `SESSION_COOKIE_HTTPONLY = True`, preventing client-side JavaScript access to session tokens and mitigating XSS token theft.
- **CSRF Defense:** Django's `CsrfViewMiddleware` generates cryptographically secure tokens validated on all mutating HTTP POST requests.
- **SQL Injection Prevention:** 100% of database queries use Django ORM parameterized expressions.
- **In-Memory Caching:** Quotes cached for 90s, OHLCV data for 1h, and market indices for 5m via `LocMemCache`.

---

# Part 9: Deployment Architecture & DevOps Workflow

### Local Development Setup
```bash
# 1. Clone or navigate to directory
cd "Final year project"

# 2. Run system checks
python manage.py check

# 3. Execute automated test suite (19 tests)
python manage.py test tests

# 4. Start local development server
python manage.py runserver 127.0.0.1:8000
```

### Production Deployment Architecture
- **WSGI Application Server:** Gunicorn or Uvicorn handling concurrent requests.
- **Static Assets:** Served via WhiteNoise with compression and unique manifest hashes.
- **Database:** PostgreSQL on AWS RDS or Render Managed Postgres via `DATABASE_URL`.
- **Process Supervision:** Docker containerization with Nginx reverse proxy handling SSL termination (HTTPS).

---

# Part 10: Selected Top 20 Technical Interview Questions & Model Answers

### Q1: What is StockSense AI, and why did you build it?
**Simple Answer:** StockSense AI is a full-stack financial intelligence and stock analysis web platform developed in Python and Django. It integrates live market quotes from Yahoo Finance, computes mathematical technical indicators using Pandas, and executes walk-forward validated machine learning models (like LSTM and ARIMA) to forecast stock price trajectories without data leakage.  
**Follow-up:** *How is your application different from existing stock portals?*  
**Answer:** Traditional portals display delayed static numbers or proprietary black-box predictions. StockSense AI provides an open quantitative laboratory where users can evaluate model residuals (MAE, RMSE, Directional Accuracy) on actual held-out test splits before reviewing forward projections.

### Q2: What exact machine learning models did you implement?
**Simple Answer:** We implemented five models: an Autoregressive Linear Regression baseline, Random Forest, ARIMA time-series on stationary log returns, a 2-layer Deep LSTM Neural Network, and a Hybrid LSTM-ARIMA Ensemble.  
**Follow-up:** *How does the Hybrid Ensemble work?*  
**Answer:** The hybrid model takes the test predictions from both LSTM and ARIMA and searches over a grid of alpha weights between 0.2 and 0.8 to find the combination that minimizes held-out Mean Squared Error. This blends linear momentum with non-linear neural patterns.

### Q3: How do you prevent data leakage in your forecasting pipeline?
**Simple Answer:** In `TimeSeriesDataPipeline`, we split our dataset chronologically into 80% training and 20% testing sets without shuffling. Crucially, our `MinMaxScaler` is fit solely on the training set, and its scaling parameters are applied to the test set.  
**Follow-up:** *What happens if you use standard k-fold cross validation on stock data?*  
**Answer:** Standard k-fold cross-validation shuffles data, training the model on future prices to predict past prices. This causes severe look-ahead bias, producing unrealistically high test accuracy that fails in real-world trading.

### Q4: How does user authentication work in your application?
**Simple Answer:** We built a custom authentication backend called `EmailOrUsernameModelBackend`. When a user submits credentials, it trims whitespace, queries `username__iexact` first, and if no user is found, queries `email__iexact`. It then verifies the password hash using PBKDF2-SHA256 and establishes a persistent database session.  
**Follow-up:** *Why was this custom backend necessary?*  
**Answer:** Standard Django authentication is case-sensitive and does not support email login. Additionally, naive views that check for an `@` symbol fail when usernames contain `@` (such as `Kiran@123`). Our backend handles special characters and casing cleanly.

### Q5: How do you calculate technical indicators like RSI and MACD?
**Simple Answer:** We implemented a pure Pandas and NumPy engine in `TechnicalIndicatorService`. For RSI, we calculate daily price deltas, separate gains and losses, and apply Wilder's exponential smoothing with an alpha of 1/14. For MACD, we subtract the 26-day EMA from the 12-day EMA, and compute a 9-day EMA signal line.

---

# Part 11: Mock Interview Practice Rounds

### Technical Round 1: Architecture & Backend
- **Scenario:** *"Walk me through the lifecycle of a request when a user visits `/stocks/TCS.NS/`."*
- **Model Key Points:** URL routing in `config/urls.py` $\to$ `stock_detail_view` in `apps/market/views.py` $\to$ `MarketDataService.get_stock_quote()` checks `LocMemCache` $\to$ on cache miss calls `yfinance` $\to$ computes technical indicators via `TechnicalIndicatorService` $\to$ renders `stock_detail.html` with context.

### Technical Round 2: Machine Learning & Time-Series
- **Scenario:** *"Your LSTM model predicts TCS will go up 10% next month. How confident are you in that prediction?"*
- **Model Key Points:** Stock prices are non-stationary and influenced by exogenous macroeconomic and company events that historical prices cannot foresee. Our model reports a directional accuracy of ~52% and an RMSE of ~49 on held-out test data. It serves as a quantitative probabilistic signal, not a guaranteed price prediction.

---

# Part 12: Quick Revision Guide (15-Minute Pre-Interview Cheat Sheet)

### Core Formulas Cheat Sheet
- **Log Return:** $r_t = \ln(P_t / P_{t-1})$
- **Mean Absolute Error:** $\text{MAE} = \frac{1}{n} \sum |y - \hat{y}|$
- **Root Mean Squared Error:** $\text{RMSE} = \sqrt{\frac{1}{n} \sum (y - \hat{y})^2}$
- **Directional Accuracy:** $\text{DirAcc} = \frac{\text{Correct Sign Predictions}}{\text{Total Steps}} \times 100\%$
- **RSI (14):** $100 - \frac{100}{1 + (\text{EMA}_{14}(\text{Gain}) / \text{EMA}_{14}(\text{Loss}))}$
- **Bollinger Bands:** $\text{SMA}_{20} \pm (2 \cdot \sigma_{20})$

### Critical Files Cheat Sheet
- **Custom Authentication:** `apps/accounts/backends.py`
- **Market Data & Caching:** `apps/market/services.py`
- **Portfolio FIFO Engine:** `apps/portfolio/services.py`
- **Technical Indicators:** `apps/analytics/services.py`
- **ML Forecasting Engine:** `apps/predictions/services/forecasting.py`
- **ML Data Pipeline:** `apps/predictions/services/pipeline.py`
- **VADER News Sentiment:** `apps/news/services.py`
- **AI Copilot (RAG):** `apps/assistant/services.py`
- **Financial Chart Wrappers:** `static/js/charts.js`
"""

def generate_markdown():
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(MARKDOWN_CONTENT)
    print(f"Master Markdown generated: {OUTPUT_FILE}")

if __name__ == '__main__':
    generate_markdown()
