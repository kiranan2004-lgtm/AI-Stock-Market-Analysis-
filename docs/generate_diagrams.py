"""
StockSense AI - Architecture & Pipeline Diagram Generator
Generates publication-quality, high-resolution PNG diagrams for documentation and PDFs.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'diagrams')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Visual Theme Constants
BG_COLOR = '#0d1117'
SURFACE_COLOR = '#161b22'
BORDER_COLOR = '#30363d'
TEXT_COLOR = '#f0f6fc'
MUTED_COLOR = '#8b949e'
PRIMARY_ACCENT = '#58a6ff'
SUCCESS_ACCENT = '#2ea043'
PURPLE_ACCENT = '#bc8cff'
ORANGE_ACCENT = '#f0883e'
RED_ACCENT = '#f85149'

def draw_card(ax, x, y, w, h, title, subtitle, color=PRIMARY_ACCENT, bg=SURFACE_COLOR, title_size=11, sub_size=8.5):
    """Draw a rounded stylish card with a color banner."""
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.03,rounding_size=0.04",
        edgecolor=color, facecolor=bg, linewidth=1.5, zorder=2
    )
    ax.add_patch(box)
    
    # Top color tag strip
    tag = patches.FancyBboxPatch(
        (x, y + h - 0.04), w, 0.04,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        edgecolor=color, facecolor=color, linewidth=0, zorder=3
    )
    ax.add_patch(tag)

    ax.text(x + w / 2, y + h - 0.08, title, color=TEXT_COLOR, fontsize=title_size,
            weight='bold', ha='center', va='center', zorder=4)
    if subtitle:
        ax.text(x + w / 2, y + (h - 0.08) / 2, subtitle, color=MUTED_COLOR, fontsize=sub_size,
                ha='center', va='center', multialignment='center', zorder=4)

def draw_arrow(ax, x1, y1, x2, y2, label=None, color=MUTED_COLOR, rad=0.0):
    """Draw an arrow with an optional label."""
    connectionstyle = f"arc3,rad={rad}" if rad != 0.0 else "arc3"
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="->,head_width=0.35,head_length=0.45",
            color=color, lw=1.6, connectionstyle=connectionstyle
        ),
        zorder=5
    )
    if label:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2 + 0.035
        ax.text(mid_x, mid_y, label, color=TEXT_COLOR, fontsize=7.5,
                ha='center', va='bottom', backgroundcolor=BG_COLOR,
                bbox=dict(boxstyle='round,pad=0.2', facecolor=BG_COLOR, edgecolor=BORDER_COLOR, lw=0.8),
                zorder=6)

# ----------------------------------------------------
# DIAGRAM 1: OVERALL SYSTEM ARCHITECTURE
# ----------------------------------------------------
def generate_system_architecture():
    fig, ax = plt.subplots(figsize=(14, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.96, "StockSense AI - End-to-End System Architecture",
            color=TEXT_COLOR, fontsize=16, weight='bold', ha='center')
    ax.text(0.5, 0.93, "Decoupled Django Full-Stack Architecture with REST APIs and ML Forecasting Engine",
            color=MUTED_COLOR, fontsize=10, ha='center')

    # Column 1: Client Tier
    ax.text(0.12, 0.88, "CLIENT PRESENTATION TIER", color=PRIMARY_ACCENT, fontsize=9.5, weight='bold', ha='center')
    draw_card(ax, 0.02, 0.68, 0.20, 0.17, "Interactive Dashboard", "Bootstrap 5 + Custom CSS\nPlotly.js Financial Charts\nVanilla JS (ES6+ Fetch API)", PRIMARY_ACCENT)
    draw_card(ax, 0.02, 0.44, 0.20, 0.18, "Stock Explorer & Screener", "Global Symbol Search\nCandlestick & Line Modes\n1M, 3M, 6M, 1Y, 5Y Filters", PRIMARY_ACCENT)
    draw_card(ax, 0.02, 0.20, 0.20, 0.18, "Portfolio & ML Lab", "Transaction Management\nWalk-Forward Model Runner\nNews Sentiment Stream", PRIMARY_ACCENT)

    # Column 2: Web & API Routing Tier
    ax.text(0.38, 0.88, "DJANGO CORE & API GATEWAY", color=PURPLE_ACCENT, fontsize=9.5, weight='bold', ha='center')
    draw_card(ax, 0.28, 0.68, 0.20, 0.17, "Django URL Router", "config/urls.py\nSession Middleware\nCSRF Protection & CORS", PURPLE_ACCENT)
    draw_card(ax, 0.28, 0.44, 0.20, 0.18, "Django REST Framework", "ViewSets & @api_view\nJSON Serialization\nStatus Codes & Auth Checks", PURPLE_ACCENT)
    draw_card(ax, 0.28, 0.20, 0.20, 0.18, "Auth & Session Core", "EmailOrUsernameBackend\nPBKDF2 Password Hasher\nPersistent DB Sessions", PURPLE_ACCENT)

    # Column 3: Business & Quantitative Engine Tier
    ax.text(0.64, 0.88, "FINANCIAL & QUANT ENGINE", color=SUCCESS_ACCENT, fontsize=9.5, weight='bold', ha='center')
    draw_card(ax, 0.54, 0.70, 0.20, 0.15, "MarketDataService", "Yahoo Finance (yfinance)\nNSE / US Universe Cache\nLocMemCache (90s - 1h)", SUCCESS_ACCENT)
    draw_card(ax, 0.54, 0.51, 0.20, 0.15, "PortfolioAnalyticsService", "FIFO & Avg Cost Accounting\nOverselling Validation\nDual Currency (INR / USD)", SUCCESS_ACCENT)
    draw_card(ax, 0.54, 0.32, 0.20, 0.15, "TechnicalIndicatorService", "SMA, EMA, Wilder RSI 14\nMACD (12, 26, 9), BB, ATR\n100% Pure Pandas / NumPy", SUCCESS_ACCENT)
    draw_card(ax, 0.54, 0.13, 0.20, 0.15, "ForecastingService", "Hybrid LSTM-ARIMA Engine\nScikit-Learn, Statsmodels\nTensorFlow / Keras 2.x/3.x", SUCCESS_ACCENT)

    # Column 4: Storage & External Providers Tier
    ax.text(0.88, 0.88, "PERSISTENCE & EXTERNAL APIS", color=ORANGE_ACCENT, fontsize=9.5, weight='bold', ha='center')
    draw_card(ax, 0.78, 0.68, 0.20, 0.17, "SQLite / PostgreSQL", "Django ORM Models\nStock, HistoricalPrice\nPortfolio, Transaction", ORANGE_ACCENT)
    draw_card(ax, 0.78, 0.44, 0.20, 0.18, "Market Data Sources", "Yahoo Finance yfinance\nGlobal Indices (^NSEI, ^BSESN)\nLive OHLCV Feeds", ORANGE_ACCENT)
    draw_card(ax, 0.78, 0.20, 0.20, 0.18, "AI & NLP Services", "VADER Sentiment Analyzer\nGoogle Gemini AI API\nFinancial RSS Feeds", ORANGE_ACCENT)

    # Connecting Arrows
    draw_arrow(ax, 0.22, 0.77, 0.28, 0.77, "HTTP GET/POST")
    draw_arrow(ax, 0.22, 0.53, 0.28, 0.53, "JSON Fetch")
    draw_arrow(ax, 0.22, 0.29, 0.28, 0.29, "REST API")

    draw_arrow(ax, 0.48, 0.77, 0.54, 0.77, "Dispatches")
    draw_arrow(ax, 0.48, 0.53, 0.54, 0.58, "Calculates")
    draw_arrow(ax, 0.48, 0.53, 0.54, 0.40, "Extracts")
    draw_arrow(ax, 0.48, 0.29, 0.54, 0.21, "Trains & Predicts")

    draw_arrow(ax, 0.74, 0.77, 0.78, 0.77, "ORM Queries")
    draw_arrow(ax, 0.74, 0.77, 0.78, 0.53, "yfinance API")
    draw_arrow(ax, 0.74, 0.21, 0.78, 0.29, "NLP & AI")

    path = os.path.join(OUTPUT_DIR, 'architecture_system.png')
    plt.tight_layout()
    plt.savefig(path, dpi=300, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

# ----------------------------------------------------
# DIAGRAM 2: ML FORECASTING & VALIDATION PIPELINE
# ----------------------------------------------------
def generate_ml_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(14, 8), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "StockSense AI - Machine Learning Forecasting Pipeline",
            color=TEXT_COLOR, fontsize=16, weight='bold', ha='center')
    ax.text(0.5, 0.91, "Chronological Train-Test Split with Zero Look-Ahead Bias & Residual Blending",
            color=MUTED_COLOR, fontsize=10, ha='center')

    # Pipeline Stages
    draw_card(ax, 0.02, 0.55, 0.16, 0.28, "1. Data Acquisition", "MarketDataService\nFetches 2Y Daily OHLCV\nNaN/Null Cleaning\nValidates >= 50 Days", PRIMARY_ACCENT)
    draw_card(ax, 0.22, 0.55, 0.16, 0.28, "2. Chronological Split", "TimeSeriesDataPipeline\n80% Historical Train\n20% Held-Out Test\nZero Look-Ahead Bias", PURPLE_ACCENT)
    draw_card(ax, 0.42, 0.55, 0.16, 0.28, "3. Feature Engineering", "MinMaxScaler on Train\nAutoregressive Lags (1,2,3,5)\nRolling Mean & Std\n(X, y) Sequence Rolling", SUCCESS_ACCENT)
    draw_card(ax, 0.62, 0.55, 0.16, 0.28, "4. Model Execution", "Linear Regression\nRandom Forest (50 Trees)\nARIMA (1,1,0) on Returns\nLSTM (32-32-16 Dense)", ORANGE_ACCENT)
    draw_card(ax, 0.82, 0.55, 0.16, 0.28, "5. Ensemble Blending", "Hybrid LSTM-ARIMA\nMSE-Optimal Alpha Search\nTest Evaluation (MAE, RMSE)\nMulti-Day Forward Forecast", RED_ACCENT)

    # Bottom summary cards
    draw_card(ax, 0.05, 0.12, 0.26, 0.28, "Zero Data Leakage Rule", "MinMaxScaler is fit strictly on\nthe training 80% partition.\nTest set is scaled using\ntrain parameters exclusively.\nPrevents future price leakage.", SUCCESS_ACCENT)
    draw_card(ax, 0.37, 0.12, 0.26, 0.28, "Walk-Forward Validation", "Evaluates step-by-step 1-day\nahead out-of-sample residuals.\nMetrics: MAE, RMSE, and\nDirectional Accuracy (%)\non actual held-out market prices.", PURPLE_ACCENT)
    draw_card(ax, 0.69, 0.12, 0.26, 0.28, "Residual Blending Equation", "P_hybrid = a * P_lstm + (1-a) * P_arima\nAlpha optimized over grid [0.2, 0.8]\nto minimize out-of-sample Test MSE.\nCombines linear return trends\nwith non-linear neural patterns.", PRIMARY_ACCENT)

    # Arrows between stages
    draw_arrow(ax, 0.18, 0.69, 0.22, 0.69, "Clean DF")
    draw_arrow(ax, 0.38, 0.69, 0.42, 0.69, "80/20 Splits")
    draw_arrow(ax, 0.58, 0.69, 0.62, 0.69, "Scaled Arrays")
    draw_arrow(ax, 0.78, 0.69, 0.82, 0.69, "Sub-Predictions")

    # Connect to bottom summaries
    draw_arrow(ax, 0.30, 0.55, 0.18, 0.40, color=BORDER_COLOR)
    draw_arrow(ax, 0.50, 0.55, 0.50, 0.40, color=BORDER_COLOR)
    draw_arrow(ax, 0.90, 0.55, 0.82, 0.40, color=BORDER_COLOR)

    path = os.path.join(OUTPUT_DIR, 'architecture_ml_pipeline.png')
    plt.tight_layout()
    plt.savefig(path, dpi=300, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

# ----------------------------------------------------
# DIAGRAM 3: DATA FLOW ARCHITECTURE
# ----------------------------------------------------
def generate_data_flow_diagram():
    fig, ax = plt.subplots(figsize=(14, 8), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "StockSense AI - Market Data & Technical Analysis Flow",
            color=TEXT_COLOR, fontsize=16, weight='bold', ha='center')
    ax.text(0.5, 0.91, "How user queries fetch market quotes, compute indicators, and visualize charts",
            color=MUTED_COLOR, fontsize=10, ha='center')

    draw_card(ax, 0.03, 0.45, 0.16, 0.30, "1. User Browser", "User searches 'TCS.NS'\nSelects '1Y' period\nChooses 'Candlestick'\nFetch API triggered", PRIMARY_ACCENT)
    draw_card(ax, 0.23, 0.45, 0.16, 0.30, "2. Django View", "stock_detail_view\napi_stock_quote\napi_stock_indicators\nValidates symbol & period", PURPLE_ACCENT)
    draw_card(ax, 0.43, 0.45, 0.16, 0.30, "3. Cache Check", "LocMemCache lookup:\nohlcv_TCS.NS_1y\nIf HIT -> Return in 2ms\nIf MISS -> Call yfinance", ORANGE_ACCENT)
    draw_card(ax, 0.63, 0.45, 0.16, 0.30, "4. Market Data & Quant", "yfinance Ticker API\nPure Pandas Indicator Engine:\nSMA (20,50), EMA (20)\nRSI 14, MACD, BB, ATR", SUCCESS_ACCENT)
    draw_card(ax, 0.83, 0.45, 0.14, 0.30, "5. Plotly.js Visual", "JSON Response\nStockSenseCharts.js\nCandlestick + Volume\nRSI / MACD Subplots", PRIMARY_ACCENT)

    # Forward arrows
    draw_arrow(ax, 0.19, 0.65, 0.23, 0.65, "GET /stocks/TCS.NS/")
    draw_arrow(ax, 0.39, 0.65, 0.43, 0.65, "Cache Query")
    draw_arrow(ax, 0.59, 0.65, 0.63, 0.65, "On Cache Miss")
    draw_arrow(ax, 0.79, 0.65, 0.83, 0.65, "Calculates JSON")

    # Bottom explanation notes
    draw_card(ax, 0.10, 0.12, 0.38, 0.22, "Smart In-Memory Caching (LocMemCache)", "Quotes cached for 90 seconds to prevent rate limits.\nHistorical OHLCV cached for 1 hour.\nMarket overview cached for 5 minutes.\nEnsures lightning fast responses for recurring users.", ORANGE_ACCENT)
    draw_card(ax, 0.52, 0.12, 0.38, 0.22, "Resilient Fallback Mechanism", "If Yahoo Finance is unreachable or rate limits,\nplatform transparently recovers last snapshot from\nlocal Stock database model.\nFrontend clearly displays 'Delayed' or 'Cached'.", SUCCESS_ACCENT)

    path = os.path.join(OUTPUT_DIR, 'architecture_data_flow.png')
    plt.tight_layout()
    plt.savefig(path, dpi=300, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

# ----------------------------------------------------
# DIAGRAM 4: AUTHENTICATION & SESSION PERSISTENCE FLOW
# ----------------------------------------------------
def generate_auth_flow_diagram():
    fig, ax = plt.subplots(figsize=(14, 8), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "StockSense AI - Authentication & Session Architecture",
            color=TEXT_COLOR, fontsize=16, weight='bold', ha='center')
    ax.text(0.5, 0.91, "Robust dual-identifier authentication supporting usernames with '@' and persistent sessions",
            color=MUTED_COLOR, fontsize=10, ha='center')

    draw_card(ax, 0.02, 0.48, 0.16, 0.32, "1. Login Credentials", "User enters:\n'Kiran@123' OR\n'kiranan2004@gmail.com'\nOR Demo Trader button\nTrims whitespace", PRIMARY_ACCENT)
    draw_card(ax, 0.22, 0.48, 0.18, 0.32, "2. Custom Backend", "EmailOrUsernameBackend\n1. Lookup username__iexact\n(Fixes '@' in usernames!)\n2. Fallback to email__iexact\n3. Fake hash on miss", PURPLE_ACCENT)
    draw_card(ax, 0.44, 0.48, 0.16, 0.32, "3. Password Hashing", "Django check_password()\nPBKDF2 with SHA256\n1,500,000 Iterations\nSalted Cryptographic Hash\nZero plaintext storage", SUCCESS_ACCENT)
    draw_card(ax, 0.64, 0.48, 0.16, 0.32, "4. Database Session", "django_session Table\nstocksense_sessionid\nSESSION_SAVE_EVERY_REQUEST\n2-Week Cookie Age\nSurvives Server Restarts", ORANGE_ACCENT)
    draw_card(ax, 0.84, 0.48, 0.14, 0.32, "5. Protected Access", "login(request, user)\nHTTP 302 Redirect\n@login_required Access\nRestores Auth State\non Page Refresh", PRIMARY_ACCENT)

    draw_arrow(ax, 0.18, 0.64, 0.22, 0.64, "POST /login/")
    draw_arrow(ax, 0.40, 0.64, 0.44, 0.64, "User Found")
    draw_arrow(ax, 0.60, 0.64, 0.64, 0.64, "Hash Verified")
    draw_arrow(ax, 0.80, 0.64, 0.84, 0.64, "Session Created")

    draw_card(ax, 0.08, 0.10, 0.40, 0.26, "The Critical '@' Username Bug & Fix", "Earlier bug: if '@' in identifier, view assumed email.\nUsername 'Kiran@123' failed because email was different!\nSolution: Dedicated EmailOrUsernameModelBackend\nsearches username__iexact first regardless of characters.\nGuarantees seamless login for all user identifiers.", RED_ACCENT)
    draw_card(ax, 0.52, 0.10, 0.40, 0.26, "Persistent Database Sessions", "Engine: django.contrib.sessions.backends.db\nCookie Name: stocksense_sessionid (HttpOnly, SameSite=Lax)\nSESSION_SAVE_EVERY_REQUEST = True refreshes expiry.\nSessions stored in SQLite database, meaning users stay\nlogged in across browser reloads and development server restarts.", SUCCESS_ACCENT)

    path = os.path.join(OUTPUT_DIR, 'architecture_auth_flow.png')
    plt.tight_layout()
    plt.savefig(path, dpi=300, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

# ----------------------------------------------------
# DIAGRAM 5: DATABASE ENTITY RELATIONSHIP DIAGRAM (ERD)
# ----------------------------------------------------
def generate_database_erd():
    fig, ax = plt.subplots(figsize=(14, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.96, "StockSense AI - Relational Database Schema (ERD)",
            color=TEXT_COLOR, fontsize=16, weight='bold', ha='center')
    ax.text(0.5, 0.93, "Normalized SQLite / PostgreSQL Database Models with Foreign Key Integrity",
            color=MUTED_COLOR, fontsize=10, ha='center')

    # Core Models
    draw_card(ax, 0.03, 0.60, 0.18, 0.28, "User & UserProfile", "id (PK)\nusername (unique)\nemail, password (hash)\npreferred_currency\npreferred_theme\ninitial_capital", PRIMARY_ACCENT)
    draw_card(ax, 0.26, 0.60, 0.18, 0.28, "Portfolio", "id (PK)\nowner_id (FK -> User)\nname ('Primary')\ndescription\nbase_currency ('INR')\ncreated_at, updated_at", PURPLE_ACCENT)
    draw_card(ax, 0.50, 0.60, 0.20, 0.28, "Transaction", "id (PK)\nportfolio_id (FK -> Portfolio)\nstock_id (FK -> Stock)\ntransaction_type (BUY/SELL)\nquantity, price, charges\ndate, notes", ORANGE_ACCENT)
    draw_card(ax, 0.76, 0.60, 0.21, 0.28, "Stock", "id (PK)\nsymbol (unique, 'TCS.NS')\nname, exchange, sector\ncurrency ('INR'/'USD')\nlast_price, last_change\nday_high, day_low, volume", SUCCESS_ACCENT)

    draw_card(ax, 0.03, 0.18, 0.18, 0.32, "Watchlist & Item", "Watchlist (owner_id -> User)\n- is_default, name\n\nWatchlistItem\n- watchlist_id (FK)\n- stock_id (FK)\n- added_at", PRIMARY_ACCENT)
    draw_card(ax, 0.26, 0.18, 0.18, 0.32, "PriceAlert", "id (PK)\nowner_id (FK -> User)\nstock_id (FK -> Stock)\ntarget_price\ncondition (ABOVE/BELOW)\nstatus (ACTIVE/TRIGGERED)\ntriggered_at", RED_ACCENT)
    draw_card(ax, 0.50, 0.18, 0.20, 0.32, "PredictionRun", "id (PK)\nstock_id (FK -> Stock)\nmodel_type, horizon_days\npredicted_price, return_pct\nmae, rmse, dir_accuracy\npredictions_json (JSON)\ntest_actual_json (JSON)", PURPLE_ACCENT)
    draw_card(ax, 0.76, 0.18, 0.21, 0.32, "News & Assistant", "NewsArticle\n- stock_id (FK), headline\n- sentiment_label, score\n\nChatConversation (user_id)\nChatMessage (role, content)", SUCCESS_ACCENT)

    # Relationships
    draw_arrow(ax, 0.21, 0.74, 0.26, 0.74, "1 to 1..N")
    draw_arrow(ax, 0.44, 0.74, 0.50, 0.74, "1 to N")
    draw_arrow(ax, 0.76, 0.74, 0.70, 0.74, "1 to N")
    draw_arrow(ax, 0.12, 0.60, 0.12, 0.50, "1 to N")
    draw_arrow(ax, 0.35, 0.60, 0.35, 0.50, "1 to N")
    draw_arrow(ax, 0.86, 0.60, 0.60, 0.50, "1 to N")
    draw_arrow(ax, 0.86, 0.60, 0.86, 0.50, "1 to N")

    path = os.path.join(OUTPUT_DIR, 'architecture_database_erd.png')
    plt.tight_layout()
    plt.savefig(path, dpi=300, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

# ----------------------------------------------------
# DIAGRAM 6: NEWS SENTIMENT & AI COPILOT PIPELINE
# ----------------------------------------------------
def generate_sentiment_assistant_diagram():
    fig, ax = plt.subplots(figsize=(14, 8), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "StockSense AI - Financial News Sentiment & AI Copilot",
            color=TEXT_COLOR, fontsize=16, weight='bold', ha='center')
    ax.text(0.5, 0.91, "Lexicon-based VADER sentiment classification & Retrieval-Augmented Assistant",
            color=MUTED_COLOR, fontsize=10, ha='center')

    # Top Flow: News Sentiment
    ax.text(0.08, 0.82, "FINANCIAL NEWS SENTIMENT ANALYSIS PIPELINE", color=PRIMARY_ACCENT, fontsize=10, weight='bold')
    draw_card(ax, 0.05, 0.54, 0.18, 0.24, "News Acquisition", "yfinance Ticker.news\nFinancial Media publishers\nPublished timestamps\nHeadlines & URLs", PRIMARY_ACCENT)
    draw_card(ax, 0.28, 0.54, 0.20, 0.24, "VADER NLP Scoring", "SentimentIntensityAnalyzer\nFinancial word intensities\nCompound score calculation\nRange: [-1.0 to +1.0]", PURPLE_ACCENT)
    draw_card(ax, 0.53, 0.54, 0.20, 0.24, "Classification Logic", "Compound >= +0.05 -> POSITIVE\nCompound <= -0.05 -> NEGATIVE\nBetween -> NEUTRAL\nUpsert NewsArticle in DB", SUCCESS_ACCENT)
    draw_card(ax, 0.78, 0.54, 0.17, 0.24, "Terminal Display", "Sentiment distribution bar\nArticle cards with badges\nPublisher & timestamp\nDirect article links", ORANGE_ACCENT)

    draw_arrow(ax, 0.23, 0.66, 0.28, 0.66, "Headlines")
    draw_arrow(ax, 0.48, 0.66, 0.53, 0.66, "Scores")
    draw_arrow(ax, 0.73, 0.66, 0.78, 0.66, "Aggregated")

    # Bottom Flow: AI Copilot
    ax.text(0.08, 0.42, "GROUNDED RESEARCH ASSISTANT (RAG ARCHITECTURE)", color=SUCCESS_ACCENT, fontsize=10, weight='bold')
    draw_card(ax, 0.05, 0.10, 0.24, 0.28, "1. User Query & Context", "User asks: 'Analyze TCS portfolio'\nAssistant checks keywords\nPulls user holdings, P&L, cash\nExtracts stock tickers", SUCCESS_ACCENT)
    draw_card(ax, 0.35, 0.10, 0.30, 0.28, "2. Grounding & Synthesis", "Retrieves live quotes & SMA/RSI\nSynthesizes factual quantitative facts\nCalls Google Gemini API (if key)\nOR executes local quant analyst logic", PURPLE_ACCENT)
    draw_card(ax, 0.71, 0.10, 0.24, 0.28, "3. Intelligent Response", "Saves ChatMessage turn in DB\nOutputs structured investment analysis\nIncludes risk warnings & disclaimers\n100% grounded in real platform data", PRIMARY_ACCENT)

    draw_arrow(ax, 0.29, 0.24, 0.35, 0.24, "Tool Context")
    draw_arrow(ax, 0.65, 0.24, 0.71, 0.24, "Synthesizes")

    path = os.path.join(OUTPUT_DIR, 'architecture_sentiment_assistant.png')
    plt.tight_layout()
    plt.savefig(path, dpi=300, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

if __name__ == '__main__':
    generate_system_architecture()
    generate_ml_pipeline_diagram()
    generate_data_flow_diagram()
    generate_auth_flow_diagram()
    generate_database_erd()
    generate_sentiment_assistant_diagram()
    print("All 6 architecture diagrams generated successfully!")
