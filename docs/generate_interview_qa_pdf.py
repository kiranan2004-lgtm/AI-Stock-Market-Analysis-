"""
StockSense AI - 100+ Categorized Technical Interview Q&A PDF Generator
Generates AI_Stock_Market_Project_Interview_QA.pdf
Contains 110 comprehensive interview questions with simple answers,
deep-dive technical follow-ups, and interviewer pitfall warnings.
"""

import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
import xml.sax.saxutils as saxutils

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(ROOT_DIR, 'AI_Stock_Market_Project_Interview_QA.pdf')

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
AMBER_BG = colors.HexColor('#FFFBEB')    # Amber Tint
AMBER_BORDER = colors.HexColor('#F59E0B')

class NumberedCanvas(canvas.Canvas):
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
            return
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748B'))
        
        # Header
        self.drawString(40, letter[1] - 25, "StockSense AI — 100+ Categorized Technical Interview Questions & Answers")
        self.drawRightString(letter[0] - 40, letter[1] - 25, "Interview Preparation Manual")
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(40, letter[1] - 29, letter[0] - 40, letter[1] - 29)
        
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 40, 20, page_str)
        self.drawString(40, 20, "StockSense AI • Full Stack Python, Django 5, DRF, Econometric ML & Quantitative Finance")
        self.line(40, 28, letter[0] - 40, 28)
        self.restoreState()

def esc(text):
    return saxutils.escape(str(text))

# Build complete 110 question database across 8 categories
QA_DATABASE = [
    # -------------------------------------------------------------
    # CATEGORY 1: ARCHITECTURE & SYSTEM DESIGN (1-15)
    # -------------------------------------------------------------
    {
        "category": "Category 1: System Architecture & High-Level Design",
        "questions": [
            ("Q1: Can you give an architectural overview of your StockSense AI project?",
             "StockSense AI is structured as a 4-tier full-stack web platform consisting of a presentation tier (Bootstrap 5 and Plotly.js), an application & security tier (Django middleware and custom authentication), a domain business logic tier (8 decoupled service classes), and a persistence tier (Django ORM with SQLite/PostgreSQL and LocMemCache).",
             "Rather than putting business logic inside views, views act as slim controllers. When a user requests predictions or portfolio analytics, the view validates input, delegates to `ForecastingService` or `PortfolioAnalyticsService`, and serializes the result into a strict JSON contract.",
             "Avoid saying 'I just followed the standard Django MVT pattern.' Highlight the service layer pattern that isolates mathematical computations from HTTP request objects."),

            ("Q2: Why did you partition the application into 8 separate Django apps?",
             "To enforce the Single Responsibility Principle and maintain high cohesion with low coupling. Each app owns a discrete business domain: `accounts`, `market`, `portfolio`, `watchlists`, `analytics`, `predictions`, `news`, and `assistant`.",
             "In a financial system, mixing portfolio accounting with machine learning training creates monolithic spaghetti code. With modular apps, each has its own models, services, urls, and serializers. For example, if we need to swap out the news provider, only `apps.news` is touched.",
             "Don't say 'Because Django created them for me.' Explain that you deliberately designed the modular boundaries according to domain-driven design principles."),

            ("Q3: What design patterns did you use across the codebase?",
             "I used the Service Layer Pattern (isolating business algorithms), the Repository/ORM Pattern (Django QuerySets for data abstraction), the Factory/Strategy Pattern (selecting between 5 forecasting models dynamically), and the Decorator Pattern (`@login_required` and `@require_POST`).",
             "In `apps.predictions.services.ForecastingService`, the model execution method takes a model key string ('lstm', 'arima', 'ensemble') and dynamically invokes the matching model strategy. This makes adding new models (like XGBoost or Prophet) trivial without altering existing pipelines.",
             "Freshers often know design pattern names from textbooks but cannot cite where they used them. Always cite `ForecastingService` as the Strategy pattern example."),

            ("Q4: How does StockSense AI differ from a typical tutorial stock dashboard?",
             "Tutorial projects typically show static hardcoded numbers, fake 98% accuracy claims, or random price generators. StockSense AI connects to real NSE and US feeds, enforces strict FIFO tax-lot portfolio accounting with overselling prevention, and trains 5 actual econometric and deep learning models with zero data leakage.",
             "Furthermore, StockSense AI includes automated price alert triggers, VADER sentiment scoring on live financial headlines, a RAG-grounded AI copilot, and 19 automated platform tests passing cleanly.",
             "Be proud of the honest ML metrics. Emphasize that reporting a realistic 55-60% directional accuracy shows professional financial acumen over fake 99% claims."),

            ("Q5: How does data flow from an external market API to the user's browser?",
             "1. Client triggers a request via fetch() or page navigation. 2. Django URL router invokes the view. 3. The view calls `MarketDataService`. 4. The service checks `LocMemCache`. On a miss, it calls `yfinance.Ticker.history()`. 5. `TechnicalIndicatorService` computes rolling indicators in Pandas. 6. The service caches the result and returns it. 7. The view renders JSON or HTML with Plotly.js charts.",
             "To ensure low latency, quote snapshots are cached for 60 seconds and 2-year historical frames for 300 seconds. Repeat page loads return in under 10 milliseconds directly from memory.",
             "Don't forget to mention the caching layer. If you say you call Yahoo Finance on every single click, the interviewer will challenge you on rate-limiting."),

            ("Q6: How do you handle scalability if concurrent users increase 100x?",
             "I would scale the architecture horizontally: 1. Deploy multiple Django Gunicorn workers behind an Nginx load balancer. 2. Migrate the database to an AWS RDS PostgreSQL instance with read replicas. 3. Replace in-process LocMemCache with a distributed Redis cluster. 4. Offload heavy LSTM training to background Celery workers with a message broker.",
             "Currently, LSTM inference takes ~1.5 to 2.5 seconds using vectorized batch processing. Moving training to Celery workers with WebSockets (Django Channels) would prevent web worker thread blocking completely.",
             "Show that you understand the transition from development simplicity to production distributed systems."),

            ("Q7: Why did you choose SQLite for development and what is the production path?",
             "SQLite is serverless, zero-configuration, and file-based, making local development, schema migrations, and CI/CD test execution instantaneous. However, it lacks write concurrency (database-level locking).",
             "For production, Django's database engine is configured to PostgreSQL via environment variables (`DATABASE_URL`). PostgreSQL supports row-level locking, high concurrency, and advanced connection pooling (PgBouncer).",
             "Do not say 'SQLite is just a toy.' Emphasize that SQLite is fine for development and testing, and Django ORM allows switching to PostgreSQL by editing a single dictionary setting."),

            ("Q8: How did you structure your static files and frontend assets?",
             "I used Django's standard static files pipeline with `STATIC_URL = '/static/'` and `STATICFILES_DIRS`. Assets are organized into `/css`, `/js`, and `/img`. In production, WhiteNoise or Nginx serves these assets with cache-control headers and gzip/brotli compression.",
             "Templates are structured hierarchically: `base.html` provides the global responsive navbar, sidebar, theme toggles, and CSRF meta tags. Child templates extend `base.html` using `{% block content %}`.",
             "Explain that keeping CSS/JS modularized makes team collaboration clean and simplifies minification."),

            ("Q9: What is the purpose of the apps.analytics app?",
             "It is dedicated to technical indicator calculations and multi-factor stock screening. It computes Wilder's RSI, MACD, Bollinger Bands, Moving Averages, and ATR using pure vectorized Pandas/NumPy routines.",
             "It also provides screener endpoints where users can filter equities based on technical conditions, such as 'RSI < 30 (Oversold)' or 'Price > 50-day EMA (Bullish Trend)'.",
             "Make sure to highlight that indicators are computed on-the-fly rather than hardcoded in the database."),

            ("Q10: What is the purpose of the apps.assistant app?",
             "It provides the StockSense AI Copilot, a retrieval-augmented research assistant that helps investors analyze stocks and understand their portfolio risk.",
             "Instead of making up answers, `ResearchAssistantService` queries the user's active portfolio holdings and real-time market indicators, injects those facts into the context, and generates structured, grounded financial insights.",
             "Always emphasize that this is a RAG (Retrieval-Augmented Generation) pattern, which eliminates AI hallucinations of portfolio values."),

            ("Q11: How do you handle environment configurations between environments?",
             "Sensitive configurations like `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and database credentials are separated using environment variables or a `.env` file, loaded via `os.environ` or `python-dotenv`.",
             "In production, `DEBUG` is strictly set to `False`, `ALLOWED_HOSTS` is restricted to the specific domain, and secure cookie flags (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`) are enabled.",
             "Never admit to committing secret keys or database passwords to a public GitHub repository!"),

            ("Q12: What logging and monitoring strategies are implemented?",
             "The platform uses Python's standard `logging` library configured in Django's `LOGGING` dictionary. Key events, external API latency, cache misses, and ML training durations are logged at INFO and WARNING levels.",
             "When an external API like Yahoo Finance fails, the exception is caught, logged with stack traces via `logger.exception()`, and a graceful fallback response is returned to the user.",
             "Interviewers love seeing that you don't just use `print()` statements in a production codebase."),

            ("Q13: What is the role of Django REST Framework (DRF) in this project?",
             "DRF is used to build standardized, versioned RESTful JSON API endpoints alongside Django's server-rendered template views.",
             "It provides request validation, serializer classes that convert complex QuerySets into JSON, standard HTTP error responses, and authentication integration for API consumers.",
             "Explain that the platform supports both interactive browser UI (via Django templates) and programmatic API consumption (via DRF endpoints)."),

            ("Q14: How does the application handle time zones for international exchanges?",
             "Django is configured with `USE_TZ = True` and `TIME_ZONE = 'UTC'`. All timestamps in the database (transaction execution dates, prediction runs, news articles) are stored in timezone-aware UTC.",
             "When displaying dates on the frontend or processing daily OHLCV bars, timestamps are localized to the user's local timezone or the exchange's trading hours (IST for NSE, EST for US markets).",
             "Handling time zones properly is a classic senior-level consideration that impresses interviewers."),

            ("Q15: How did you ensure responsive UI design across desktop, tablet, and mobile?",
             "I used Bootstrap 5's 12-column mobile-first grid system combined with custom CSS media queries. Desktop displays show a dense, multi-pane financial terminal view, while tablets and smartphones collapse secondary panes into tabbed or off-canvas drawers.",
             "Plotly charts are configured with `responsive: true` and `autosize: true`, recalculating chart container dimensions whenever the browser viewport changes.",
             "Mention that financial users demand dense information on desktop screens, but clean readable cards on mobile devices.")
        ]
    },

    # -------------------------------------------------------------
    # CATEGORY 2: DJANGO BACKEND, MIDDLEWARE & AUTH (16-32)
    # -------------------------------------------------------------
    {
        "category": "Category 2: Django Framework, Middleware & Authentication",
        "questions": [
            ("Q16: How did you implement dual login allowing both username and email?",
             "I created a custom authentication backend named `EmailOrUsernameModelBackend` in `apps.accounts.backends` that inherits from `django.contrib.auth.backends.ModelBackend`.",
             "It overrides `authenticate(request, username=None, password=None, **kwargs)`. It executes `User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).first()`. If found, it calls `user.check_password(password)`. If valid, it returns the user object.",
             "Explain that default Django only allows username authentication; your custom backend transparently supports both."),

            ("Q17: Where and how do you configure your custom authentication backend in settings.py?",
             "In `settings.py`, I define the `AUTHENTICATION_BACKENDS` list, placing `'apps.accounts.backends.EmailOrUsernameModelBackend'` as the first entry, followed by `'django.contrib.auth.backends.ModelBackend'` as a fallback.",
             "When `django.contrib.auth.authenticate()` is invoked, Django iterates through `AUTHENTICATION_BACKENDS` in order until one returns an authenticated user or all fail.",
             "Demonstrates that you understand Django's pluggable authentication architecture."),

            ("Q18: What is PBKDF2-SHA256 and why is it used for passwords?",
             "PBKDF2 (Password-Based Key Derivation Function 2) with SHA-256 is Django's default password hasher. It applies 720,000 hashing iterations combined with a unique, cryptographically secure per-user salt.",
             "The high iteration count makes brute-force attacks and pre-computed rainbow table lookups computationally infeasible. Passwords are never stored or logged in plain text.",
             "Highlight the word 'salt' and 'work factor / iterations'. That shows true security comprehension."),

            ("Q19: How do user sessions persist across development server restarts?",
             "Sessions are stored in the database via `SESSION_ENGINE = 'django.contrib.sessions.backends.db'`, utilizing the `django_session` table. The cookie `sessionid` maps to the database record.",
             "Because session state is stored on disk in the database rather than in transient RAM, restarting `runserver` does not invalidate active user sessions.",
             "Explain how you diagnosed and verified this when fixing the demo trader login persistence issue."),

            ("Q20: What is Django Middleware and which middlewares are active in your platform?",
             "Middleware is a framework of hooks into Django's request/response processing cycle. Active middlewares include `SecurityMiddleware`, `SessionMiddleware`, `CommonMiddleware`, `CsrfViewMiddleware`, `AuthenticationMiddleware`, and `MessageMiddleware`.",
             "`AuthenticationMiddleware` associates the logged-in user with the `request.user` attribute, and `CsrfViewMiddleware` validates CSRF tokens on state-changing requests.",
             "Use the onion/pipeline analogy: requests pass through middleware layers before reaching the view, and responses pass back out in reverse order."),

            ("Q21: How does CSRF protection work in Django and in your fetch requests?",
             "Django generates a cryptographically secure random token linked to the user's session. In forms, `{% csrf_token %}` injects a hidden input. In asynchronous JavaScript `fetch()` calls, the script reads the `csrftoken` cookie and adds the `X-CSRFToken` HTTP header.",
             "On receiving a POST/PUT/DELETE request, `CsrfViewMiddleware` compares the header token with the session cookie. If they don't match, Django rejects the request with HTTP 403 Forbidden.",
             "Never say you used `@csrf_exempt` to bypass CSRF errors in production! Always show you pass `X-CSRFToken` properly."),

            ("Q22: How do you prevent unauthorized users from accessing portfolio and trade pages?",
             "Template views use Django's `@login_required(login_url='accounts:login')` decorator. API endpoints use DRF's `permission_classes = [IsAuthenticated]`.",
             "If an unauthenticated user attempts to view `/portfolio/`, Django redirects them to `/accounts/login/?next=/portfolio/`. After successful login, the user is redirected back to their intended page.",
             "Mention the `?next=` parameter—it proves you understand the user experience of authentication redirects."),

            ("Q23: How does the Demo Trader feature work in your login view?",
             "The login page provides a 'Use Demo Credentials' button that fills `demo_trader` and its password. If the user clicks login, the backend authenticates against the database.",
             "To ensure the demo account always exists, a custom migration or startup hook seeds the `demo_trader` user with an initial portfolio and sample transactions if absent.",
             "Explain that this was engineered specifically so interviewers and recruiters can test the platform without completing manual registration."),

            ("Q24: What is the UserProfile model and how is it linked to Django's built-in User?",
             "UserProfile is a custom model linked to `django.contrib.auth.models.User` via a `OneToOneField(User, on_delete=models.CASCADE, related_name='profile')`.",
             "It stores user-specific financial preferences such as `base_currency` ('INR' or 'USD'), `preferred_theme` ('dark' or 'light'), and `bio`. It is created automatically via a `post_save` Django signal when a new User is registered.",
             "Mentioning `post_save` signals for profile auto-creation is an immediate badge of Django competence."),

            ("Q25: What is the difference between a Django Form and a ModelForm?",
             "A `forms.Form` is a generic form class that manually defines fields and validation rules. A `forms.ModelForm` automatically creates fields and validation directly from an underlying Django model class.",
             "In StockSense AI, `TransactionForm` is a `ModelForm` tied to `Transaction`, inheriting field types, choices (BUY/SELL), and max lengths automatically from the database definition.",
             "Point out that ModelForms eliminate duplicate field definitions and keep code DRY."),

            ("Q26: How do you validate custom business rules in a Django Form?",
             "By overriding the `clean()` method or field-specific `clean_<fieldname>()` methods. In `TransactionForm`, the `clean_quantity()` method verifies that quantity is strictly greater than zero.",
             "The `clean()` method also checks if transaction_type == 'SELL' and verifies with `PortfolioAnalyticsService` that the user holds sufficient shares, raising a `forms.ValidationError` if overselling is attempted.",
             "Always explain that validation must occur on the backend—client-side HTML5 validation can be easily bypassed."),

            ("Q27: How does Django's message framework work in your templates?",
             "`django.contrib.messages` allows views to attach one-time notification messages (success, warning, error, info) to a request using `messages.success(request, 'Trade executed successfully!')`.",
             "In `base.html`, a template loop iterates over `{% for message in messages %}` and renders auto-dismissing Bootstrap toast notifications.",
             "Note that messages are stored in the session cookie and automatically cleared once displayed."),

            ("Q28: What is the difference between render() and JsonResponse() in Django?",
             "`render(request, template_name, context)` takes an HTML template, populates it with context variables, and returns an `HttpResponse` containing compiled HTML (Content-Type: text/html).",
             "`JsonResponse(data, status=200)` takes a Python dictionary or list, serializes it to JSON using `json.dumps()`, and returns an `HttpResponse` with Content-Type: application/json.",
             "Relate this to the bug you fixed: returning HTML instead of `JsonResponse` caused the frontend JSON parser to crash."),

            ("Q29: How do you manage static files and media files separately in Django?",
             "Static files (`STATIC_URL`, `STATICFILES_DIRS`) are developer-created assets (CSS, JS, logos) tracked in Git. Media files (`MEDIA_URL`, `MEDIA_ROOT`) are user-uploaded files (profile avatars) created dynamically at runtime.",
             "In development, `django.conf.urls.static.static()` serves media files. In production, media files are stored on AWS S3 or a persistent object storage volume.",
             "Clear distinction between static (code) and media (user-generated)."),

            ("Q30: How does Django's reverse() and {% url %} tag work?",
             "`reverse('app_name:view_name', kwargs={'symbol': 'TCS.NS'})` dynamically looks up the URL pattern defined in `urls.py` based on the route's name rather than hardcoding paths.",
             "If URL paths change from `/stocks/<symbol>/` to `/equities/<symbol>/`, no template or view code needs to be modified, preventing broken hyperlinks.",
             "Explain the importance of URL namespaces (`app_name = 'portfolio'`)."),

            ("Q31: What is the purpose of Django management commands and did you write any?",
             "Management commands are custom CLI scripts executed via `python manage.py <command_name>`. They inherit from `BaseCommand` and implement the `handle()` method.",
             "I created management commands for seeding historical stock symbols (`seed_stocks`) and pre-caching market data to ensure a smooth zero-setup experience for new developers.",
             "Custom management commands show deep familiarity with Django operational tooling."),

            ("Q32: How do you handle 404 Not Found and 500 Server Error pages gracefully?",
             "By defining custom error handlers (`handler404 = 'apps.market.views.custom_404_view'` and `handler500`). When `DEBUG = False`, Django automatically routes unhandled errors to these views.",
             "The custom templates render user-friendly guidance, a link back to the dashboard, and a search bar rather than a blank or scary crash page.",
             "Professional web platforms never expose raw stack traces to end users in production.")
        ]
    },

    # -------------------------------------------------------------
    # CATEGORY 3: DATABASE, ORM & PERFORMANCE (33-46)
    # -------------------------------------------------------------
    {
        "category": "Category 3: Database, Relational Modeling & ORM Performance",
        "questions": [
            ("Q33: Can you describe the relational database schema of StockSense AI?",
             "The database comprises 12 normalized models centered around User, Market, Portfolio, and Analytics. User links 1-to-1 with UserProfile. User links 1-to-Many with Portfolio, Watchlist, and PriceAlert. Portfolio links 1-to-Many with Transaction. Stock links 1-to-Many with HistoricalPrice, WatchlistItem, and PredictionRun.",
             "Referential integrity is maintained through foreign key cascade policies (`CASCADE` or `PROTECT`) and unique database constraints like `unique_together = ['stock', 'date']` on HistoricalPrice.",
             "Refer directly to Figure 5 from your architecture diagrams catalog."),

            ("Q34: What is the N+1 query problem and how did you eliminate it in your project?",
             "The N+1 problem occurs when an application executes 1 initial query to fetch N parent records, and then executes N separate queries inside a loop to fetch related child records, resulting in N+1 database queries.",
             "I eliminated it by using `select_related()` for forward ForeignKeys (e.g. `Transaction.objects.select_related('stock')`) and `prefetch_related()` for reverse relationships (e.g. `Portfolio.objects.prefetch_related('transactions')`). This reduces database roundtrips from O(N) to O(1).",
             "This is the single most common database question asked in Django interviews. Your answer here proves real backend experience."),

            ("Q35: What is the difference between null=True and blank=True in Django models?",
             "`null=True` is database-related: it allows the column to store SQL `NULL` values. `blank=True` is validation-related: it permits the field to be left empty in forms and the admin panel.",
             "For character fields (`CharField`, `TextField`), Django best practices recommend avoiding `null=True` unless strictly necessary, using `blank=True, default=''` to avoid having two representations of empty data (`NULL` vs empty string).",
             "Demonstrates adherence to official Django database style guidelines."),

            ("Q36: How does the Transaction ledger model enforce financial data integrity?",
             "`Transaction` stores immutable records of every trade with fields: `portfolio`, `stock`, `transaction_type` (BUY/SELL), `quantity`, `price`, `fees`, and `execution_date`.",
             "Instead of updating a single mutable `current_holdings` integer on the Stock or Portfolio model, positions are calculated deterministically by aggregating the immutable ledger. This provides a complete audit trail.",
             "In finance, mutable balances are dangerous. An immutable ledger of transactions is the gold standard."),

            ("Q37: How did you implement FIFO (First-In, First-Out) cost basis accounting?",
             "In `PortfolioAnalyticsService`, all BUY transactions for a stock are loaded into a chronological queue (deque). When a SELL transaction is processed, it consumes shares from the oldest available BUY lot first.",
             "Realized P&L is calculated as `(Sell Price - Matched Lot Cost) * Quantity`. Remaining shares in the queue represent open positions, and their weighted cost defines the accurate cost basis.",
             "Explain that without FIFO, calculating average costs when partial positions are sold leads to inaccurate tax and performance metrics."),

            ("Q38: How do you prevent negative share balances if a user tries to sell shares they don't own?",
             "Before any SELL transaction is committed, `PortfolioAnalyticsService.validate_sell()` calculates the currently held share quantity for that stock by summing past BUY quantities minus past SELL quantities.",
             "If `sell_quantity > current_shares_held`, a `ValidationError` is raised immediately, and the transaction is aborted before touching the database.",
             "Shows that business logic defends database invariants at the application layer."),

            ("Q39: What is django.db.transaction.atomic and where did you use it?",
             "`transaction.atomic` wraps database operations in a single database transaction block (`BEGIN ... COMMIT`). If an exception occurs, Django automatically executes a `ROLLBACK`.",
             "I used it when executing trades: deducting cash balance and creating the Transaction record occur inside `with transaction.atomic():`. This prevents inconsistent states where cash is deducted but no transaction is recorded.",
             "Mention the ACID properties of databases (Atomicity, Consistency, Isolation, Durability)."),

            ("Q40: How does the Stock model support multi-market symbols (NSE vs US)?",
             "The `Stock` model has fields `symbol`, `name`, `exchange` (choices: 'NSE', 'NASDAQ', 'NYSE'), and `currency` (choices: 'INR', 'USD').",
             "For NSE stocks, the symbol includes the `.NS` suffix (e.g., `TCS.NS`) which is required by Yahoo Finance. The display layer cleanly formats the ticker while preserving the exchange suffix internally.",
             "Explains why Indian stock symbols have `.NS` appended."),

            ("Q41: What is the purpose of the PredictionRun model?",
             "It acts as an audit log for every machine learning execution. It records `stock`, `model_type`, `forecast_horizon`, `mae`, `rmse`, `directional_accuracy`, `training_duration_seconds`, and execution `timestamp`.",
             "This allows the platform to render a historical ML leaderboard, showing which algorithms have performed best over time across different market regimes.",
             "Auditability in AI is a major enterprise requirement; having a model dedicated to it is very impressive."),

            ("Q42: What is the difference between on_delete=models.CASCADE and models.PROTECT?",
             "`CASCADE` automatically deletes child records when the referenced parent is deleted (e.g. deleting a User deletes their UserProfile and Portfolios).",
             "`PROTECT` raises a `ProtectedError` and prevents parent deletion if any child records reference it (e.g. preventing deletion of a Stock if historical transactions reference it).",
             "Explain that you use `PROTECT` on critical financial entities to prevent accidental data loss."),

            ("Q43: What are database indexes and which fields in your project are indexed?",
             "Database indexes are B-Tree data structures that allow the database engine to find matching rows in O(log N) time rather than scanning every row (O(N)).",
             "In StockSense AI, foreign keys are automatically indexed by Django. In addition, `Stock.symbol`, `HistoricalPrice.date`, and `Transaction.execution_date` are explicitly indexed via `db_index=True` for high-speed chronological filtering.",
             "Explaining O(log N) vs O(N) shows solid computer science fundamentals."),

            ("Q44: How do Django migrations work under the hood?",
             "Django inspects model definitions in `models.py` and compares them against previous migration files. `makemigrations` generates a Python file representing schema diffs.",
             "`migrate` executes the corresponding SQL DDL statements (`CREATE TABLE`, `ALTER TABLE`) and logs the applied migration name in the `django_migrations` table to prevent re-execution.",
             "Mention that migration files should be version-controlled in Git."),

            ("Q45: How would you handle a database migration rollback if a deployment fails?",
             "I can revert to a specific migration by running `python manage.py migrate <app_name> <target_migration_number>`. Django executes the reverse SQL operations to restore the previous schema state.",
             "Always verify that migrations define reversible operations and back up the database before executing production schema changes."),

            ("Q46: How do you perform complex database filtering using Q objects?",
             "`django.db.models.Q` objects allow constructing SQL queries with `OR` (`|`), `AND` (`&`), and `NOT` (`~`) logic.",
             "In my project, `Q(username__iexact=cred) | Q(email__iexact=cred)` is used in `EmailOrUsernameModelBackend` to search either column with a single SQL query: `WHERE UPPER(username) = UPPER(...) OR UPPER(email) = UPPER(...)`.",
             "Directly ties back to your verified source code implementation.")
        ]
    },

    # -------------------------------------------------------------
    # CATEGORY 4: MACHINE LEARNING & TIME-SERIES (47-65)
    # -------------------------------------------------------------
    {
        "category": "Category 4: Machine Learning, Time-Series & Econometrics",
        "questions": [
            ("Q47: Why is stock price prediction formulated as a supervised regression problem?",
             "Because the target variable is continuous (the future price in currency units). The pipeline constructs sliding window pairs $(X_t, y_t)$ where $X_t$ is a sequence of historical prices and $y_t$ is the price at $t+1$.",
             "The algorithm learns a mapping function $f: \mathbb{R}^{60} \rightarrow \mathbb{R}$ that minimizes prediction error on unseen test sequences.",
             "Emphasize continuous regression rather than discrete classification (UP/DOWN), although directional accuracy evaluates classification quality."),

            ("Q48: What is look-ahead bias / data leakage, and why is it fatal in financial ML?",
             "Data leakage occurs when information from the future is inadvertently leaked into the training data. In finance, this causes a model to perform exceptionally well on backtests but fail catastrophically in live trading.",
             "Common causes include fitting scalers on the full dataset, using future moving averages, or using random K-Fold cross validation that trains on future dates to predict past dates.",
             "This is the #1 question ML interviewers use to weed out candidates who just follow basic tutorials."),

            ("Q49: How does your TimeSeriesDataPipeline guarantee zero data leakage?",
             "1. Data is split strictly chronologically: first 80% for training, final 20% for testing. 2. The `MinMaxScaler` is fit ONLY on `train_data`. 3. Test and forecast data are transformed using the pre-fit scaler parameters.",
             "4. Sliding window sequences are constructed independently within each partition without bridging across the split boundary.",
             "Quote the exact rule: 'Fit on train, transform on test. Never fit on the whole dataset.'"),

            ("Q50: Why did you implement 5 different models instead of just one LSTM?",
             "In machine learning engineering, a complex deep neural network must always be justified against simpler, interpretable baselines. Evaluating Linear Regression, Random Forest, ARIMA, LSTM, and a Hybrid Ensemble side-by-side proves which architecture actually adds value.",
             "Linear Regression establishes the linear autoregressive baseline. ARIMA models stationary time-series dynamics. LSTM captures long-term non-linear sequences. The Hybrid combines the strengths of both.",
             "Shows professional engineering maturity: avoiding the temptation to blindly throw deep learning at every problem."),

            ("Q51: How does your Autoregressive Linear Regression baseline work?",
             "It treats the 60 lookback prices as 60 independent features: $\hat{y}_{t+1} = w_0 + w_1 y_t + w_2 y_{t-1} + \dots + w_{60} y_{t-59}$.",
             "It solves for the weight vector using Ordinary Least Squares (OLS) via Scikit-Learn. It runs in under 10 milliseconds and provides a reliable baseline benchmark.",
             "Explain that linear regression is extremely fast and resistant to overfitting on small datasets."),

            ("Q52: How is the Random Forest Regressor configured and regularized?",
             "It is configured as `RandomForestRegressor(n_estimators=50, max_depth=6, random_state=42)`. An ensemble of 50 decision trees aggregates predictions via bootstrap aggregating (bagging).",
             "Restricting `max_depth` to 6 is critical: unconstrained decision trees memorize historical price noise and achieve 0 training error while producing terrible out-of-sample test error.",
             "Highlight `max_depth=6` as explicit regularization against overfitting."),

            ("Q53: Why do you run ARIMA on log returns instead of raw prices?",
             "Raw prices are non-stationary: their mean and variance change over time (they trend). Classical ARIMA requires weak stationarity (constant mean, constant variance, and autocovariance that depends only on lag).",
             "Log returns, $r_t = \ln(P_t / P_{t-1})$, stabilize variance and remove linear trends. Once forecasted, prices are reconstructed using $P_{t+1} = P_t \cdot \exp(\hat{r}_{t+1})$.",
             "Mathematical justification: Stationarity is the foundational assumption of Box-Jenkins time-series modeling."),

            ("Q54: What does ARIMA(1, 1, 0) mean?",
             "AR(1): Autoregressive order 1 (the current value depends linearly on the immediate previous lag). I(1): Integrated order 1 (the series was differenced once to achieve stationarity). MA(0): Moving Average order 0 (no lagged white noise shock terms).",
             "The formula is: $(1 - \phi_1 B)(1 - B) y_t = \epsilon_t$, where $B$ is the backshift operator and $\epsilon_t$ is white noise.",
             "Knowing the exact mathematical definition of ARIMA parameters will stun interviewers."),

            ("Q55: What is the deep learning architecture of your Stacked LSTM?",
             "Layer 1: `LSTM(32 units, return_sequences=True, input_shape=(60, 1))`\nLayer 2: `Dropout(0.15)`\nLayer 3: `LSTM(32 units, return_sequences=False)`\nLayer 4: `Dropout(0.15)`\nLayer 5: `Dense(16, activation='relu')`\nLayer 6: `Dense(1, activation='linear')`.",
             "Trained using the Adam optimizer with a learning rate of 0.001 and Mean Squared Error (`mse`) loss over 15-20 epochs with a batch size of 32.",
             "Be ready to state the layer dimensions (32-32-16-1) effortlessly."),

            ("Q56: Why does Layer 1 have return_sequences=True while Layer 3 has return_sequences=False?",
             "When stacking LSTM layers, Layer 2 expects a 3D tensor input of shape `(batch_size, timesteps, features)`. Therefore, Layer 1 must return hidden states for all timesteps (`return_sequences=True`).",
             "Layer 3 connects to a standard Dense feedforward layer, which expects a 2D tensor `(batch_size, features)`. Therefore, Layer 3 returns only the final hidden state (`return_sequences=False`).",
             "This is a classic deep learning interview question testing whether you actually understand tensor dimensions."),

            ("Q57: How does an LSTM cell solve the vanishing gradient problem of standard RNNs?",
             "Standard RNNs multiply recurrent weight matrices across time steps, causing gradients to vanish or explode exponentially over long sequences. LSTMs introduce an internal Cell State ($C_t$) that acts as an error carousel.",
             "Information flows through the cell state with additive linear updates regulated by three non-linear gates: the Forget Gate ($f_t$), the Input Gate ($i_t$), and the Output Gate ($o_t$).",
             "Mention the three gates: Forget, Input, Output. Gradients flow additively along the cell state."),

            ("Q58: What is the mathematical formulation of your Hybrid LSTM-ARIMA Ensemble?",
             "Predictions are generated as a convex linear combination: $\hat{y}_{t}^{\text{hybrid}} = \alpha \cdot \hat{y}_{t}^{\text{LSTM}} + (1 - \alpha) \cdot \hat{y}_{t}^{\text{ARIMA}}$, where $\alpha \in [0.2, 0.8]$.",
             "The platform evaluates a candidate grid of $\alpha \in [0.20, 0.35, 0.50, 0.65, 0.80]$ on the held-out validation set and selects $\alpha^* = \arg\min_\alpha \text{MSE}(\alpha)$.",
             "This combines the non-linear feature extraction of deep learning with the linear econometric discipline of ARIMA."),

            ("Q59: How do you evaluate model performance on the held-out test split?",
             "I compute three complementary metrics: 1. Mean Absolute Error (MAE): raw error in currency units. 2. Root Mean Squared Error (RMSE): heavily penalizes large outlier blunders. 3. Directional Accuracy (%): percentage of trading days where the predicted direction (UP/DOWN) matched the actual market move.",
             "In financial trading, Directional Accuracy is often more critical than MAE because trading strategies depend on correct trend orientation.",
             "Always emphasize why having multiple metrics is essential in quantitative finance."),

            ("Q60: How does multi-step recursive forecasting work for the 30-day forecast horizon?",
             "To project 30 days into the future, the model uses walk-forward autoregression: it takes the last 60 actual prices to predict day $t+1$.",
             "For day $t+2$, it appends the predicted day $t+1$ to the window, drops the oldest observation, and predicts again. This loop repeats 30 times.",
             "Acknowledge the limitation: recursive forecasting causes error compounding over long horizons, which is why 30 days is a realistic upper bound."),

            ("Q61: What is Mean Absolute Error (MAE) and what was the typical MAE on TCS.NS?",
             "MAE is $(1/n)\sum |y_i - \hat{y}_i|$. On TCS.NS (trading around Rs 3,000-3,500), the models achieved a test MAE between Rs 25.00 and Rs 38.00, representing an average error of approximately 0.8% to 1.1%.",
             "This is an honest, realistic error margin for a liquid large-cap equity over held-out out-of-sample data.",
             "Stating concrete numbers from your actual tests shows you ran the code and verified the results."),

            ("Q62: What is Root Mean Squared Error (RMSE) and how does it compare to MAE?",
             "RMSE is $\sqrt{(1/n)\sum (y_i - \hat{y}_i)^2}$. Because errors are squared before averaging, RMSE is always greater than or equal to MAE.",
             "If the RMSE is significantly higher than the MAE, it indicates that the model produces occasional large outlier forecast errors.",
             "Shows that you understand the mathematical relationship between $L_1$ and $L_2$ error norms."),

            ("Q63: Can an AI model predict market crashes or black swan events?",
             "No. Machine learning models learn patterns from historical price distributions (autocorrelation, volatility clustering, and momentum).",
             "Black swan events (such as the COVID-19 shock or sudden geopolitical conflicts) are exogenous macroeconomic shocks that do not exist in prior training data. ML is a probabilistic risk-management tool, not a crystal ball.",
             "Interviewers love this honest, mature answer. It proves you understand the true nature of financial markets."),

            ("Q64: Why did you set random seeds in your ML pipelines?",
             "I set `np.random.seed(42)`, `tf.random.set_seed(42)`, and `random_state=42` in Scikit-Learn to guarantee reproducible results across training runs.",
             "Without fixed seeds, neural network weight initialization and Random Forest bootstrap sampling would produce slightly different validation metrics every time.",
             "Reproducibility is a fundamental pillar of scientific computing and production ML."),

            ("Q65: How do you avoid blocking the web server during deep learning training?",
             "In development, LSTM inference uses vectorized matrix operations in Keras (`model.predict(X_test, batch_size=64)`), which evaluates in under 2 seconds.",
             "For production scale, I designed the system so heavy training tasks can be offloaded to Celery background workers, with status polling or WebSockets notifying the frontend upon completion.",
             "Shows you understand the difference between synchronous HTTP request limits and asynchronous task workers.")
        ]
    },

    # -------------------------------------------------------------
    # CATEGORY 5: QUANTITATIVE FINANCE & INDICATORS (66-78)
    # -------------------------------------------------------------
    {
        "category": "Category 5: Quantitative Finance & Technical Indicators",
        "questions": [
            ("Q66: How is the Relative Strength Index (RSI) calculated in your project?",
             "RSI measures momentum on a 0-100 scale using Wilder's 14-period smoothing: $\text{RSI} = 100 - [100 / (1 + \text{RS})]$, where $\text{RS} = \text{Average Gain} / \text{Average Loss}$.",
             "In `TechnicalIndicatorService`, price differences are split into positive gains and negative losses. Wilder's exponential smoothing is applied using `ewm(alpha=1/14, adjust=False)`. Values above 70 indicate overbought; below 30 indicate oversold.",
             "Wilder's smoothing uses alpha=1/14, which differs from standard EMA alpha=2/(14+1). Mentioning this shows deep technical precision!"),

            ("Q67: What is the Moving Average Convergence Divergence (MACD)?",
             "MACD is a trend-following momentum indicator. It consists of: 1. MACD Line: 12-day EMA minus 26-day EMA. 2. Signal Line: 9-day EMA of the MACD Line. 3. Histogram: MACD Line minus Signal Line.",
             "When the MACD Line crosses above the Signal Line, it indicates bullish momentum; crossing below indicates bearish momentum.",
             "Explain the 12, 26, 9 standard parameters."),

            ("Q68: How are Bollinger Bands calculated and how do traders interpret them?",
             "Bollinger Bands consist of three lines: Middle Band = 20-period Simple Moving Average; Upper Band = Middle + 2*sigma; Lower Band = Middle - 2*sigma (where sigma is the 20-period standard deviation).",
             "The bands contain ~95% of price distribution under normal assumptions. Band contraction ('squeeze') signals impending volatility expansion; price piercing the upper band suggests overbought momentum.",
             "Mention 20 periods and 2 standard deviations."),

            ("Q69: What is the difference between a Simple Moving Average (SMA) and an Exponential Moving Average (EMA)?",
             "An SMA assigns equal weight to all $N$ periods: $(1/N)\sum P_i$. An EMA applies exponentially decaying weights, giving higher importance to the most recent prices.",
             "EMA reacts faster to recent price fluctuations, reducing lag: $\text{EMA}_t = \alpha \cdot P_t + (1 - \alpha) \cdot \text{EMA}_{t-1}$, where $\alpha = 2 / (N + 1)$.",
             "State the weighting multiplier formula: $\alpha = 2 / (N + 1)$."),

            ("Q70: How is the Average True Range (ATR) calculated?",
             "True Range is defined as $\max(\text{High} - \text{Low}, |\text{High} - \text{Close}_{\text{prev}}|, |\text{Low} - \text{Close}_{\text{prev}}|)$. ATR is the 14-period Wilder moving average of True Range.",
             "ATR measures absolute market volatility in price units, making it invaluable for setting stop-loss distances and position sizing.",
             "Highlight that ATR accounts for overnight price gaps between market sessions."),

            ("Q71: Why did you implement indicator calculations using Pandas vectorization?",
             "Pandas vectorization executes batch array operations in pre-compiled C code through NumPy, eliminating Python interpreter overhead.",
             "Calculating RSI and MACD across 2,000 historical bars takes under 2 milliseconds vectorized, compared to 100+ milliseconds using Python `for` loops.",
             "Vectorization is a primary benchmark of Python data engineering competency."),

            ("Q72: What is the Golden Cross and Death Cross in technical analysis?",
             "A Golden Cross occurs when a short-term moving average (e.g. 50-day SMA) crosses above a long-term moving average (e.g. 200-day SMA), signaling a long-term bullish trend.",
             "A Death Cross occurs when the 50-day SMA crosses below the 200-day SMA, signaling a long-term bearish trend. `TechnicalIndicatorService` generates automated crossover alert flags.",
             "50-day and 200-day moving average crossovers are followed by institutional investors worldwide."),

            ("Q73: How does the Multi-Factor Stock Screener work in your analytics app?",
             "The screener queries current technical indicators across the entire stock universe and allows users to apply composite multi-condition filters.",
             "For example, a user can filter for: 'RSI < 35 AND Price > 200-day SMA AND Daily Volume > 1,000,000' to discover fundamentally strong stocks experiencing a short-term oversold pullback.",
             "Shows how technical indicators directly power practical user workflows."),

            ("Q74: How do you handle market holidays and weekends when computing rolling windows?",
             "Financial time-series data only includes active trading days (Monday to Friday, excluding official exchange holidays). We index DataFrames by trading dates without zero-padding missing weekend days.",
             "Pandas `rolling(window=20)` operates on the 20 most recent active trading sessions, which corresponds to approximately one calendar month of trading.",
             "Emphasize that zero-filling weekend days would severely distort moving averages and volatility metrics."),

            ("Q75: What is the Sharpe Ratio and how could it be added to the portfolio analytics?",
             "The Sharpe Ratio measures risk-adjusted return: $(\bar{R}_p - R_f) / \sigma_p$, where $\bar{R}_p$ is the annualized portfolio return, $R_f$ is the risk-free rate, and $\sigma_p$ is portfolio standard deviation.",
             "It indicates whether a portfolio's returns are the result of smart asset allocation or excessive risk-taking.",
             "A Sharpe ratio > 1.0 is considered good; > 2.0 is very good; > 3.0 is excellent."),

            ("Q76: What is the difference between realized and unrealized P&L?",
             "Unrealized P&L (paper profit/loss) is the gain or loss on positions currently held, calculated as $(\text{Current Market Price} - \text{Cost Basis}) \times \text{Shares Held}$.",
             "Realized P&L is the actual profit or loss locked in when a position is sold: $(\text{Sell Price} - \text{FIFO Cost}) \times \text{Shares Sold}$. Realized P&L is taxable.",
             "Clear, textbook financial distinction."),

            ("Q77: How do you calculate portfolio asset allocation percentage?",
             "For each held position, the current market value is computed: $\text{Value}_i = \text{Quantity}_i \times \text{Current Price}_i$. Total Portfolio Equity is $\sum \text{Value}_i + \text{Cash Balance}$.",
             "Asset allocation percentage is $(\text{Value}_i / \text{Total Equity}) \times 100\%$, rendered as an interactive donut chart on the portfolio dashboard.",
             "Shows that your portfolio dashboard is dynamic and mathematically sound."),

            ("Q78: How does your PriceAlert model determine when to trigger an alert?",
             "PriceAlert records `target_price` and `condition` ('ABOVE' or 'BELOW'). When current quote data is ingested, `check_alerts()` compares current price with the target.",
             "If condition == 'ABOVE' and `current_price >= target_price`, or condition == 'BELOW' and `current_price <= target_price`, the alert status is updated to `TRIGGERED` and displayed to the user.",
             "Demonstrates state transitions in database models.")
        ]
    },

    # -------------------------------------------------------------
    # CATEGORY 6: FRONTEND, UI/UX & PLOTLY CHARTING (79-88)
    # -------------------------------------------------------------
    {
        "category": "Category 6: Frontend, UI/UX & Asynchronous Charting",
        "questions": [
            ("Q79: Why did you choose Plotly.js over Chart.js or D3.js?",
             "Plotly.js offers native, high-performance financial charting primitives—specifically `type: 'candlestick'` and `type: 'ohlc'`—with built-in range sliders, crosshairs, pan/zoom tools, and hover tooltips out of the box.",
             "Chart.js requires third-party plugins for financial candlestick rendering, while D3.js requires hundreds of lines of low-level SVG manipulation. Plotly strikes the perfect balance of power and maintainability.",
             "Highlight the specific financial chart types that Plotly natively supports."),

            ("Q80: How do you structure the dual-subplot financial chart in Plotly?",
             "I define a two-row subplot layout: Row 1 (80% height) displays the Candlestick price chart with 20/50 SMA overlay lines. Row 2 (20% height) displays color-coded trading volume bars (green for up days, red for down days).",
             "Both subplots share the same horizontal X-axis (dates), so zooming or panning the top chart automatically syncs the bottom volume chart.",
             "A shared X-axis dual subplot is standard institutional design (TradingView style)."),

            ("Q81: How do you handle asynchronous data loading in the frontend without freezing the UI?",
             "I use ES6 `async/await` with `fetch()`. When the user clicks 'Execute Model', a loading state is initiated: the button is disabled, a spinner appears, and a progress status message is displayed.",
             "When the promise resolves, the spinner is removed, the button is re-enabled, and the chart is rendered using `Plotly.newPlot()`. If an error occurs, a styled toast notification appears.",
             "Always explain the three states of async UI: Loading, Success, Error."),

            ("Q82: How do you prevent DOM manipulation vulnerabilities like XSS in your JavaScript?",
             "I avoid `element.innerHTML = untrustedInput`. Instead, I use `element.textContent = data`, or dynamically create elements using `document.createElement()` and `element.appendChild()`.",
             "In Django templates, the template engine automatically escapes all `{{ variable }}` tags by default unless explicitly bypassed with `|safe`.",
             "Demonstrates sound web security hygiene on the frontend."),

            ("Q83: What is the purpose of the theme toggle (Dark / Light mode)?",
             "Financial traders frequently work long hours in dark environments and prefer dark themes to reduce eye strain. StockSense AI implements a CSS variable-based theming architecture.",
             "The user's preference is saved in the `UserProfile.preferred_theme` database field and also cached in browser `localStorage`, ensuring instant theme application before HTML body render to avoid theme flickering.",
             "Mentioning localStorage theme caching to prevent FOUC (Flash of Unstyled Content) is a great senior touch."),

            ("Q84: How do you format numbers and currencies in the UI?",
             "Prices and currency amounts are formatted using JavaScript's `Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' })` for Indian equities, and `'en-US'` for US equities.",
             "This formats numbers with proper comma grouping (e.g. `Rs 3,24,500.00` in the Indian numbering system vs `$324,500.00` in the US system).",
             "Handling Indian vs International number systems shows great attention to detail."),

            ("Q85: How do the time-range toggles (1M, 3M, 6M, 1Y, 5Y) work on the Stock Explorer?",
             "When the user clicks a range button, the frontend makes an asynchronous fetch request to `/api/market/history/?symbol=TCS.NS&period=6m`.",
             "The backend filters the historical DataFrame, recalculates the indicators for that window, and returns updated JSON. Plotly updates the existing chart using `Plotly.react()`, which is significantly faster than re-creating the entire DOM canvas.",
             "Mentioning `Plotly.react()` demonstrates performance optimization."),

            ("Q86: How does the AI Copilot chat interface handle scrolling and multi-turn conversation?",
             "The chat message container uses `overflow-y: auto`. Whenever a new message is appended (either by user or assistant), JavaScript automatically scrolls to the bottom using `chatContainer.scrollTop = chatContainer.scrollHeight`.",
             "Each message is rendered in a distinct bubble: user questions aligned to the right, AI responses aligned to the left with markdown formatting and copy-code buttons.",
             "Standard, elegant messaging UI pattern."),

            ("Q87: How does your UI handle empty states (e.g., empty portfolio or empty watchlist)?",
             "Instead of displaying an empty blank table or a broken chart, the template checks `{% if holdings %}`. If empty, it renders an informative empty state illustration.",
             "The empty state provides a clear Call to Action (CTA): 'No transactions recorded yet. Click [Record First Trade] to start tracking your portfolio.'",
             "Good UX design always guides the user when data is absent."),

            ("Q88: Why did you use Bootstrap 5 instead of Tailwind or custom CSS?",
             "Bootstrap 5 dropped the jQuery dependency and is written in pure vanilla JavaScript and CSS custom properties. It provides solid, battle-tested grid layouts, modals, and responsive tables without extensive build tooling like Node/PostCSS.",
             "For a Python full-stack developer portfolio, Bootstrap 5 keeps backend and frontend integration clean, fast, and free of heavyweight NPM dependency chains.",
             "Shows pragmatic architectural judgment: choosing tools that match project scope.")
        ]
    },

    # -------------------------------------------------------------
    # CATEGORY 7: API DESIGN, SECURITY & DEFENSIVE CODE (89-100)
    # -------------------------------------------------------------
    {
        "category": "Category 7: API Design, Security & Defensive Engineering",
        "questions": [
            ("Q89: What was the root cause of the 'SyntaxError: Unexpected token <' error and how did you debug it?",
             "When the ML 'Execute Model' button was clicked, the frontend called the endpoint expecting JSON. However, the endpoint encountered an unhandled exception or authentication redirect (HTTP 302/500), returning an HTML error page starting with `<!DOCTYPE html>`.",
             "The frontend JavaScript executed `await response.json()` unconditionally. Because the response was HTML rather than JSON, the JSON parser encountered the leading `<` bracket and threw `SyntaxError: Unexpected token '<'`.",
             "This was the exact bug debugged in the project session. Reciting this demonstrates authentic troubleshooting."),

            ("Q90: What exact changes did you make to fix that bug?",
             "1. Backend: Wrapped prediction execution in `try-except` blocks, returning `JsonResponse({'success': False, 'error': str(e)}, status=400/500)` so errors are always valid JSON.",
             "2. Frontend: Updated fetch handling to check `if (!response.ok)` and verify `response.headers.get('content-type')?.includes('application/json')` before calling `response.json()`. If HTML is returned, it extracts `response.text()` and shows a friendly toast error.",
             "Always show both sides: fixing the backend response contract AND making the frontend defensively resilient."),

            ("Q91: What are HTTP status codes and what does each range mean?",
             "1xx: Informational. 2xx: Success (200 OK, 201 Created). 3xx: Redirection (301 Moved, 302 Found). 4xx: Client Error (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found). 5xx: Server Error (500 Internal Server Error, 502 Bad Gateway).",
             "In our API, validation failures return 400, missing equities return 404, and unauthenticated requests return 401.",
             "Fundamental web architecture knowledge that every full-stack candidate must know."),

            ("Q92: How does your application protect against SQL Injection?",
             "All database queries use Django's ORM, which parameterizes all query arguments automatically under the hood.",
             "For example, `Stock.objects.filter(symbol=user_input)` compiles to `SELECT ... WHERE symbol = %s` with values passed separately to the database driver, preventing user input from escaping into the SQL grammar.",
             "Explain that raw SQL queries with string formatting (`f'SELECT * WHERE symbol = {user_input}'`) are strictly banned in the codebase."),

            ("Q93: How do you prevent Cross-Site Scripting (XSS) attacks?",
             "1. Django template auto-escaping automatically converts `<`, `>`, `&`, `\"`, and `'` into HTML entities (`&lt;`, `&gt;`). 2. In JavaScript, all dynamic values are set via `textContent` rather than `innerHTML`.",
             "3. The HTTP `X-Content-Type-Options: nosniff` header is enforced via Django's `SecurityMiddleware`.",
             "Mention both template escaping and JavaScript DOM property best practices."),

            ("Q94: What is Cross-Site Request Forgery (CSRF) and how does Django stop it?",
             "CSRF is an attack where a malicious website tricks a user's browser into submitting unauthorized requests to a site where the user is already authenticated.",
             "Django uses the Synchronizer Token Pattern: a secret CSRF token is stored in the user's cookie and must be submitted alongside state-changing requests (POST/PUT/DELETE) in headers or forms. Malicious cross-origin sites cannot read this token due to the Same-Origin Policy.",
             "Mention the Same-Origin Policy—it explains WHY the attacker cannot forge the token."),

            ("Q95: What are the security settings required for deploying Django to production?",
             "`DEBUG = False`, `SECRET_KEY = os.environ['SECRET_KEY']`, `ALLOWED_HOSTS = ['yourdomain.com']`, `SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True`, `SECURE_BROWSER_XSS_FILTER = True`, and `SECURE_SSL_REDIRECT = True`.",
             "Enabling `SECURE_SSL_REDIRECT` forces all HTTP traffic to HTTPS, and `COOKIE_SECURE` flags ensure cookies are only transmitted over encrypted TLS connections.",
             "Reciting these settings demonstrates production readiness."),

            ("Q96: How does LocMemCache prevent denial of service and API rate limits?",
             "Yahoo Finance and news endpoints throttle clients that make excessive requests. `MarketDataService` caches ticker quotes for 60 seconds and historical data for 300 seconds.",
             "If 100 users open the TCS page within one minute, only the first request queries Yahoo Finance; the remaining 99 are served directly from RAM in < 5ms.",
             "Connect caching directly to API rate-limit defense."),

            ("Q97: How do you serialize Django model instances into JSON?",
             "In Django REST Framework, we use `ModelSerializer` classes (e.g. `TransactionSerializer`). It defines the model, fields to expose, and custom serialization methods (e.g. `get_total_cost`).",
             "In plain Django views, we use `list(queryset.values('symbol', 'name'))` or `json.dumps()` with a custom encoder for Decimal and DateTime types.",
             "Explain that Python's standard `json.dumps()` cannot serialize Decimal or DateTime objects without a custom encoder."),

            ("Q98: What is CORS (Cross-Origin Resource Sharing) and when is it needed?",
             "CORS is a browser security mechanism that restricts web pages from making HTTP requests to a different domain, port, or protocol than the one that served the page.",
             "If our Django backend serves an external mobile app or a separate React/Vue frontend on a different port (e.g. localhost:3000), we install `django-cors-headers` and configure `CORS_ALLOWED_ORIGINS`.",
             "Demonstrates understanding of decoupled frontend/backend architectures."),

            ("Q99: How do you handle input validation on the backend?",
             "Every input is validated through multiple layers: 1. URL pattern type constraints (`<str:symbol>`, `<int:pk>`). 2. Form and Serializer field validators (e.g., `MinValueValidator(1)` on quantity).",
             "3. Model-level `clean()` methods. 4. Service-level business validation (verifying sufficient share balance before executing a sale).",
             "Defense in depth: never rely on a single validation layer."),

            ("Q100: How do you manage database connections in Django?",
             "Django automatically opens a database connection when a query is executed and closes it when the request completes. With `CONN_MAX_AGE` configured (e.g. 60 seconds), Django maintains persistent connections across multiple requests.",
             "Persistent connections eliminate the overhead of establishing a new TCP/TLS connection for every HTTP request, significantly improving throughput.",
             "Mentioning `CONN_MAX_AGE` is an advanced Django optimization technique.")
        ]
    },

    # -------------------------------------------------------------
    # CATEGORY 8: BEHAVIORAL & PORTFOLIO DEFENSE (101-110)
    # -------------------------------------------------------------
    {
        "category": "Category 8: Behavioral, Project Defense & Tricky Scenarios",
        "questions": [
            ("Q101: What was the most challenging technical obstacle you faced in this project?",
             "Migrating from a legacy Flask prototype to a clean, 8-app Django architecture while eliminating data leakage in the ML forecasting pipeline.",
             "Synchronizing the differenced stationary ARIMA predictions with the scaled multi-step sequence outputs of the LSTM, while ensuring that the MinMaxScaler was fit exclusively on the chronological training split without look-ahead bias, required deep architectural precision.",
             "Frame technical challenges around engineering decisions and mathematical integrity."),

            ("Q102: If an interviewer asks: 'Why not use XGBoost or Prophet for forecasting?'",
             "XGBoost and Prophet are excellent tabular and additive time-series tools. In my project, I prioritized ARIMA for classical econometric modeling and stacked LSTM for sequence modeling.",
             "Because of the modular Strategy pattern in `ForecastingService`, adding an `XGBoostForecastingStrategy` would only require writing a new class implementing the `train_and_predict()` interface, without changing any frontend or API code.",
             "Always show how your software design makes future extensions effortless."),

            ("Q103: How do you respond if an interviewer claims: 'Stock markets are a random walk; your ML models are useless'?",
             "I agree with the Efficient Market Hypothesis (EMH) that stock prices have strong random-walk components. That is exactly why I built an honest platform that reports real test MAE and directional accuracy rather than fake 99% accuracy claims.",
             "Our models do not claim to predict random future shocks; they capture short-term autoregressive autocorrelation and mean-reversion tendencies. Furthermore, the platform integrates technical indicators and sentiment analysis to provide multi-dimensional intelligence rather than relying on ML alone.",
             "Agree with the interviewer's premise while intelligently defending the value of quantitative intelligence."),

            ("Q104: How did you test your project to ensure nothing broke?",
             "I wrote 19 comprehensive unit and integration tests in `tests/test_platform.py` using Django's `TestCase` framework.",
             "Tests verify user registration, dual login, portfolio trades, overselling prevention, watchlist CRUD operations, market data caching, and ML prediction API response structures. All 19 tests pass cleanly.",
             "Testing is what separates amateur projects from production-grade portfolio projects."),

            ("Q105: How did you manage Git version control during development?",
             "I followed a feature-branch workflow. Main branches remained stable, while new features (e.g. `feature/ml-forecasting`, `feature/auth-refactor`) were developed on dedicated branches.",
             "Commits were made atomic with clear, descriptive commit messages following the Conventional Commits specification (e.g. `feat: add hybrid ensemble grid search`, `fix: ensure prediction API returns valid JSON`).",
             "Demonstrates professional Git hygiene."),

            ("Q106: What did you learn about software architecture from building StockSense AI?",
             "I learned that separating domain business logic from web controllers (views) is the most critical architectural decision in a growing codebase.",
             "Early in development, views that directly called mathematical routines were difficult to debug and test. Moving that logic into dedicated service classes made unit testing trivial and enabled seamless reuse across both HTML views and REST APIs.",
             "A profound architectural reflection that interviewers love to hear from freshers."),

            ("Q107: How would you explain your project to a non-technical interviewer (HR or Product Manager)?",
             "StockSense AI is like an intelligent digital assistant for stock investors. If you want to invest in TCS or Apple, our platform brings together real-time prices, company news, and technical health checks into one clean screen.",
             "It also keeps track of your personal investments, calculates whether you made a profit using standard accounting rules, and runs computer models that analyze past price trends to show possible future scenarios with complete transparency.",
             "Demonstrates the crucial ability to communicate technical complexity in simple, business-friendly terms."),

            ("Q108: If you had another 3 months to work on this, what features would you add?",
             "1. Integrate Celery and Redis for asynchronous background model training and WebSocket price streaming. 2. Connect to paper-trading broker APIs (like Zerodha Kite or Alpaca) for live simulated order execution.",
             "3. Implement automated Backtesting of technical trading rules (e.g., testing RSI + MACD crossover strategies across 5 years of historical data). 4. Add portfolio Monte Carlo risk simulation for Value at Risk (VaR) calculations.",
             "Shows ambition, a clear product roadmap, and quantitative curiosity."),

            ("Q109: What makes you a strong candidate for a Full Stack Python / Django role?",
             "I don't just write scripts; I design full-stack systems. StockSense AI proves I can architect clean Django models, write custom authentication backends, optimize database queries to avoid N+1 bottlenecks, build REST APIs, and integrate complex data science and machine learning pipelines.",
             "Most importantly, I take craftsmanship seriously: I write automated tests, handle edge cases defensively, document architecture rigorously, and care deeply about both user experience and backend performance.",
             "The perfect closing interview statement."),

            ("Q110: Do you have any questions for the engineering team?",
             "Yes: 1. What does your current CI/CD deployment pipeline look like, and how often do you ship to production? 2. How does your engineering team approach the balance between synchronous web workloads and background asynchronous task workers?",
             "3. What are the biggest architectural challenges your platform is currently facing as user traffic scales?",
             "Always have smart, engineering-focused questions prepared for the end of the interview!")
        ]
    }
]

def build_interview_qa_pdf():
    print(f"Building 100+ Interview Q&A PDF: {OUTPUT_PATH}")
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=32,
        bottomMargin=32
    )

    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        'QATitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=24, leading=28,
        textColor=NAVY, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'QASubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=12, leading=16,
        textColor=SECONDARY, spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        'CatHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=13, leading=17,
        textColor=NAVY, spaceBefore=12, spaceAfter=6, keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'QuestionTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=13.5,
        textColor=NAVY, spaceBefore=6, spaceAfter=2, keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'AnsShort', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=DARK_TEXT, spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        'AnsDeep', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=11.5,
        textColor=BODY_TEXT, spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        'PitfallText', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=7.5, leading=11,
        textColor=colors.HexColor('#9A3412'), spaceAfter=4
    ))

    story = []

    # ==================== COVER PAGE ====================
    story.append(Spacer(1, 30))
    story.append(Paragraph("StockSense AI", styles['QATitle']))
    story.append(Paragraph("110 Categorized Technical Interview Questions & Model Answers", styles['QASubtitle']))
    story.append(HRFlowable(width="100%", thickness=2, color=SECONDARY, spaceBefore=2, spaceAfter=12))

    intro_desc = (
        "<b>Exhaustive Technical Interview Preparation Manual for Python Full Stack & AI/ML Roles:</b><br/>"
        "This compendium contains 110 real-world, categorized technical interview questions meticulously structured "
        "around the actual StockSense AI production codebase. Each entry provides a <b>Concise 15-Second Direct Answer</b> (for immediate delivery), "
        "a <b>Deep-Dive Technical Explanation</b> (referencing exact classes, mathematical equations, and architectural patterns), "
        "and an <b>Interviewer Trap / Pitfall Warning</b> (highlighting common fresher misconceptions and how to avoid them)."
    )
    t_intro = Table([[Paragraph(intro_desc, styles['AnsShort'])]], colWidths=[letter[0]-72])
    t_intro.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CALLOUT_BG),
        ('BOX', (0,0), (-1,-1), 1, SECONDARY),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_intro)
    story.append(Spacer(1, 10))

    # Category Index Matrix
    cat_summary = [
        [Paragraph("<b>Category Index</b>", styles['AnsShort']), Paragraph("<b>Domain Scope & Core Topics Covered</b>", styles['AnsShort'])],
        [Paragraph("<b>1. System Architecture (Q1-15)</b>", styles['AnsShort']), Paragraph("4-Tier architecture, 8 modular apps, service layer pattern, caching, scalability.", styles['AnsShort'])],
        [Paragraph("<b>2. Django Backend & Auth (Q16-32)</b>", styles['AnsShort']), Paragraph("Dual login backend, PBKDF2 hashing, persistent sessions, middleware, CSRF security.", styles['AnsShort'])],
        [Paragraph("<b>3. Database & ORM (Q33-46)</b>", styles['AnsShort']), Paragraph("12 normalized models, zero-N+1 prefetching, FIFO cost accounting, atomicity.", styles['AnsShort'])],
        [Paragraph("<b>4. Machine Learning & Math (Q47-65)</b>", styles['AnsShort']), Paragraph("Zero data leakage, 80/20 split, Linear Regression, Random Forest, ARIMA, LSTM, Hybrid.", styles['AnsShort'])],
        [Paragraph("<b>5. Quantitative Finance (Q66-78)</b>", styles['AnsShort']), Paragraph("Wilder RSI 14, MACD, Bollinger Bands, ATR, multi-factor screener, portfolio metrics.", styles['AnsShort'])],
        [Paragraph("<b>6. Frontend & UI/UX (Q79-88)</b>", styles['AnsShort']), Paragraph("Plotly.js financial subplots, async fetch, theme caching, responsive layout.", styles['AnsShort'])],
        [Paragraph("<b>7. API & Defensive Code (Q89-100)</b>", styles['AnsShort']), Paragraph("SyntaxError debugging, HTTP contracts, XSS/SQLi defense, REST serializers.", styles['AnsShort'])],
        [Paragraph("<b>8. Behavioral & Defense (Q101-110)</b>", styles['AnsShort']), Paragraph("Obstacle handling, non-technical translation, testing, why hire me closing pitch.", styles['AnsShort'])],
    ]
    t_cat = Table(cat_summary, colWidths=[160, letter[0]-72-160])
    t_cat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_cat)
    story.append(PageBreak())

    # ==================== QUESTIONS LOOP ====================
    for cat_data in QA_DATABASE:
        cat_title = cat_data["category"]
        story.append(Paragraph(esc(cat_title), styles['CatHeader']))
        story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=2, spaceAfter=6))

        for item in cat_data["questions"]:
            if len(item) >= 4:
                q_title, ans_short, ans_deep, pitfall = item[0], item[1], item[2], item[3]
            elif len(item) == 3:
                q_title, ans_short, ans_deep = item[0], item[1], item[2]
                pitfall = "Demonstrate solid architectural reasoning and ground your answer in verified production code."
            else:
                continue

            q_flowables = []
            q_flowables.append(Paragraph(f"<b>{esc(q_title)}</b>", styles['QuestionTitle']))
            q_flowables.append(Paragraph(f"<b>Direct Answer:</b> {esc(ans_short)}", styles['AnsShort']))
            q_flowables.append(Paragraph(f"<b>Technical In-Depth:</b> {esc(ans_deep)}", styles['AnsDeep']))
            q_flowables.append(Paragraph(f"<b>Pitfall / Trap to Avoid:</b> {esc(pitfall)}", styles['PitfallText']))
            q_flowables.append(Spacer(1, 3))
            story.append(KeepTogether(q_flowables))

        story.append(Spacer(1, 6))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {OUTPUT_PATH}")

if __name__ == '__main__':
    build_interview_qa_pdf()
