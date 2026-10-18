"""
StockSense AI - Architecture Diagrams Catalog Generator
Generates AI_Stock_Market_Architecture_Diagrams.pdf
Contains all 6 high-resolution architectural diagrams with exhaustive technical breakdowns,
component maps, security details, and interview defense strategies.
"""

import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
import xml.sax.saxutils as saxutils

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIAGRAMS_DIR = os.path.join(os.path.dirname(__file__), 'diagrams')
OUTPUT_PATH = os.path.join(ROOT_DIR, 'AI_Stock_Market_Architecture_Diagrams.pdf')

PRIMARY = colors.HexColor('#0F172A')     # Slate 900
NAVY = colors.HexColor('#1E3A8A')        # Deep Blue
SECONDARY = colors.HexColor('#2563EB')   # Vibrant Indigo
ACCENT = colors.HexColor('#0D9488')      # Teal Accent
DARK_TEXT = colors.HexColor('#1E293B')   # Slate 800
BODY_TEXT = colors.HexColor('#334155')   # Slate 700
LIGHT_BG = colors.HexColor('#F8FAFC')    # Slate 50
BORDER_COLOR = colors.HexColor('#CBD5E1')# Slate 300
CALLOUT_BG = colors.HexColor('#EFF6FF')  # Soft Blue Tint
GREEN_BG = colors.HexColor('#ECFDF5')    # Emerald Tint
GREEN_BORDER = colors.HexColor('#10B981')

class LandscapeNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress on cover
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748B'))
        
        # Header
        self.drawString(40, landscape(letter)[1] - 25, "StockSense AI — System Architecture & Component Design Catalog")
        self.drawRightString(landscape(letter)[0] - 40, landscape(letter)[1] - 25, "Confidential — Technical Architecture Defense")
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(40, landscape(letter)[1] - 29, landscape(letter)[0] - 40, landscape(letter)[1] - 29)
        
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(landscape(letter)[0] - 40, 20, page_str)
        self.drawString(40, 20, "StockSense AI Platform Architecture • Full Stack Python, Django, REST APIs, ML Engines & VADER Sentiment")
        self.line(40, 28, landscape(letter)[0] - 40, 28)
        self.restoreState()

def esc(text):
    return saxutils.escape(str(text))

def build_architecture_catalog():
    print(f"Building Architecture Diagrams PDF: {OUTPUT_PATH}")
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=landscape(letter),
        leftMargin=40,
        rightMargin=40,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=NAVY,
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=19,
        textColor=SECONDARY,
        spaceAfter=20
    ))
    styles.add(ParagraphStyle(
        'CoverDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=BODY_TEXT,
        spaceAfter=25
    ))
    styles.add(ParagraphStyle(
        'DiagTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=NAVY,
        spaceAfter=4,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'DiagSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=SECONDARY,
        spaceAfter=8,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=NAVY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=BODY_TEXT,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=BODY_TEXT,
        leftIndent=12,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        'CodeText',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0F172A'),
        backColor=colors.HexColor('#F1F5F9'),
        borderPadding=4
    ))

    story = []

    # ==================== COVER PAGE ====================
    story.append(Spacer(1, 40))
    story.append(Paragraph("StockSense AI", styles['CoverTitle']))
    story.append(Paragraph("System Architecture, Data Pipelines & Technical Blueprint Catalog", styles['CoverSubtitle']))
    story.append(HRFlowable(width="100%", thickness=2, color=SECONDARY, spaceBefore=5, spaceAfter=15))
    
    cover_desc = (
        "This architectural specification documents the end-to-end design, component hierarchy, "
        "data flows, asynchronous processing pipelines, security layers, and relational entity models "
        "of the StockSense AI platform. Built strictly upon the production codebase, this catalog provides "
        "the definitive engineering defense reference for system architecture and technical interview reviews."
    )
    story.append(Paragraph(cover_desc, styles['CoverDesc']))
    
    # Metadata Table
    meta_data = [
        [Paragraph("<b>Platform Scope:</b>", styles['Body']), Paragraph("Enterprise Financial Intelligence, Econometric ML Forecasting, Portfolio Accounting", styles['Body'])],
        [Paragraph("<b>Backend Architecture:</b>", styles['Body']), Paragraph("Django 5.0 Core, Django REST Framework (DRF), 8 Modular Domain Apps, Multi-Model ML Service", styles['Body'])],
        [Paragraph("<b>Quantitative Engines:</b>", styles['Body']), Paragraph("NumPy, Pandas, Scikit-Learn, Statsmodels ARIMA(1,1,0), TensorFlow/Keras LSTM, VADER Sentiment", styles['Body'])],
        [Paragraph("<b>Database & Cache:</b>", styles['Body']), Paragraph("SQLite3 (Development) / PostgreSQL (Production), Django ORM with Zero-N+1 Prefetching, LocMemCache", styles['Body'])],
        [Paragraph("<b>Frontend & Visuals:</b>", styles['Body']), Paragraph("HTML5 Semantic Templates, Bootstrap 5 UI, Custom Vanilla JavaScript ES6+, Plotly.js Financial Charts", styles['Body'])],
        [Paragraph("<b>Candidate Portfolio:</b>", styles['Body']), Paragraph("Suitable for Python Full Stack Developer, Django Architect, and Financial Data Analyst Interview Defense", styles['Body'])],
    ]
    t_meta = Table(meta_data, colWidths=[150, 560])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_meta)
    
    story.append(Spacer(1, 20))
    catalog_summary = (
        "<b>Catalog Index:</b> (1) 4-Tier System Architecture & Modular App Map • "
        "(2) Zero-Data-Leakage ML Forecasting Pipeline • "
        "(3) Market Data, Caching & Plotly Financial Pipeline • "
        "(4) Dual-Identifier Authentication & Session Security Flow • "
        "(5) Relational Database Schema & Entity-Relationship Model (ERD) • "
        "(6) Financial News VADER Sentiment & RAG AI Copilot Engine."
    )
    story.append(Paragraph(catalog_summary, styles['Body']))
    story.append(PageBreak())

    # ==================== DIAGRAM DEFINITIONS ====================
    diagram_entries = [
        {
            'num': 1,
            'title': "Figure 1: Full-Stack 4-Tier System Architecture & Modular Django App Map",
            'subtitle': "Presentation Tier, Application Gateway & Security Tier, Domain Business Logic Tier, and Persistence Tier",
            'image': "architecture_system.png",
            'core_summary': (
                "The StockSense AI platform is architected around clean separation of concerns across four discrete tiers. "
                "The presentation layer communicates via HTTP/JSON with the Django application server. Incoming requests pass through "
                "Django's security middleware stack before routing to one of 8 modular applications: apps.accounts, apps.market, "
                "apps.portfolio, apps.watchlists, apps.analytics, apps.predictions, apps.news, and apps.assistant."
            ),
            'components': [
                ("Presentation Tier", "Bootstrap 5 responsive UI, Plotly.js interactive financial candlestick/line charting, modular ES6 JavaScript controllers with error-resilient JSON fetching."),
                ("Security & Middleware Tier", "CSRF enforcement, SecurityMiddleware, SessionMiddleware, AuthenticationMiddleware, and custom EmailOrUsernameModelBackend authentication provider."),
                ("Domain Business Logic Tier", "Decoupled service layer containing MarketDataService, ForecastingService, PortfolioAnalyticsService, TechnicalIndicatorService, NewsSentimentService, and ResearchAssistantService."),
                ("Persistence & Cache Tier", "Django ORM interfacing SQLite/PostgreSQL, transactional rollback atomicity (transaction.atomic), and in-memory cache (LocMemCache) for API call acceleration.")
            ],
            'interview_defense': (
                "<b>How to defend in an interview:</b> 'I separated the platform into 8 domain-specific Django apps rather than a monolithic views file. "
                "The views act as thin controllers that parse input, enforce authentication, and delegate to specialized service classes. "
                "This ensures the business logic (such as FIFO portfolio accounting and LSTM model evaluation) can be tested in isolation with zero tight coupling to HTTP requests.'"
            )
        },
        {
            'num': 2,
            'title': "Figure 2: Zero-Data-Leakage Econometric ML Forecasting Pipeline",
            'subtitle': "Chronological Train/Test Partitioning, Normalization Isolation, Multi-Model Training, and MSE-Optimized Ensembling",
            'image': "architecture_ml_pipeline.png",
            'core_summary': (
                "Financial time-series forecasting requires strict adherence to chronological ordering to eliminate data leakage. "
                "StockSense AI enforces an 80/20 train/test chronological split without random shuffling. The MinMaxScaler is fit exclusively "
                "on the training set and applied forward to test and forecast windows. Five distinct models are evaluated side-by-side: "
                "Autoregressive Linear Regression, Random Forest Regressor, ARIMA(1,1,0), Stacked LSTM Neural Network, and an MSE Grid-Optimized Hybrid Ensemble."
            ),
            'components': [
                ("Data Pipeline & Windowing", "yfinance fetches 2 years of daily OHLCV bars. TimeSeriesDataPipeline constructs sliding window sequences (lookback=60 trading days) mapping [t-59...t] to target price at t+1."),
                ("Strict Leakage Prevention", "MinMaxScaler.fit() executes ONLY on training observations. Future test data is transformed using learned training parameters (min/max), preventing future price leakage."),
                ("Model Architectures", "ARIMA models differenced stationary log-returns via statsmodels. The Deep LSTM features 2 stacked LSTM layers (32 & 32 units) with 15% Dropout, a Dense(16, relu) layer, and linear output."),
                ("Optimal Hybrid Ensembling", "Test predictions from ARIMA and LSTM are combined via y_pred = alpha*LSTM + (1-alpha)*ARIMA. The platform performs an exhaustive grid search over alpha in [0.2, 0.8] to identify the exact alpha minimizing held-out test MSE.")
            ],
            'interview_defense': (
                "<b>How to defend in an interview:</b> 'Most hobbyist stock forecasting projects suffer from look-ahead bias by standardizing data before splitting or using K-Fold cross-validation. "
                "In StockSense AI, I strictly enforced an 80/20 chronological partition. The scaler is fit strictly on training bars. Furthermore, I report walk-forward test metrics (MAE, RMSE, Directional Accuracy) "
                "and openly display model disclaimers explaining that past price autocorrelation cannot predict external macroeconomic shocks.'"
            )
        },
        {
            'num': 3,
            'title': "Figure 3: Market Data Ingestion, High-Performance Caching & Plotly Financial Pipeline",
            'subtitle': "yfinance Ingestion, LocMemCache Tier, Vectorized Technical Indicators, and Plotly Candlestick Serialization",
            'image': "architecture_data_flow.png",
            'core_summary': (
                "Market data retrieval is optimized for high responsiveness and resilience against upstream Yahoo Finance throttling. "
                "When a user inspects an equity, MarketDataService checks Django's in-memory cache (LocMemCache). On a cache miss, "
                "it fetches data via yfinance with timeout guards, computes technical indicators vectorized in Pandas, caches the result for 60-300 seconds, "
                "and serializes JSON payloads for interactive Plotly.js charts."
            ),
            'components': [
                ("Multi-Exchange Stock Universe", "Curated support for premier Indian equities (TCS.NS, INFY.NS, RELIANCE.NS, HDFCBANK.NS, SBIN.NS), US giants (AAPL, MSFT, NVDA, GOOGL, TSLA), and benchmark ETFs (SPY, QQQ, NIFTYBEES.NS)."),
                ("High-Speed Memory Cache", "LocMemCache caches quote snapshots (60s TTL) and historical dataframes (300s TTL). This achieves sub-50ms repeat query latencies and prevents external rate-limiting."),
                ("Vectorized Technical Indicators", "TechnicalIndicatorService calculates SMA(20,50,200), EMA(12,26,50), Wilder's RSI(14), MACD(12,26,9) with signal and histogram, Bollinger Bands (20, 2 std dev), and ATR(14) using pure vectorized Pandas/NumPy."),
                ("Interactive Plotly Rendering", "Frontend charts render dual subplots: Candlestick/OHLC pricing with moving average overlays on the primary axis, and color-coded trading volume bars on the secondary axis.")
            ],
            'interview_defense': (
                "<b>How to defend in an interview:</b> 'To prevent rate limiting and slow page loads, I implemented a two-tier caching pattern with LocMemCache. "
                "Quotes expire in 1 minute while 2-year historical data frames expire in 5 minutes. If Yahoo Finance is unreachable, the service falls back gracefully "
                "to database snapshots or simulated fallback bars, logging warning diagnostics without breaking the user experience.'"
            )
        },
        {
            'num': 4,
            'title': "Figure 4: Dual-Identifier Authentication, Session Security & Credential Pipeline",
            'subtitle': "EmailOrUsernameModelBackend, PBKDF2 Password Hashing, Persistent Database Sessions, and CSRF Token Guard",
            'image': "architecture_auth_flow.png",
            'core_summary': (
                "StockSense AI features an institutional authentication architecture that allows users to authenticate using either their "
                "alphanumeric username or registered email address. Passwords are cryptographic hashes stored using PBKDF2 with SHA-256 and a random salt. "
                "User sessions persist across server restarts via Django's database-backed session engine (django.contrib.sessions)."
            ),
            'components': [
                ("Custom Auth Backend", "EmailOrUsernameModelBackend intercepts credentials, performs case-insensitive lookup across username or email (Q(username__iexact=cred) | Q(email__iexact=cred)), and validates against User.check_password()."),
                ("Cryptographic Hashing", "Zero plain-text passwords. Django applies 720,000 iterations of PBKDF2 with SHA-256 hashing and unique per-user cryptographic salts, preventing rainbow table attacks."),
                ("Persistent Session Engine", "Sessions are stored in the django_session table rather than transient process memory. SESSION_COOKIE_AGE is set to 14 days, and SESSION_EXPIRE_AT_BROWSER_CLOSE=False ensures smooth development workflow."),
                ("Demo Trader Quick Access", "A dedicated 'Use Demo Credentials' client button fills verified demo credentials (demo_trader / Demo@StockSense2026), backed by an automatic database seeder if the account is absent.")
            ],
            'interview_defense': (
                "<b>How to defend in an interview:</b> 'Standard Django only authenticates by username out of the box. I wrote a custom authentication backend, "
                "EmailOrUsernameModelBackend, registered in AUTHENTICATION_BACKENDS. It queries the user table using Q objects for username or email case-insensitively, "
                "and verifies the PBKDF2 hash. I also ensured sessions persist in the database so restarting the server during demonstrations never logs the user out.'"
            )
        },
        {
            'num': 5,
            'title': "Figure 5: Relational Database Schema & Entity-Relationship Model (ERD)",
            'subtitle': "12 Normalized Models, Strict Foreign Key Constraints, Unique Indexes, and Zero-N+1 Query Architecture",
            'image': "architecture_database_erd.png",
            'core_summary': (
                "The database schema is fully normalized across 12 relational models, enforcing referential integrity, unique constraints, and cascade policies. "
                "User accounts link 1-to-1 with UserProfile for preferences. Portfolios contain child Transactions, Stocks link to HistoricalPrices and PriceAlerts, "
                "and Watchlists maintain ordered WatchlistItems. All queries utilize select_related and prefetch_related to guarantee zero N+1 database bottlenecks."
            ),
            'components': [
                ("User & Preference Models", "django.contrib.auth.models.User links 1-to-1 with UserProfile (base_currency: INR/USD, preferred_theme: dark/light)."),
                ("Market Master Models", "Stock model (symbol, name, exchange, currency, sector, is_active) links 1-to-Many with HistoricalPrice with unique_together=['stock', 'date'] constraint."),
                ("Portfolio & Transaction Ledger", "Portfolio links 1-to-Many with Transaction (transaction_type: BUY/SELL, quantity, price, execution_date, fees, notes). Strict validation prevents selling more shares than currently held."),
                ("Watchlists, Alerts & ML Runs", "Watchlist and WatchlistItem maintain user tracking lists. PriceAlert records condition (ABOVE/BELOW) and target price. PredictionRun logs model execution metadata, training duration, and MAE/RMSE metrics.")
            ],
            'interview_defense': (
                "<b>How to defend in an interview:</b> 'I designed the schema with strict referential integrity. In the transaction ledger, rather than mutating an editable balance field, "
                "every position is derived dynamically from the immutable ledger of BUY and SELL transactions. In the ORM, I prevent N+1 query performance degradation "
                "by using select_related on ForeignKeys and prefetch_related on reverse Many-to-One relationships.'"
            )
        },
        {
            'num': 6,
            'title': "Figure 6: Financial News Sentiment Pipeline & RAG Research Assistant",
            'subtitle': "News Aggregation, VADER Polarity Scoring, Grounded Context Retrieval, and Defensive Copilot Synthesis",
            'image': "architecture_sentiment_assistant.png",
            'core_summary': (
                "The intelligence suite combines real-time NLP news sentiment scoring with a retrieval-grounded AI copilot. "
                "NewsSentimentService ingests financial headlines, computes positive, negative, neutral, and compound polarity scores using NLTK VADER, "
                "and aggregates market sentiment. The ResearchAssistantService implements a Retrieval-Augmented Generation (RAG) architecture: "
                "it retrieves live portfolio positions, real-time quotes, and technical signals to ground the AI assistant's responses in verifiable data."
            ),
            'components': [
                ("VADER Sentiment Engine", "VADER (Valence Aware Dictionary and sEntiment Reasoner) analyzes financial headlines. A compound score >= 0.05 is classified as BULLISH/POSITIVE, <= -0.05 as BEARISH/NEGATIVE, and between -0.05 and 0.05 as NEUTRAL."),
                ("Headline Ingestion & Caching", "NewsArticle model caches ingested headlines, source publications, publication timestamps, and sentiment scores. Deduplication prevents repetitive sentiment weighting."),
                ("Context-Grounded RAG Engine", "When a user asks the AI Copilot about their portfolio or a stock, the backend queries the database for user holdings, fetches the latest RSI/MACD indicators, and injects this structured context into the prompt."),
                ("Conversational Memory", "ChatConversation and ChatMessage models persist conversation history with chronological ordering, allowing multi-turn research dialogues across browser sessions.")
            ],
            'interview_defense': (
                "<b>How to defend in an interview:</b> 'Instead of letting the AI assistant hallucinate random stock prices, I designed a RAG pipeline. "
                "The assistant queries the live PortfolioAnalyticsService and MarketDataService first. The verified numbers (such as actual realized P&L and 14-day RSI) "
                "are injected into the response generation context. For sentiment, VADER provides deterministic, explainable polarity scores without the latency of heavy cloud LLM calls.'"
            )
        }
    ]

    for entry in diagram_entries:
        # PAGE 1: DIAGRAM PAGE
        story.append(Paragraph(esc(entry['title']), styles['DiagTitle']))
        story.append(Paragraph(esc(entry['subtitle']), styles['DiagSubtitle']))
        story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=2, spaceAfter=8))
        
        img_path = os.path.join(DIAGRAMS_DIR, entry['image'])
        if os.path.exists(img_path):
            # Landscape letter is 792 x 612 pt. Margins are 40 pt each side. Printable width = 712 pt.
            # Available height = ~460 pt.
            # 4200 x 2400 is 1.75 aspect ratio. 700 pt wide by 400 pt high fits cleanly.
            img = Image(img_path, width=700, height=400)
            story.append(img)
        else:
            story.append(Paragraph(f"<b>[Diagram Image Not Found: {entry['image']}]</b>", styles['Body']))
            
        story.append(Spacer(1, 8))
        story.append(Paragraph(f"<b>Core Overview:</b> {esc(entry['core_summary'])}", styles['Body']))
        story.append(PageBreak())

        # PAGE 2: IN-DEPTH TECHNICAL BREAKDOWN & INTERVIEW DEFENSE
        story.append(Paragraph(f"Deep-Dive Technical Analysis & Interview Defense: {esc(entry['title'])}", styles['DiagTitle']))
        story.append(Paragraph(f"Architectural Specifications, Subsystem Interactions & Candidate Talking Points", styles['DiagSubtitle']))
        story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=2, spaceAfter=10))

        story.append(Paragraph("Subsystem Component Breakdown", styles['SectionHeader']))
        comp_table_data = [
            [Paragraph("<b>Subsystem / Component</b>", styles['Body']), Paragraph("<b>Technical Responsibilities & Code Implementation</b>", styles['Body'])]
        ]
        for name, desc in entry['components']:
            comp_table_data.append([
                Paragraph(f"<b>{esc(name)}</b>", styles['Body']),
                Paragraph(esc(desc), styles['Body'])
            ])
        t_comp = Table(comp_table_data, colWidths=[180, 530])
        t_comp.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
            ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t_comp)
        
        story.append(Spacer(1, 14))
        story.append(Paragraph("Candidate Technical Interview Defense & Viva Strategy", styles['SectionHeader']))
        
        # Interview Defense Callout
        def_content = [
            Paragraph("<b>Interview Defense Talking Points (Verbatim Script):</b>", ParagraphStyle('ITitle', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=colors.HexColor('#065F46'))),
            Spacer(1, 4),
            Paragraph(entry['interview_defense'], ParagraphStyle('IBody', fontName='Helvetica', fontSize=9, leading=13.5, textColor=DARK_TEXT))
        ]
        t_def = Table([[def_content]], colWidths=[710])
        t_def.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), GREEN_BG),
            ('BOX', (0,0), (-1,-1), 1.5, GREEN_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ]))
        story.append(t_def)
        
        if entry['num'] < len(diagram_entries):
            story.append(PageBreak())

    doc.build(story, canvasmaker=LandscapeNumberedCanvas)
    print(f"Successfully generated: {OUTPUT_PATH}")

if __name__ == '__main__':
    build_architecture_catalog()
