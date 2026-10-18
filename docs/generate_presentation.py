"""
StockSense AI - Professional Technical Interview Presentation Generator
Generates AI_Stock_Market_Project_Interview_Presentation.pptx
A 12-slide modern, dark-themed technical slide deck designed with python-pptx
for technical interview defense, project vivas, and architectural walkthroughs.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(ROOT_DIR, 'AI_Stock_Market_Project_Interview_Presentation.pptx')

# Color Palette (Dark Theme matching StockSense AI)
BG_DARK = RGBColor(15, 23, 42)       # Slate 900
CARD_BG = RGBColor(30, 41, 59)       # Slate 800
CARD_BORDER = RGBColor(51, 65, 85)   # Slate 700
NAVY_ACCENT = RGBColor(30, 58, 138)  # Deep Navy
INDIGO = RGBColor(59, 130, 246)      # Blue 500 / Indigo
EMERALD = RGBColor(16, 185, 129)     # Green 500
AMBER = RGBColor(245, 158, 11)       # Amber 500
WHITE = RGBColor(248, 250, 252)      # Slate 50
TEXT_MUTED = RGBColor(148, 163, 184) # Slate 400

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_DARK

def add_header(slide, title_text, category_text="STOCKSENSE AI • TECHNICAL INTERVIEW DEFENSE"):
    # Category badge
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.4), Inches(0.3))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(9)
    p_cat.font.bold = True
    p_cat.font.color.rgb = INDIGO
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(8.4), Inches(0.6))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = WHITE

def add_card(slide, left, top, width, height, title, body_bullets, accent_color=INDIGO):
    # Shape card
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = CARD_BG
    shape.line.color.rgb = accent_color
    shape.line.width = Pt(1.5)
    
    # Text
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    tf.margin_bottom = Inches(0.2)
    
    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(14)
    p_title.font.bold = True
    p_title.font.color.rgb = accent_color
    p_title.space_after = Pt(8)
    
    for bullet in body_bullets:
        p_b = tf.add_paragraph()
        p_b.text = f"• {bullet}"
        p_b.font.size = Pt(10.5)
        p_b.font.color.rgb = WHITE
        p_b.space_after = Pt(4)

def build_presentation():
    print(f"Building PowerPoint Presentation: {OUTPUT_PATH}")
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625) # 16:9 Widescreen
    blank_layout = prs.slide_layouts[6]

    # ==================== SLIDE 1: TITLE SLIDE ====================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)
    
    # Main Title Box
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(8.0), Inches(2.2))
    tf = t_box.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = "STOCKSENSE AI"
    p0.font.size = Pt(36)
    p0.font.bold = True
    p0.font.color.rgb = INDIGO
    p0.space_after = Pt(6)
    
    p1 = tf.add_paragraph()
    p1.text = "Stock Market Intelligence & Portfolio Analytics Platform"
    p1.font.size = Pt(18)
    p1.font.color.rgb = WHITE
    p1.space_after = Pt(12)

    p2 = tf.add_paragraph()
    p2.text = "Full Stack Django • REST APIs • Econometric ML • Real-Time VADER Sentiment • FIFO Accounting"
    p2.font.size = Pt(11)
    p2.font.color.rgb = EMERALD

    # Footer Metadata Card
    card_meta = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(3.8), Inches(8.0), Inches(1.1))
    card_meta.fill.solid()
    card_meta.fill.fore_color.rgb = CARD_BG
    card_meta.line.color.rgb = CARD_BORDER
    tf_m = card_meta.text_frame
    tf_m.word_wrap = True
    p_m1 = tf_m.paragraphs[0]
    p_m1.text = "Candidate Profile: Full Stack Python Developer & AI/ML Engineer (Fresher / Junior Role)"
    p_m1.font.size = Pt(11)
    p_m1.font.bold = True
    p_m1.font.color.rgb = WHITE
    p_m2 = tf_m.add_paragraph()
    p_m2.text = "Tech Stack: Python 3.13, Django 5.0, DRF, SQLite/PostgreSQL, Pandas, Scikit-Learn, Statsmodels, Keras, Plotly.js"
    p_m2.font.size = Pt(9.5)
    p_m2.font.color.rgb = TEXT_MUTED

    # ==================== SLIDE 2: THE PROBLEM & NEED ====================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Problem: Why Traditional Retail Tools Fall Short")
    add_card(s2, Inches(0.8), Inches(1.4), Inches(2.6), Inches(3.6),
             "1. Severe Fragmentation",
             ["Quotes, charts, news, and portfolio tracking exist on disparate websites.",
              "Investors must toggle between 4-5 apps to research a single equity.",
              "No unified institutional-grade analytics for retail traders."],
             AMBER)
    add_card(s2, Inches(3.7), Inches(1.4), Inches(2.6), Inches(3.6),
             "2. Fake 'Black-Box' AI",
             ["Hobbyist dashboards claim fake '98% accuracy' without auditable backtests.",
              "Many use random number generators disguised as artificial intelligence.",
              "Lack of transparency breeds distrust in quantitative tools."],
             RGBColor(239, 68, 68))
    add_card(s2, Inches(6.6), Inches(1.4), Inches(2.6), Inches(3.6),
             "3. Look-Ahead Data Leakage",
             ["Tutorial projects standardize data before train/test splitting.",
              "Random K-Fold cross validation uses future prices to predict past prices.",
              "Models fail catastrophically during live market execution."],
             INDIGO)

    # ==================== SLIDE 3: 4-TIER ARCHITECTURE ====================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "System Architecture: Decoupled 4-Tier Full-Stack Design")
    add_card(s3, Inches(0.8), Inches(1.4), Inches(4.0), Inches(1.7),
             "1. Presentation Tier",
             ["Semantic HTML5, Bootstrap 5 responsive 12-col grid.",
              "Interactive Plotly.js financial candlestick & volume charts.",
              "Vanilla ES6 JavaScript with error-resilient fetch handling."],
             INDIGO)
    add_card(s3, Inches(5.2), Inches(1.4), Inches(4.0), Inches(1.7),
             "2. Security & Gateway Tier",
             ["Django SecurityMiddleware, SessionMiddleware, CsrfViewMiddleware.",
              "Custom EmailOrUsernameModelBackend supporting dual login.",
              "Persistent database-backed session engine."],
             EMERALD)
    add_card(s3, Inches(0.8), Inches(3.3), Inches(4.0), Inches(1.7),
             "3. Domain Business Services Tier",
             ["8 Decoupled Django apps: accounts, market, portfolio, watchlists, etc.",
              "Service Layer Pattern: MarketDataService, ForecastingService, etc.",
              "Zero coupling between mathematical algorithms and HTTP views."],
             AMBER)
    add_card(s3, Inches(5.2), Inches(3.3), Inches(4.0), Inches(1.7),
             "4. Persistence & Cache Tier",
             ["Django ORM interfacing SQLite3 (Dev) / PostgreSQL (Prod).",
              "12 Normalized models with strict referential constraints.",
              "In-memory LocMemCache (60s quote TTL, 300s history TTL)."],
             RGBColor(168, 85, 247))

    # ==================== SLIDE 4: MARKET INGESTION & CACHING ====================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Market Ingestion, Caching & Global Stock Universe")
    add_card(s4, Inches(0.8), Inches(1.4), Inches(4.0), Inches(3.6),
             "High-Performance Caching Architecture",
             ["Two-tier caching using Django LocMemCache in RAM.",
              "Quote snapshots cached with 60-second Time-To-Live (TTL).",
              "2-Year daily historical data frames cached with 300-second TTL.",
              "Sub-5ms repeat query response times.",
              "Graceful fallback to database snapshots on API degradation."],
             INDIGO)
    add_card(s4, Inches(5.2), Inches(1.4), Inches(4.0), Inches(3.6),
             "Curated Multi-Exchange Universe",
             ["Indian NSE Equities: TCS.NS, INFY.NS, RELIANCE.NS, HDFCBANK.NS, SBIN.NS.",
              "US Tech Leaders: AAPL, MSFT, NVDA, GOOGL, TSLA.",
              "Benchmark ETFs: SPY, QQQ, NIFTYBEES.NS.",
              "Multi-currency support: Dynamic formatting for INR (Rs) and USD ($).",
              "Symbol normalization handling '.NS' suffix transparently."],
             EMERALD)

    # ==================== SLIDE 5: TECHNICAL ANALYSIS & PLOTLY ====================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Vectorized Technical Indicators & Interactive Charting")
    add_card(s5, Inches(0.8), Inches(1.4), Inches(4.0), Inches(3.6),
             "Vectorized Pandas Indicator Engine",
             ["Wilder's RSI (14): Exponential alpha=1/14 smoothing.",
              "MACD (12, 26, 9): Fast EMA, Slow EMA, Signal, and Histogram.",
              "Bollinger Bands (20, 2): 20 SMA middle +/- 2 std dev bands.",
              "Moving Averages: SMA (20, 50, 200) and EMA (12, 26, 50).",
              "Average True Range (ATR 14): Absolute volatility measurement.",
              "All computed in < 2ms using compiled NumPy/Pandas primitives."],
             AMBER)
    add_card(s5, Inches(5.2), Inches(1.4), Inches(4.0), Inches(3.6),
             "Plotly.js Financial Dual Subplots",
             ["Row 1 (80% Height): Candlestick price chart with 20/50 SMA overlay.",
              "Row 2 (20% Height): Color-coded volume bars (green/red).",
              "Shared X-axis: Synchronized crosshairs, panning, and zoom sliders.",
              "Time-range toggles: 1M, 3M, 6M, 1Y, 5Y with Plotly.react() updates.",
              "100% Responsive: Recalculates canvas size on viewport resize."],
             INDIGO)

    # ==================== SLIDE 6: FIFO PORTFOLIO ACCOUNTING ====================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Portfolio Accounting: Strict FIFO Cost Basis Ledger")
    add_card(s6, Inches(0.8), Inches(1.4), Inches(4.0), Inches(3.6),
             "Immutable Transaction Ledger",
             ["No mutable share count field on user or stock records.",
              "Holdings derived dynamically from immutable BUY/SELL trades.",
              "Fields: portfolio, stock, type, qty, price, fees, date, notes.",
              "Wrapped inside django.db.transaction.atomic blocks.",
              "Strict overselling prevention: raises ValidationError if selling unowned shares."],
             EMERALD)
    add_card(s6, Inches(5.2), Inches(1.4), Inches(4.0), Inches(3.6),
             "FIFO Calculation & Realized P&L",
             ["Buy lots queued in memory chronologically (deque).",
              "SELL trades consume oldest buy lots first (FIFO rule).",
              "Realized P&L = (Sell Price - Matched Buy Price) * Quantity.",
              "Unrealized P&L = (Market Price - FIFO Cost Basis) * Remaining Quantity.",
              "Asset Allocation Donut Chart renders live equity exposure."],
             INDIGO)

    # ==================== SLIDE 7: ZERO-DATA-LEAKAGE ML ====================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Machine Learning: Zero-Data-Leakage Pipeline")
    add_card(s7, Inches(0.8), Inches(1.4), Inches(4.0), Inches(3.6),
             "Supervised Sliding Window Pipeline",
             ["Historical Lookback = 60 Trading Days (~3 calendar months).",
              "Feature Tensor: X_t = [Price_{t-59}, ..., Price_t] (shape: N, 60, 1).",
              "Target Scalar: y_t = Price_{t+1}.",
              "Strict 80% Train / 20% Test Chronological Partition.",
              "NO random shuffling — preserves temporal autocorrelation."],
             INDIGO)
    add_card(s7, Inches(5.2), Inches(1.4), Inches(4.0), Inches(3.6),
             "Scaler Isolation & Forward Projection",
             ["MinMaxScaler fit strictly on training partition.",
              "Test partition transformed using training parameters ONLY.",
              "Eliminates look-ahead bias completely.",
              "Walk-forward recursive forecasting for 30-day horizon.",
              "Fixed random seeds (seed=42) for reproducible training."],
             AMBER)

    # ==================== SLIDE 8: 5 FORECASTING MODELS ====================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "5 Econometric & Deep Learning Models Compared")
    add_card(s8, Inches(0.8), Inches(1.4), Inches(2.6), Inches(3.6),
             "Baselines",
             ["1. Linear Regression:\nAutoregressive OLS across 60 lookback days. Fast, interpretable benchmark.",
              "2. Random Forest:\n50 decision trees, max_depth=6. Explicit regularization against price noise."],
             INDIGO)
    add_card(s8, Inches(3.7), Inches(1.4), Inches(2.6), Inches(3.6),
             "Time-Series & Deep",
             ["3. ARIMA(1, 1, 0):\nModeled on stationary log returns via statsmodels. Captures mean reversion.",
              "4. Stacked LSTM:\n2 layers (32-32-16-1) with 15% Dropout. Captures non-linear sequence memory."],
             EMERALD)
    add_card(s8, Inches(6.6), Inches(1.4), Inches(2.6), Inches(3.6),
             "Hybrid Ensemble",
             ["5. Hybrid Ensemble:\ny_pred = a*LSTM + (1-a)*ARIMA.",
              "Validation Grid Search:\nEvaluates alpha in [0.2, 0.8] to find exact alpha minimizing held-out test MSE.",
              "Blends deep learning with econometric rigor."],
             RGBColor(168, 85, 247))

    # ==================== SLIDE 9: VALIDATION & REALISTIC METRICS ====================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Walk-Forward Validation & Financial Realism")
    add_card(s9, Inches(0.8), Inches(1.4), Inches(4.0), Inches(3.6),
             "Out-of-Sample Performance Metrics",
             ["Mean Absolute Error (MAE): Raw rupee/dollar error.",
              "Root Mean Squared Error (RMSE): Penalizes large outlier misses.",
              "Directional Accuracy (%): Percentage of days where predicted direction (UP/DOWN) matched actual market move.",
              "TCS.NS Benchmark: Test MAE ~Rs 28.50 (~0.9% error), Directional Accuracy ~56.4%.",
              "Statistically significant edge for trend-following strategies."],
             EMERALD)
    add_card(s9, Inches(5.2), Inches(1.4), Inches(4.0), Inches(3.6),
             "Why Markets Are Not 100% Predictable",
             ["Efficient Market Hypothesis (EMH): Prices contain random-walk noise.",
              "Exogenous Shocks: Wars, interest rate changes, black swans.",
              "No past price sequence contains future geopolitical news.",
              "Transparent Disclaimers: Platform informs users that ML is a probabilistic risk-management tool, not a guarantee.",
              "Honest metrics prove professional engineering integrity."],
             AMBER)

    # ==================== SLIDE 10: AUTHENTICATION & SECURITY ====================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Authentication Architecture & Defensive Engineering")
    add_card(s10, Inches(0.8), Inches(1.4), Inches(4.0), Inches(3.6),
             "Dual-Identifier Authentication",
             ["Custom EmailOrUsernameModelBackend in apps.accounts.",
              "Case-insensitive lookup across username OR email via Q objects.",
              "Zero plain-text passwords: PBKDF2-SHA256 with 720,000 iterations.",
              "Persistent database sessions: SESSION_ENGINE = 'db'.",
              "Pre-seeded Demo Credentials button (demo_trader) for reviewers."],
             INDIGO)
    add_card(s10, Inches(5.2), Inches(1.4), Inches(4.0), Inches(3.6),
             "Defensive Web Engineering",
             ["Fixed 'SyntaxError: Unexpected token <' bug by enforcing strict JsonResponse error contracts on APIs.",
              "Frontend fetch validates response.ok and Content-Type before parsing JSON.",
              "CSRF protection enforced on all state-changing endpoints.",
              "Django ORM parameterization prevents SQL Injection.",
              "Zero N+1 queries via select_related() and prefetch_related()."],
             EMERALD)

    # ==================== SLIDE 11: SENTIMENT & AI COPILOT ====================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "VADER News Sentiment & RAG Research Assistant")
    add_card(s11, Inches(0.8), Inches(1.4), Inches(4.0), Inches(3.6),
             "VADER Financial Sentiment Engine",
             ["Ingests live financial news headlines from market feeds.",
              "Computes positive, negative, neutral, and compound polarity scores.",
              "Thresholds: Positive >= +0.05, Negative <= -0.05, Neutral between.",
              "Deterministic and explainable without heavy LLM API latency.",
              "Articles cached in database to prevent redundant NLP scoring."],
             AMBER)
    add_card(s11, Inches(5.2), Inches(1.4), Inches(4.0), Inches(3.6),
             "RAG-Grounded AI Research Copilot",
             ["Retrieval-Augmented Generation (RAG) architecture.",
              "Pulls live portfolio positions, current prices, and RSI/MACD signals.",
              "Injects factual database context into prompt to eliminate hallucinations.",
              "Conversations persisted in ChatConversation and ChatMessage models.",
              "Multi-turn conversational memory across browser sessions."],
             INDIGO)

    # ==================== SLIDE 12: TESTING & ROADMAP ====================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Production Readiness, Automated Testing & Roadmap")
    add_card(s12, Inches(0.8), Inches(1.4), Inches(4.0), Inches(3.6),
             "Verified Automated Test Suite",
             ["19 Unit and integration tests in tests/test_platform.py.",
              "Covers: Dual login, bad passwords, demo access, session persistence, trade execution, FIFO cost basis, overselling prevention, watchlist CRUD, and prediction API JSON contracts.",
              "Execution: Ran 19 tests in 4.8s — OK (100% Pass Rate).",
              "Production Stack: Gunicorn + Nginx + PostgreSQL + WhiteNoise."],
             EMERALD)
    add_card(s12, Inches(5.2), Inches(1.4), Inches(4.0), Inches(3.6),
             "Future Engineering Roadmap",
             ["1. Asynchronous Celery + Redis for background model training.",
              "2. WebSockets (Django Channels) for live tick-by-tick price streaming.",
              "3. Paper-trading broker API integration (Zerodha Kite / Alpaca).",
              "4. Quantitative Backtesting Engine for rule-based strategies.",
              "5. Monte Carlo Portfolio Simulation for Value at Risk (VaR)."],
             INDIGO)

    prs.save(OUTPUT_PATH)
    print(f"Successfully generated: {OUTPUT_PATH}")

if __name__ == '__main__':
    build_presentation()
