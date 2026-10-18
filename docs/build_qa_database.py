"""
StockSense AI - Comprehensive 235+ Interview Question Bank Compiler
Generates docs/qa_bank.py with questions, simple answers, technical explanations, and examples.
"""

import os
import json

QA_DATA = {
    "Basic": [
        ("What is StockSense AI in one sentence?",
         "StockSense AI is a full-stack financial intelligence platform that unifies market analytics, algorithmic forecasting, news sentiment, and portfolio management.",
         "It integrates real-time equity data from Indian and US markets, computes quantitative indicators, applies 5 machine learning models, and tracks portfolio positions with FIFO cost basis.",
         "Example: An investor can search 'TCS.NS', view interactive candlestick charts with RSI/MACD, run a 30-day LSTM forecast, check VADER news sentiment, and record a buy order."),

        ("What programming language is the backend built in?",
         "The backend is built entirely in Python (version 3.13) utilizing Django 5.0.",
         "Python was chosen for its mature ecosystem in data science, machine learning (TensorFlow, Scikit-learn, Statsmodels), and robust web development capabilities.",
         "Example: Pandas handles dataframe manipulation, NumPy computes indicators, and Django manages ORM and HTTP routing."),

        ("What web framework did you use and why?",
         "I used Django 5.0, a high-level Python web framework.",
         "Django provides an 'out-of-the-box' architecture with an ORM, authentication system, CSRF protection, and clean modular structure, reducing boilerplate code.",
         "Example: Django's authentication system and ORM allowed implementing secure user sessions and database models with minimal custom infrastructure."),

        ("What database is used in your project?",
         "SQLite is used for local development and testing, with full compatibility for PostgreSQL in production.",
         "SQLite is a serverless, zero-configuration file-based database ideal for local development, while Django's database abstraction layer makes switching to PostgreSQL a single setting change.",
         "Example: Settings use `DATABASE_URL` via python-dotenv to switch from `db.sqlite3` to PostgreSQL on cloud platforms like Render or AWS."),

        ("What frontend technologies did you use?",
         "HTML5, CSS3, Vanilla JavaScript (ES6+), Bootstrap 5, Lucide icons, and Plotly.js.",
         "I avoided heavy single-page application frameworks like React to keep the architecture cohesive within Django's MVT pattern while utilizing Plotly.js for hardware-accelerated interactive charting.",
         "Example: Chart renders are dynamically populated via asynchronous Fetch API calls to Django REST endpoints."),

        ("What is the primary objective of this project?",
         "To solve information fragmentation and provide retail investors with honest, auditable financial intelligence.",
         "Most retail tools either scatter data across multiple sites or show fabricated '99% accurate' black-box AI predictions. StockSense AI provides verifiable metrics with zero data leakage.",
         "Example: Forecasting models report walk-forward MAE and RMSE rather than unrealistic guaranteed price promises."),

        ("What markets does your platform support?",
         "Both Indian equities (NSE and BSE) and US equities (NASDAQ and NYSE), as well as benchmark ETFs.",
         "Tickers like TCS.NS, RELIANCE.NS, and INFY.NS are supported alongside AAPL, MSFT, and NVDA, with dual-currency handling (INR and USD).",
         "Example: Indian equities display prices in INR (₹) and US stocks in USD ($)."),

        ("How does a user log in to the application?",
         "Users log in using either their registered username or email address along with their password.",
         "Authentication is handled by a custom Django authentication backend (`EmailOrUsernameModelBackend`) that verifies passwords using PBKDF2-SHA256 hashing.",
         "Example: A user can enter either `demo_trader` or `trader@stocksense.ai` with `StockSense@2026` to authenticate."),

        ("What is a stock ticker symbol?",
         "A unique series of letters representing a publicly traded company on an exchange.",
         "For Indian stocks on the National Stock Exchange, symbols end with `.NS` (e.g., `TCS.NS`), while US stocks use plain tickers (e.g., `AAPL`).",
         "Example: `RELIANCE.NS` represents Reliance Industries Limited on the NSE."),

        ("What is candlestick charting?",
         "A financial chart style displaying Open, High, Low, and Close (OHLC) prices for a specific time interval.",
         "Green/white candles represent periods where the closing price was higher than the opening price, while red/black candles represent price declines.",
         "Example: In StockSense AI, Plotly.js renders interactive OHLC candlesticks with volume bars on a synchronized subplot."),

        ("What is a moving average?",
         "A technical indicator that smooths price data by creating a constantly updated average price over a specific window.",
         "A Simple Moving Average (SMA) weights all days equally, while an Exponential Moving Average (EMA) applies more weight to recent prices.",
         "Example: The 50-day SMA crossing above the 200-day SMA is a classic bullish 'Golden Cross' signal."),

        ("What is RSI (Relative Strength Index)?",
         "A momentum oscillator that measures the speed and change of price movements on a scale from 0 to 100.",
         "Values above 70 typically indicate an overbought condition, while values below 30 indicate an oversold condition.",
         "Example: StockSense AI calculates 14-period RSI using Wilder's smoothing technique."),

        ("What is MACD?",
         "Moving Average Convergence Divergence: a trend-following momentum indicator showing the relationship between two EMAs.",
         "It consists of the MACD line (12 EMA minus 26 EMA), the signal line (9 EMA of MACD), and a histogram showing the difference.",
         "Example: When the MACD line crosses above the signal line, it suggests upward momentum."),

        ("What is machine learning in simple terms?",
         "Algorithms that learn patterns from historical data to make predictions without being explicitly programmed with fixed rules.",
         "In financial forecasting, ML models analyze historical price patterns, volume, and technical indicators to project probable future price trajectories.",
         "Example: StockSense AI trains models on 2 years of daily trading data to forecast the next 7, 14, or 30 days."),

        ("What is sentiment analysis?",
         "Natural Language Processing (NLP) technique to determine whether a text expresses a positive, negative, or neutral tone.",
         "In finance, news sentiment reveals how the media views a company's prospects, earnings, or management actions.",
         "Example: 'TCS reports 2.7% revenue growth' is scored as positive, while 'Citi cuts target' is scored as negative."),

        ("What is a REST API?",
         "An architectural style for network communication using standard HTTP methods like GET, POST, PUT, and DELETE.",
         "StockSense AI uses Django REST Framework to expose JSON endpoints for stock quotes, indicator values, predictions, and news.",
         "Example: `GET /api/stocks/TCS.NS/` returns a JSON object containing current price, change, volume, and company details."),

        ("What is the difference between GET and POST requests?",
         "GET retrieves data from a server without modifying state, while POST sends data to create or update server-side resources.",
         "GET requests are idempotent and can be bookmarked/cached, whereas POST requests typically include a body and CSRF protection.",
         "Example: `/api/predictions/TCS.NS/` uses GET to retrieve forecasts, while `/api/portfolio/transactions/` uses POST to execute trades."),

        ("What is CSRF and how does Django protect against it?",
         "Cross-Site Request Forgery is an attack that tricks authenticated users into executing unwanted actions.",
         "Django generates a unique CSRF token per user session that must be submitted with every state-changing POST/PUT request.",
         "Example: Django templates include `{% csrf_token %}` inside forms, and AJAX requests pass the `X-CSRFToken` header."),

        ("What is an ORM?",
         "Object-Relational Mapping: a technique that lets you query and manipulate a database using object-oriented code instead of raw SQL.",
         "Django ORM maps Python classes to database tables and instances to rows.",
         "Example: `Stock.objects.filter(is_active=True)` compiles to `SELECT * FROM market_stock WHERE is_active = 1`."),

        ("What is a virtual environment in Python?",
         "An isolated environment that keeps dependencies required by different projects separate from each other and the global Python installation.",
         "It prevents package version conflicts and ensures project reproducibility.",
         "Example: Created using `python -m venv venv` and activated using `venv\\Scripts\\activate` on Windows.")
    ],

    "Intermediate": [
        ("Explain the MVT architecture of Django.",
         "MVT stands for Model-View-Template: Model defines database structure, View handles logic and renders templates, and Template manages HTML presentation.",
         "Django's View corresponds to the Controller in traditional MVC, while the Template corresponds to the View. In StockSense AI, we also add a decoupled Service layer.",
         "Example: `models.py` holds `Stock`, `views.py` coordinates HTTP requests, and `templates/market/explorer.html` presents the data."),

        ("How does the Service Layer pattern improve Django applications?",
         "It extracts complex business and mathematical algorithms out of views and models into dedicated, testable service classes.",
         "In StockSense AI, classes like `MarketDataService`, `ForecastingService`, and `PortfolioAnalyticsService` encapsulate domain logic.",
         "Example: `ForecastingService` can be executed from a web view, a REST API, a test suite, or a CLI command without altering a single line of logic."),

        ("How does StockSense AI prevent API rate-limiting from Yahoo Finance?",
         "By implementing an in-memory caching layer (`LocMemCache`) with tiered TTL (Time-To-Live) expirations.",
         "Current quotes are cached for 60 seconds, historical daily frames for 300 seconds, and news feeds for 300 seconds. Repeat user requests hit memory rather than external networks.",
         "Example: When 10 users view TCS simultaneously, Yahoo Finance is queried only once; the remaining 9 requests return from memory in under 5ms."),

        ("How does the portfolio position accounting work?",
         "It maintains a double-entry transaction ledger and computes holdings using weighted average cost basis.",
         "When a user buys shares, the cost basis updates dynamically: `((old_shares * old_price) + (new_shares * new_price)) / total_shares`. When shares are sold, realized P&L is booked.",
         "Example: Buying 10 shares at Rs 3000 and 10 at Rs 3200 sets average price to Rs 3100. Selling 10 at Rs 3500 books Rs 4000 realized profit."),

        ("How do you prevent a user from selling more shares than they own?",
         "Through strict server-side validation inside `PortfolioAnalyticsService.record_transaction()` before saving to the database.",
         "The service calculates currently open shares: `total_bought - total_sold`. If requested sell quantity exceeds open balance, it raises a `ValidationError`.",
         "Example: Attempting to sell 25 shares when owning only 20 immediately returns a 400 Bad Request error."),

        ("What technical indicators did you implement and how are they calculated?",
         "SMA (20, 50, 200), EMA (12, 26, 50), RSI (14), MACD (12, 26, 9), Bollinger Bands (20, 2), ATR (14), and 21-day annualized historical volatility.",
         "Calculations use vectorized Pandas and NumPy operations on the closing price series for sub-millisecond execution.",
         "Example: Bollinger Bands compute `rolling(20).mean()` for middle band and `middle +/- 2 * rolling(20).std()` for upper and lower bands."),

        ("How does Wilder's exponential smoothing work in RSI?",
         "Unlike standard EMA where smoothing factor is `2 / (N + 1)`, Wilder's smoothing uses `1 / N` (or `alpha = 1 / 14`).",
         "This applies a slower decay rate that accurately mirrors J. Welles Wilder's original 1978 specification, avoiding false momentum spikes.",
         "Example: In `TechnicalIndicatorService`, gains and losses are smoothed using `.ewm(alpha=1/14, adjust=False).mean()`."),

        ("Explain the difference between classification and regression in Machine Learning.",
         "Classification predicts a discrete categorical label (e.g., Buy vs Sell), while regression predicts a continuous numerical quantity (e.g., stock price).",
         "StockSense AI utilizes regression to forecast future price levels and residual errors, rather than binary up/down guessing.",
         "Example: Predicting that TCS will be Rs 3,450.50 in 14 days is a regression task."),

        ("Why is random train-test splitting invalid for stock market data?",
         "Because time-series data possesses strict temporal ordering and autocorrelation. Random shuffling introduces severe look-ahead bias (data leakage).",
         "If the model trains on future data points and tests on past points, test metrics will be artificially high but fail completely in real trading.",
         "Example: StockSense AI strictly partitions data chronologically: the first 80% of days for training and the remaining 20% for testing."),

        ("What is look-ahead bias and how did you prevent it?",
         "Look-ahead bias occurs when information from the future is inadvertently used to train a model or fit scalers.",
         "In StockSense AI, `MinMaxScaler` is fit exclusively on the training partition: `scaler.fit(X_train)`, and then applied to test data via `scaler.transform(X_test)`.",
         "Example: Fitting the scaler on the whole dataset would expose the test set's maximum and minimum values to the training phase."),

        ("Explain the Linear Regression baseline used in your forecasting engine.",
         "It models the next day's price as a linear combination of autoregressive lag features (Close t-1, t-2, t-3, t-5) and rolling momentum.",
         "It uses Ordinary Least Squares (OLS) to find coefficients that minimize the sum of squared residuals.",
         "Example: In `ForecastingService._forecast_linear`, features are created with `.shift(1)`, `.shift(2)`, and fitted via `sklearn.linear_model.LinearRegression`."),

        ("How does Random Forest work for time-series forecasting?",
         "It constructs an ensemble of decision trees, each trained on bootstrap subsets of data with randomized feature splits, and averages their predictions.",
         "Random Forests capture non-linear relationships and interactions between volume, RSI, and price momentum without assuming data normality.",
         "Example: We configure `RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42)` in `ForecastingService`."),

        ("What is ARIMA and what do (p, d, q) represent?",
         "Autoregressive Integrated Moving Average: p is the number of lag observations, d is the degree of differencing for stationarity, and q is the moving average error window.",
         "StockSense AI implements `ARIMA(2, 1, 1)` on log-transformed closing prices to achieve stationary variance and mean.",
         "Example: d=1 differences log prices: `log(P_t) - log(P_{t-1})`, converting non-stationary prices into stationary continuous returns."),

        ("What is an LSTM network and why is it suited for stock forecasting?",
         "Long Short-Term Memory is a specialized Recurrent Neural Network (RNN) designed to learn long-term temporal dependencies.",
         "Traditional RNNs suffer from vanishing gradients. LSTMs use forget, input, and output gates with a cell state to selectively retain or discard historical context.",
         "Example: A lookback window of 30 trading days is fed as a 3D tensor `(samples, 30, features)` into the LSTM layer."),

        ("How does your Hybrid LSTM-ARIMA Ensemble model work?",
         "It combines the linear statistical rigor of ARIMA with the non-linear deep learning capabilities of LSTM.",
         "The ensemble performs a parameter grid search to find weights `alpha` and `(1 - alpha)` that minimize Mean Squared Error on validation data: `P_ens = alpha * P_lstm + (1 - alpha) * P_arima`.",
         "Example: If ARIMA performs better during stable periods, alpha might be 0.4; during volatile trend shifts, LSTM weight increases to 0.7."),

        ("What evaluation metrics do you compute for machine learning models?",
         "Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and Directional Accuracy (%).",
         "MAE measures average magnitude of absolute error; RMSE penalizes large outlier mistakes more severely; Directional Accuracy measures whether the predicted direction (+/-) matched reality.",
         "Example: An MAE of Rs 32.50 means predictions deviated by an average of Rs 32.50 from actual closing prices."),

        ("Why is 55% to 60% Directional Accuracy considered good in financial markets?",
         "Financial markets are near-efficient, noisy, and non-stationary. A consistent 55-60% directional edge produces significant statistical advantage over random guessing (50%).",
         "Claims of 90%+ directional accuracy on daily equity prices invariably indicate data leakage or curve fitting.",
         "Example: Top quantitative hedge funds like Renaissance Technologies operate with directional edges of 51% to 54% across massive volumes."),

        ("How does VADER sentiment analysis work?",
         "VADER is a rule-based lexicon and sentiment intensity analyzer calibrated specifically for social and media text.",
         "It calculates positive, neutral, and negative proportions, and normalizes them into a compound score between -1.0 (most negative) and +1.0 (most positive).",
         "Example: Headlines scoring >= +0.05 are tagged Positive, <= -0.05 Negative, and in between Neutral."),

        ("Where do you source real financial news articles?",
         "Through a multi-tier pipeline: Google News Financial RSS as default, NewsAPI.org if an API key is configured, and local SQLite caching as fallback.",
         "Google News RSS requires zero configuration, provides high availability, and aggregates verified articles from NDTV Profit, Economic Times, Moneycontrol, and Reuters.",
         "Example: For `TCS.NS`, the service queries Google News RSS for 'Tata Consultancy Services stock' with `hl=en-IN&gl=IN`."),

        ("How does the platform handle cases where no news articles are found?",
         "It gracefully renders an informative fallback card with quick suggestions rather than crashing or showing a blank page.",
         "The view handles empty article lists as a valid operational scenario and serves previously cached database articles if available.",
         "Example: The UI displays 'No News Articles Found for this Query' with buttons to explore TCS.NS or view general market news."),

        ("How does Django's authentication system hash passwords?",
         "By default, Django uses PBKDF2 with a SHA256 hash, an automated salt, and thousands of hashing iterations.",
         "Plaintext passwords are never saved. When a user logs in, the entered password is salted and hashed with the same parameters to check if hashes match.",
         "Example: In `auth_user` table, passwords appear as `pbkdf2_sha256$720000$salt$hash`."),

        ("How does the custom `EmailOrUsernameModelBackend` work?",
         "It inspects the submitted login identifier: if it contains an '@', it looks up the user by `email__iexact`; otherwise by `username__iexact`.",
         "If no match is found, it also falls back to checking username directly to support usernames that include '@' symbols (such as `Kiran@123`).",
         "Example: `User.objects.filter(Q(email__iexact=identifier) | Q(username__iexact=identifier)).first()`."),

        ("How do user sessions persist across browser refreshes and server restarts?",
         "Through Django's database-backed session engine (`SESSION_ENGINE = 'django.contrib.sessions.backends.db'`).",
         "A unique `stocksense_sessionid` cookie is stored in the browser, while the session data dictionary is persisted in the `django_session` table.",
         "Example: Session cookie age is set to 14 days (`SESSION_COOKIE_AGE = 1209600`), and `SESSION_SAVE_EVERY_REQUEST = True` continuously extends the expiry."),

        ("How does the StockSense AI Copilot work?",
         "It is a retrieval-grounded research assistant that inspects live platform data before generating responses.",
         "When a user asks about an equity, the backend fetches real-time quotes, technical indicators, and portfolio holdings, feeding them as factual context to Google Gemini.",
         "Example: Asking 'Should I buy TCS?' provides the assistant with current RSI (42.5), 50-day SMA, and news sentiment score, preventing hallucinations."),

        ("What happens if the Gemini API key is not configured?",
         "The research assistant seamlessly falls back to a deterministic quantitative analysis engine.",
         "The deterministic engine evaluates indicator thresholds (e.g., RSI < 30 oversold, MACD bullish crossover) and produces structured analytical commentary without failing.",
         "Example: Users without an API key still receive comprehensive fundamental and technical commentary."),

        ("What is Django REST Framework (DRF) and why use it alongside Django views?",
         "DRF is a toolkit for building Web APIs in Django, providing serialization, request parsing, authentication policies, and browsable API views.",
         "It allows StockSense AI to serve both standard server-rendered HTML pages and JSON endpoints consumed by interactive frontend widgets.",
         "Example: `api_news` returns serialized JSON data for frontend asynchronous charts or third-party client consumption."),

        ("What is WhiteNoise and why is it used?",
         "WhiteNoise allows a Python web application to serve its own static files directly without relying on Nginx or Apache.",
         "It integrates with Django's WSGI pipeline, compresses files with Gzip/Brotli, and sets unique cache-busting headers for high performance in production.",
         "Example: `MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware', ...]` serves compiled CSS and JavaScript assets on cloud containers."),

        ("How does Plotly.js render charts in StockSense AI?",
         "The Django view passes timestamps, OHLC prices, and indicator series as JSON context, which Plotly.js renders inside an interactive SVG/WebGL canvas.",
         "Users can pan, zoom, hover over candles to view exact prices, toggle indicators, and download high-resolution PNG chart snapshots.",
         "Example: `Plotly.newPlot('chartDiv', data, layout, {responsive: true})`."),

        ("How are price alerts implemented and checked?",
         "Users create alerts with target price conditions (`ABOVE` or `BELOW`). An evaluation service compares active alerts against current quotes.",
         "When a stock's current price breaches the defined threshold, the alert status transitions from `ACTIVE` to `TRIGGERED` and logs the event.",
         "Example: Setting an alert for 'TCS.NS ABOVE 3500' triggers automatically when the price reaches Rs 3,502.00."),

        ("What automated testing approach did you follow?",
         "I built a comprehensive test suite in `tests/test_platform.py` using Django's `TestCase` and test `Client`.",
         "The suite runs 22 integration tests covering authentication, portfolio accounting, watchlists, ML pipelines, news sentiment, and REST API contracts.",
         "Example: Running `python manage.py test tests.test_platform` runs all 22 tests in an isolated in-memory test database.")
    ],

    "Advanced": [
        ("How did you eliminate data leakage across the entire ML pipeline?",
         "By implementing a strict temporal pipeline: chronological partitioning (80/20), fitting scalers solely on `X_train`, and transforming `X_test` independently.",
         "In addition, lag features are generated using backward shifting only (`t-1`, `t-2`), ensuring no future candle data appears in feature vectors.",
         "Example: `scaler = MinMaxScaler(); X_train_scaled = scaler.fit_transform(X_train); X_test_scaled = scaler.transform(X_test)`."),

        ("Explain the mathematical difference between Simple, Exponential, and Wilder's Moving Averages.",
         "SMA: `SMA_t = (1/N) * sum_{i=0}^{N-1} P_{t-i}` (equal weights). EMA: `EMA_t = alpha * P_t + (1 - alpha) * EMA_{t-1}` with `alpha = 2 / (N + 1)` (exponential decay).",
         "Wilder's smoothing uses `alpha = 1 / N`, equivalent to an EMA of period `2N - 1`. This creates a smoother, less reactionary trendline suitable for bounded momentum oscillators like RSI.",
         "Example: A 14-period standard EMA has alpha = 2/15 = 0.1333, whereas Wilder's RSI smoothing uses alpha = 1/14 = 0.0714."),

        ("How does ARIMA enforce stationarity and handle heteroscedasticity?",
         "Financial price series typically exhibit non-constant variance (heteroscedasticity) and a unit root (non-stationarity).",
         "We apply a natural logarithm transformation to stabilize variance, followed by first-order differencing (`d=1`): `r_t = ln(P_t) - ln(P_{t-1})`.",
         "Example: Differencing eliminates the stochastic trend, resulting in a mean-reverting series tested via the Augmented Dickey-Fuller (ADF) test."),

        ("How is the LSTM architecture constructed in TensorFlow/Keras?",
         "The sequential model consists of: 1. LSTM layer (50 units, `return_sequences=True`), 2. Dropout (0.2), 3. LSTM layer (50 units, `return_sequences=False`), 4. Dense layer (25 units, ReLU), 5. Output Dense layer (1 unit, Linear).",
         "It uses the Adam optimizer (`learning_rate=0.001`) with Mean Squared Error loss and `EarlyStopping(patience=5)` to prevent overfitting.",
         "Example: Features are shaped into `(N - 30, 30, num_features)` where 30 is the sequence lookback window."),

        ("Explain the multi-step forward recursive forecasting strategy.",
         "To forecast H steps ahead (7, 14, 30 days), the model makes a 1-step prediction for `t+1`, appends it to the feature vector, and recursively predicts `t+2` up to `t+H`.",
         "While error compounds over long horizons, recursive forecasting maintains continuous dynamic state without requiring H distinct models.",
         "Example: At step k, the input window shifts forward: `window = np.append(window[1:], predicted_price)`."),

        ("How do you evaluate and optimize the Hybrid Ensemble weights?",
         "The ensemble runs an optimization loop evaluating blending weights `alpha in [0.0, 0.1, ..., 1.0]` against out-of-sample validation data.",
         "The weight combination that minimizes validation MSE is selected: `alpha* = argmin_alpha MSE(alpha * y_lstm + (1 - alpha) * y_arima, y_val)`.",
         "Example: When testing on TCS, an alpha of 0.65 for LSTM and 0.35 for ARIMA produced a 12% lower RMSE than either individual model."),

        ("What are the key limitations of financial time-series forecasting?",
         "1. Non-stationarity and regime shifts (e.g., sudden interest rate changes or geopolitical conflicts). 2. Low signal-to-noise ratio. 3. Reflexivity (Soros): market participants adapt to patterns, eroding predictive signals.",
         "Because external news and earnings surprises cannot be captured by past prices alone, forecasts represent statistical baselines, not guarantees.",
         "Example: A flash market crash caused by an unexpected rate hike cannot be predicted purely from historical price lags."),

        ("Explain the database schema and relational constraints of StockSense AI.",
         "Models: `UserProfile` (OneToOne with `User`), `Stock` (unique ticker, exchange), `HistoricalPrice` (ForeignKey to Stock with `unique_together=('stock', 'date')`), `Portfolio` (OneToOne with User), `Transaction` (ForeignKey to Portfolio and Stock), `Watchlist` and `WatchlistItem`, and `NewsArticle` (`unique_together=('url',)`).",
         "Foreign keys enforce referential integrity with `on_delete=models.CASCADE` or `SET_NULL`, and indexed fields optimize query speeds.",
         "Example: `unique_together = ('stock', 'date')` on `HistoricalPrice` guarantees no duplicate daily candles exist for any equity."),

        ("How did you optimize ORM query performance to prevent N+1 query problems?",
         "By utilizing `select_related()` for single-valued relationships (ForeignKey, OneToOne) and `prefetch_related()` for multi-valued relationships (ManyToMany, reverse ForeignKeys).",
         "In portfolio views, fetching transactions with `Transaction.objects.select_related('stock', 'portfolio__user')` performs an SQL `INNER JOIN` in 1 query instead of N+1.",
         "Example: Without `select_related`, iterating over 100 transactions to print stock symbols executes 101 separate SQL queries."),

        ("How does Django's session management operate at the HTTP protocol level?",
         "HTTP is stateless. When a user authenticates, Django creates a session record with a 32-character random key and sets a `Set-Cookie: stocksense_sessionid=...` header.",
         "Subsequent browser requests include this cookie. Django's `SessionMiddleware` reads the cookie, queries `django_session`, and attaches the loaded user to `request.user`.",
         "Example: Settings enforce `SESSION_COOKIE_HTTPONLY = True` (preventing JavaScript access) and `SESSION_COOKIE_SAMESITE = 'Lax'` (defending against CSRF)."),

        ("How does the platform defend against Cross-Site Scripting (XSS)?",
         "1. Django template engine automatically escapes all variable outputs (converting `<`, `>`, `&`, `\"` to HTML entities). 2. Session cookies use `HttpOnly` flags. 3. Explicit input sanitization using regex.",
         "If user input must render HTML, it is cleaned with `bleach` or `html.escape` rather than using the dangerous `|safe` filter indiscriminately.",
         "Example: Submitting `<script>alert('hack')</script>` in a search box renders safely as `&lt;script&gt;` text in the DOM."),

        ("How does the platform defend against SQL Injection?",
         "Django ORM uses parameterized queries (prepared statements) for all database operations.",
         "User inputs are passed as parameters separate from the SQL command structure, ensuring input characters are treated as literal data, never as executable SQL commands.",
         "Example: `Stock.objects.filter(symbol=user_input)` compiles to `WHERE symbol = %s` with safe parameter substitution."),

        ("Explain the FIFO (First-In, First-Out) tax-lot portfolio accounting algorithm.",
         "When shares are sold, the algorithm matches sold shares against the oldest available buy transactions to calculate realized capital gains.",
         "Each buy lot tracks `remaining_quantity`. As sells occur, older lots are exhausted first, establishing accurate cost basis for tax compliance.",
         "Example: Buying 10 shares at Rs 100, then 10 at Rs 150. Selling 10 shares at Rs 200 matches against the Rs 100 lot, booking Rs 1000 profit rather than Rs 500."),

        ("How does the multi-factor equity screener filter the universe?",
         "It evaluates equities across multiple dimensions: market capitalization, P/E ratio bounds, 52-week price range proximity, RSI thresholds, and moving average alignment.",
         "In `apps.market.services.MarketDataService`, filtering is vectorized across cached dataframe snapshots for immediate response times.",
         "Example: Filtering for `RSI < 35 AND Price > SMA_200` identifies oversold equities that remain in long-term structural uptrends."),

        ("How would you scale this application to handle 10,000 requests per minute?",
         "1. Deploy multiple Django instances using Gunicorn/Uvicorn behind Nginx with round-robin load balancing. 2. Replace LocMemCache with a Redis Cluster. 3. Migrate database to AWS Aurora PostgreSQL with read replicas and PgBouncer connection pooling. 4. Offload ML training to asynchronous Celery workers backed by RabbitMQ.",
         "Static assets would be offloaded to an Amazon S3 bucket with CloudFront CDN distribution.",
         "Example: Read-heavy quote and chart endpoints would be served directly from Redis cache with 99% hit rates, protecting PostgreSQL from saturation."),

        ("How would you transition model inference from synchronous to asynchronous?",
         "I would use Celery with Redis as the broker. When a user requests a heavy 30-day LSTM training run, the view dispatches a task (`forecast_task.delay(symbol)`) and immediately returns a `task_id`.",
         "The frontend polls `/api/tasks/<task_id>/` or listens via WebSockets (Django Channels) for the completed forecast JSON payload.",
         "Example: This prevents HTTP worker timeouts on slow network connections or deep neural network training runs."),

        ("Explain the architecture of the News Sentiment engine pipeline.",
         "1. View requests news for a symbol. 2. Service checks cache (`news_feed_<symbol>`). 3. On miss, it queries Google News RSS / NewsAPI. 4. Extracts titles, pubDates, publishers, and clean summaries. 5. VADER computes polarity scores. 6. Articles are upserted into SQLite (`NewsArticle.objects.update_or_create`). 7. Aggregates distribution metrics and caches for 300s.",
         "The unique URL constraint prevents duplicate articles, building a persistent historical sentiment archive over time.",
         "Example: Even if the external news feed is unreachable, previously persisted articles serve as an offline database cache."),

        ("What is the difference between VADER and a Transformer-based model like FinBERT?",
         "VADER is a rule-based lexicon tool: extremely fast (~1 millisecond per article), requires zero GPU memory, and runs locally without large neural network weights.",
         "FinBERT is a BERT language model fine-tuned on financial text: captures deep contextual nuances but requires ~500MB model memory and GPU acceleration.",
         "Example: For a real-time web application running on commodity servers, VADER provides immediate sentiment classification without server latency."),

        ("How do you handle dual-currency conversions (INR vs USD)?",
         "The `UserProfile` model stores the user's `preferred_currency` ('INR' or 'USD'). Each `Stock` model specifies its native trading currency.",
         "When calculating portfolio totals, foreign assets are converted using the active USD/INR exchange rate fetched and cached by `MarketDataService`.",
         "Example: If USD/INR is 83.50, an Apple holding of $1,000 is converted to Rs 83,500 when calculating total net worth for an Indian investor."),

        ("What is the significance of Directional Accuracy over Mean Absolute Error in trading?",
         "MAE tells you the average error in price points, but in trading, knowing whether tomorrow's price will move UP or DOWN is often more valuable than the exact rupee price.",
         "A model with low MAE could systematically predict the wrong direction during trend reversals, leading to losing trades.",
         "Example: If a stock moves from Rs 100 to Rs 110, predicting Rs 108 gives +8 direction (correct), whereas predicting Rs 99 has similar absolute error but wrong direction."),

        ("How does the platform handle time zones across global markets?",
         "All database timestamps (`created_at`, `published_at`, `transaction_date`) are stored in UTC using Django's timezone-aware datetime utilities (`USE_TZ = True`).",
         "Display layers format times to the user's local session timezone (IST for Indian market hours, EST for US sessions).",
         "Example: `published_at = email.utils.parsedate_to_datetime(pub_date); timezone.make_aware(published_at, datetime.timezone.utc)`."),

        ("Explain the role of `django-cors-headers` in your project.",
         "Cross-Origin Resource Sharing (CORS) is a browser security mechanism that restricts HTTP requests made from a different domain or port.",
         "`django-cors-headers` adds appropriate `Access-Control-Allow-Origin` headers to Django API responses, enabling external clients or mobile apps to interact with the endpoints.",
         "Example: In `settings.py`, `CORS_ALLOW_ALL_ORIGINS = True` permits authorized client access during development."),

        ("What happens during a walk-forward model validation?",
         "Rather than training once and predicting far into the future, walk-forward validation tests the model sequentially over rolling historical windows.",
         "At each step t, the model trains on data up to t, predicts t+1, records the error, and then rolls the window forward by 1 step.",
         "Example: This mirrors real trading conditions where an algorithm re-evaluates data daily with fresh close prices."),

        ("Why did you use `update_or_create` instead of `get_or_create` for news persistence?",
         "`get_or_create` leaves existing records untouched. `update_or_create` ensures that if an article already exists (by unique URL), any updated metadata, summary, or recalculated sentiment score is refreshed.",
         "This guarantees data integrity without creating duplicate key constraint violations in the database.",
         "Example: `NewsArticle.objects.update_or_create(url=link, defaults={'sentiment_score': compound, ...})`."),

        ("How does the Research Assistant synthesize answers using Gemini?",
         "It uses Google's latest `google.genai` SDK (`gemini-2.5-flash`). The service constructs a grounded prompt embedding real-time stock data, technical indicators, and portfolio holdings.",
         "The model is instructed to act as a quantitative research analyst, citing verified numbers from the provided context and refusing to invent ungrounded data.",
         "Example: If the prompt contains `TCS Current Price: Rs 3450, RSI: 42.5`, Gemini analyzes those exact numbers rather than guessing outdated training data."),

        ("What is the difference between `null=True` and `blank=True` in Django models?",
         "`null=True` is database-related: it defines whether the database column allows `NULL` values. `blank=True` is validation-related: it determines whether the field is required in forms and admin.",
         "For character-based fields (CharField, TextField), Django conventions suggest avoiding `null=True` to prevent having two representations for empty data (`NULL` vs empty string `''`).",
         "Example: In `NewsArticle`, `stock = models.ForeignKey(..., null=True, blank=True)` allows market-wide news articles not tied to a specific stock."),

        ("How do you handle database migrations safely in production?",
         "1. Never run `makemigrations` in production. 2. Review generated migration SQL using `python manage.py sqlmigrate <app> <migration_number>`. 3. Apply non-destructive migrations (`migrate`) during deployment windows.",
         "For schema changes on high-traffic tables, use multi-phase rollouts (e.g., add nullable column, backfill data, add constraints).",
         "Example: We test migrations on local SQLite, verify against PostgreSQL staging, and execute `python manage.py migrate --noinput` in CI/CD."),

        ("What is the purpose of `unique_together` in Django models?",
         "It enforces a composite unique constraint across multiple table columns at the database level.",
         "In `HistoricalPrice`, `unique_together = ('stock', 'date')` guarantees that no stock can have two competing price records for the same calendar date.",
         "Example: Attempting to insert a second row for TCS on 2026-09-30 triggers an `IntegrityError` at the database level."),

        ("Explain how you tested the application against network failures.",
         "I simulated API connection drops and external timeouts in `NewsSentimentService` and `MarketDataService`.",
         "When external feeds fail, try/except blocks capture `urllib.error.URLError` and fall back to local SQLite cached data, serving the user with an informational notice rather than an HTTP 500 error.",
         "Example: When testing offline mode, the news page displays 'Local Database Cache (Offline Mode)' with all previously saved articles intact."),

        ("What would you say is the most complex engineering challenge you solved in this project?",
         "Bridging the disconnect between asynchronous financial market feeds, leakage-free econometric model execution, and sub-second web presentation.",
         "Solving this required architecting a decoupled service layer, implementing vectorized pandas computations, designing a multi-tier fallback news pipeline, and establishing walk-forward ML evaluation.",
         "Example: Ensuring that executing a 5-model comparison on TCS runs in under 3 seconds while maintaining zero data leakage across all training partitions.")
    ],

    "Python": [
        ("What are list comprehensions and why are they preferred in Python?",
         "List comprehensions provide a concise syntax to create lists from existing iterables: `[expr for item in iterable if condition]`.",
         "They are executed at C-speed inside the Python interpreter, making them significantly faster and more readable than standard for-loops with `.append()`.",
         "Example: `positive_articles = [a for a in articles if a.sentiment_label == 'POSITIVE']`."),

        ("Explain the difference between `is` and `==` in Python.",
         "`==` checks for value equality (whether values of two objects are equal), while `is` checks for identity (whether both variables point to the exact same memory address).",
         "Example: `a = [1, 2]; b = [1, 2]; a == b` is True, but `a is b` is False. Use `is` when comparing against singletons like `None` (`if val is None:`)."),

        ("What is a Python generator and how does `yield` work?",
         "A generator is a function that returns an iterator that produces values on-demand using the `yield` keyword instead of `return`.",
         "Generators maintain execution state and compute values lazily, consuming `O(1)` memory regardless of dataset size.",
         "Example: Iterating over millions of historical price records row-by-row using a generator avoids loading entire tables into RAM."),

        ("What are `*args` and `**kwargs` in Python function definitions?",
         "`*args` allows passing a variable number of positional arguments (collected as a tuple), and `**kwargs` allows variable keyword arguments (collected as a dictionary).",
         "They enable flexible function signatures and clean decorator implementations.",
         "Example: `def execute_model(name, *args, **kwargs): ...` passes optional hyperparameters dynamically to underlying models."),

        ("Explain Python's Global Interpreter Lock (GIL).",
         "The GIL is a mutex that prevents multiple native OS threads from executing Python bytecodes simultaneously in CPython.",
         "It protects Python's memory management from race conditions. For CPU-bound tasks, multiprocessing or C-extensions (NumPy) are preferred over multithreading.",
         "Example: NumPy operations bypass the GIL by executing vectorized linear algebra in optimized C/Fortran libraries."),

        ("What is the difference between shallow copy and deep copy?",
         "A shallow copy constructs a new object but inserts references to the original object's nested elements. A deep copy recursively copies all nested objects.",
         "Modifying a nested mutable element in a shallow copy affects the original; in a deep copy, they are completely independent.",
         "Example: `import copy; deep_df = copy.deepcopy(original_dict)`."),

        ("How do decorators work in Python?",
         "A decorator is a function that takes another function as an argument, extends its behavior without modifying it, and returns the modified function.",
         "Decorators use the `@decorator_name` syntax.",
         "Example: Django's `@login_required` wraps a view function, checks `request.user.is_authenticated`, and redirects unauthenticated users to `/login/`."),

        ("What are Python dunder (magic) methods?",
         "Special methods surrounded by double underscores (e.g., `__init__`, `__str__`, `__repr__`, `__len__`) that define how objects behave with built-in operations.",
         "In Django models, `__str__` defines the human-readable string representation of a model instance.",
         "Example: `def __str__(self): return f'{self.symbol} - {self.name}'` in the `Stock` model."),

        ("What is the difference between `staticmethod`, `classmethod`, and regular instance methods?",
         "Instance methods receive `self` (the instance); class methods receive `cls` (the class itself) via `@classmethod`; static methods receive neither via `@staticmethod`.",
         "Class methods are useful for alternative constructors; static methods are utility functions that don't access class or instance state.",
         "Example: `NewsSentimentService.get_stock_news()` is implemented as a `@classmethod`."),

        ("How does exception handling with `try...except...else...finally` work?",
         "`try` contains code that may fail; `except` catches specific exceptions; `else` runs if no exceptions occurred; `finally` runs unconditionally for cleanup.",
         "Example: In API calls, `try` fetches data, `except URLError` handles network drop, and `finally` closes the HTTP connection."),

        ("What are Python type hints and why are they useful?",
         "Type hints annotate expected argument types and return types using the `typing` module (e.g., `def get_stock(symbol: str) -> Optional[Stock]:`).",
         "They improve code documentation, IDE autocompletion, and allow static type checking via tools like `mypy` without impacting runtime speed.",
         "Example: `def get_stock_news(symbol: Optional[str] = None) -> Dict[str, Any]:` in `NewsSentimentService`."),

        ("What is the difference between a tuple and a list?",
         "Lists are mutable (elements can be added, removed, or changed) and defined with `[]`; tuples are immutable and defined with `()`.",
         "Tuples are hashable (can be used as dictionary keys), consume less memory, and provide write-protection for fixed collections.",
         "Example: Model choices `SENTIMENT_CHOICES = [('POSITIVE', 'Positive'), ...]` use tuples for immutable key-value pairs."),

        ("Explain how Python manages memory and garbage collection.",
         "Python uses reference counting as its primary memory management mechanism: when an object's reference count drops to zero, its memory is deallocated immediately.",
         "To resolve circular references, Python includes a cyclic garbage collector that runs generational checks periodically.",
         "Example: Deleting large intermediate DataFrames with `del df` decrements references, freeing RAM for subsequent ML training."),

        ("What is the purpose of `__init__.py` in Python packages?",
         "It marks a directory as a Python package, allowing its modules to be imported using dot notation (`from apps.market.models import Stock`).",
         "It can also contain package-level initialization code and define `__all__` to control exported symbols.",
         "Example: Every app directory in StockSense AI contains an `__init__.py` file."),

        ("What is the difference between `range()` and a list of numbers?",
         "`range(start, stop, step)` is an immutable sequence type that generates numbers on-demand in `O(1)` memory.",
         "A list of numbers allocates memory for every element immediately in RAM.",
         "Example: `for i in range(len(prices)):` uses minimal memory compared to creating a full integer list."),

        ("What is monkey patching in Python?",
         "The runtime modification of a class, module, or method without altering the original source code.",
         "Frequently used in unit testing to mock external API requests or database connections.",
         "Example: Mocking `urllib.request.urlopen` in tests to return pre-recorded RSS XML data without touching live servers."),

        ("How does Python's `zip()` function work?",
         "`zip(*iterables)` pairs corresponding elements from multiple iterables into tuples, stopping when the shortest iterable is exhausted.",
         "Example: `for date, price in zip(dates, closing_prices):` pairs timestamp arrays with price series to build time-series dictionaries."),

        ("What is the difference between `append()` and `extend()` on Python lists?",
         "`append(item)` adds its argument as a single element to the end of the list. `extend(iterable)` iterates over its argument, adding each element individually.",
         "Example: `a = [1, 2]; a.append([3, 4])` yields `[1, 2, [3, 4]]`; `a.extend([3, 4])` yields `[1, 2, 3, 4]`."),

        ("What is a lambda function?",
         "An anonymous, small inline function defined with the `lambda` keyword: `lambda arguments: expression`.",
         "Useful for short callbacks, sorting keys, or mapping functions.",
         "Example: `articles.sort(key=lambda x: x.published_at, reverse=True)` sorts articles by publication date."),

        ("What is the `with` statement and what is a context manager?",
         "The `with` statement simplifies resource management by ensuring cleanup code runs automatically via `__enter__` and `__exit__` methods.",
         "It prevents resource leaks such as unclosed files or database connections even if exceptions occur.",
         "Example: `with urllib.request.urlopen(req) as resp:` guarantees the socket connection closes immediately after reading.")
    ],

    "Django": [
        ("What is the role of `manage.py` in a Django project?",
         "A command-line utility that acts as a wrapper around `django-admin` for project-specific tasks.",
         "It sets the `DJANGO_SETTINGS_MODULE` environment variable and executes management commands like `runserver`, `migrate`, `makemigrations`, and `test`.",
         "Example: `python manage.py runserver` boots the local development server."),

        ("What is the difference between `makemigrations` and `migrate`?",
         "`makemigrations` inspects model changes in `models.py` and writes new Python migration files. `migrate` executes those migration files against the database to alter the SQL schema.",
         "Example: Adding a field to `NewsArticle` requires `makemigrations` to generate the migration file and `migrate` to add the column in SQLite."),

        ("How does Django's middleware work?",
         "Middleware is a framework of hooks into Django's request/response processing: a chain of components executed on every HTTP request and response.",
         "Examples include `SecurityMiddleware`, `SessionMiddleware`, `AuthenticationMiddleware`, and `CsrfViewMiddleware`.",
         "Example: `AuthenticationMiddleware` reads the session cookie and attaches the user object to `request.user` before views execute."),

        ("What is the difference between `select_related` and `prefetch_related`?",
         "`select_related` performs an SQL `JOIN` in a single query; used for single-valued relationships (ForeignKey, OneToOne). `prefetch_related` executes a separate lookup query and joins in Python; used for ManyToMany and reverse ForeignKeys.",
         "Example: `Transaction.objects.select_related('stock')` joins stock data in one SQL query."),

        ("What is the Django ORM `F` expression?",
         "An `F()` object represents the value of a database column directly within the database query, allowing database-level operations without pulling data into Python memory.",
         "Prevents race conditions when updating counters or comparing two fields on the same table.",
         "Example: `Product.objects.update(stock_count=F('stock_count') - 1)` decrements inventory atomically in SQL."),

        ("What is the Django ORM `Q` expression?",
         "A `Q()` object encapsulates SQL query conditions that can be combined using logical operators (`&` AND, `|` OR, `~` NOT).",
         "Enables complex OR queries that cannot be expressed with standard keyword arguments in `.filter()`.",
         "Example: `User.objects.filter(Q(username__iexact=u) | Q(email__iexact=u))` matches either username OR email."),

        ("How does Django handle static files in development vs production?",
         "In development, `django.contrib.staticfiles` automatically serves files from app `static/` folders. In production, `collectstatic` gathers all static files into `STATIC_ROOT`, served by Nginx or WhiteNoise.",
         "Example: In production, WhiteNoise compresses and caches assets with unique hashes directly from `STATIC_ROOT`."),

        ("What are Django signals and when should they be used?",
         "Signals allow decoupled applications to get notified when actions occur elsewhere in the framework (e.g., `post_save`, `pre_delete`).",
         "In StockSense AI, a `post_save` signal on the `User` model automatically creates a corresponding `UserProfile` and empty `Portfolio`.",
         "Example: `@receiver(post_save, sender=User) def create_user_profile(sender, instance, created, **kwargs): ...`."),

        ("What is the difference between a Django Form and a ModelForm?",
         "A standard `Form` requires manually defining all fields and validation. A `ModelForm` automatically generates fields, widgets, and validation rules directly from a Django model class.",
         "Example: `TransactionForm(forms.ModelForm)` automatically inherits fields and validation constraints from the `Transaction` model."),

        ("How do you implement custom user authentication in Django?",
         "By creating a custom authentication backend class that inherits from `django.contrib.auth.backends.ModelBackend` and overrides `authenticate(self, request, username=None, password=None)`.",
         "Then configure `AUTHENTICATION_BACKENDS` in `settings.py`.",
         "Example: `EmailOrUsernameModelBackend` checks whether the identifier is an email or username before calling `user.check_password()`."),

        ("What is `get_object_or_404` and why is it used?",
         "A shortcut that calls `get()` on a model manager and raises an `Http404` exception instead of letting a `DoesNotExist` exception cause an unhandled 500 error.",
         "Example: `stock = get_object_or_404(Stock, symbol=symbol.upper())` cleanly returns an HTTP 404 page if an unknown stock is requested."),

        ("What are Django template tags and filters?",
         "Tags provide logic in templates (e.g., `{% if %}`, `{% for %}`, `{% url %}`); filters transform values (e.g., `{{ price|floatformat:2 }}`, `{{ date|date:'Y-m-d' }}`).",
         "Example: `{{ article.published_at|date:'M d, Y' }}` formats UTC timestamps into human-readable dates."),

        ("What does `auto_now` vs `auto_now_add` mean on DateTimeField?",
         "`auto_now_add=True` sets the timestamp only once when the object is first created. `auto_now=True` updates the timestamp every time the object is saved.",
         "Example: `created_at = models.DateTimeField(auto_now_add=True)` and `updated_at = models.DateTimeField(auto_now=True)`."),

        ("How do you handle database transactions atomically in Django?",
         "By using `transaction.atomic()` as a decorator or context manager: either all database operations within the block succeed, or all are rolled back on error.",
         "Ensures data consistency when executing multi-table operations like updating portfolio cash balance and creating a transaction record.",
         "Example: `with transaction.atomic(): portfolio.cash -= total; transaction.save()`."),

        ("What is the role of `settings.py`?",
         "The master configuration file for a Django project, defining installed apps, middleware, database settings, auth backends, templates, and security flags.",
         "Example: In StockSense AI, `settings.py` configures `INSTALLED_APPS`, `CACHES`, `DATABASES`, and API keys via environment variables."),

        ("What is `reverse()` in Django?",
         "A utility that resolves a URL path string from its configured view name, eliminating hardcoded URLs.",
         "Example: `reverse('news')` returns `'/news/'`, and `redirect('stocks_detail', symbol='TCS.NS')` resolves dynamic routes."),

        ("What is the purpose of `related_name` on ForeignKey fields?",
         "It defines the reverse relationship attribute name on the target model.",
         "Example: On `Transaction.stock = ForeignKey(Stock, related_name='transactions')`, calling `stock.transactions.all()` accesses all trades for that stock."),

        ("How does Django protect against Clickjacking?",
         "Via `XFrameOptionsMiddleware`, which sets the `X-Frame-Options: DENY` (or `SAMEORIGIN`) HTTP response header, preventing the site from being embedded inside an unauthorized `<iframe>`.",
         "Example: Enabled by default in Django's `MIDDLEWARE` setting."),

        ("What is the difference between `request.GET` and `request.POST`?",
         "`request.GET` is a dictionary-like `QueryDict` containing URL query parameters; `request.POST` contains form data submitted in the HTTP request body.",
         "Example: `request.GET.get('symbol')` reads `?symbol=TCS.NS`, while `request.POST.get('shares')` reads submitted trade quantities."),

        ("What is `django.core.cache` and how is it configured?",
         "Django's caching framework supporting multiple backends: `LocMemCache` (local memory), `RedisCache`, `MemcachedCache`, or `DatabaseCache`.",
         "Example: Configured in `settings.py` with `BACKEND: 'django.core.cache.backends.locmem.LocMemCache'` for fast in-process caching.")
    ],

    "HTML_CSS_JS": [
        ("What is the Document Object Model (DOM)?",
         "A programming interface that represents HTML documents as a hierarchical tree of nodes, allowing JavaScript to inspect and modify content, structure, and styles dynamically.",
         "Example: `document.getElementById('loadingOverlay').style.display = 'block'` modifies a DOM node's CSS style."),

        ("What is the difference between `let`, `const`, and `var` in JavaScript?",
         "`var` is function-scoped and hoisted; `let` and `const` are block-scoped. `const` creates an immutable binding (cannot be reassigned), whereas `let` allows reassignment.",
         "Example: Use `const chartData = [...]` for fixed references and `let currentPrice = 100` for mutable variables."),

        ("What is the Fetch API and how does it replace XMLHttpRequest?",
         "Fetch is a modern, promise-based JavaScript API for making asynchronous HTTP network requests with cleaner syntax and native JSON parsing.",
         "Example: `fetch('/api/predictions/TCS.NS/').then(r => r.json()).then(data => renderChart(data))`."),

        ("What is asynchronous programming and how do Promises work in JavaScript?",
         "Asynchronous programming allows long-running operations (like network API requests) to run in the background without freezing the browser UI thread.",
         "A Promise represents an eventual completion (resolved) or failure (rejected) of an async operation.",
         "Example: Using `async/await` syntax: `const res = await fetch('/api/news/'); const data = await res.json();`."),

        ("What is event bubbling in JavaScript?",
         "Event bubbling is the process where an event triggered on a child DOM element propagates up through its parent elements in the DOM tree.",
         "Enables event delegation: attaching a single listener to a parent container to manage events from multiple child elements.",
         "Example: Listening for clicks on a watchlist table body to handle delete actions on dynamic rows."),

        ("What is CSS Flexbox and when should you use it?",
         "A 1-dimensional CSS layout model designed for distributing space and aligning items along a single row or column.",
         "Ideal for navigation bars, button groups, and responsive card headers.",
         "Example: `display: flex; justify-content: space-between; align-items: center;`."),

        ("What is CSS Grid and how does it differ from Flexbox?",
         "CSS Grid is a 2-dimensional layout model managing both rows and columns simultaneously, whereas Flexbox is primarily 1-dimensional.",
         "Grid is ideal for overall page layouts and multi-column dashboard card grids.",
         "Example: `display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;` renders StockSense AI's KPI metric cards."),

        ("What are CSS Variables (Custom Properties) and why use them?",
         "Entities defined by CSS authors containing specific values reused throughout a document using the `var(--name)` syntax.",
         "Enables consistent theme management (dark mode palettes) across thousands of lines of CSS.",
         "Example: `:root { --bg-app: #0d1117; --accent-primary: #1f6feb; }`."),

        ("What is responsive design and how do CSS Media Queries work?",
         "Responsive design ensures a web application renders cleanly across desktops, tablets, and mobile devices.",
         "Media queries apply CSS rule blocks conditionally based on screen characteristics like viewport width.",
         "Example: `@media (max-width: 768px) { .app-sidebar { display: none; } }` collapses sidebar on mobile."),

        ("What is the difference between `display: none` and `visibility: hidden`?",
         "`display: none` removes the element completely from document flow (takes zero space); `visibility: hidden` hides the element visually while preserving its layout space in the DOM.",
         "Example: `#loadingOverlay { display: none; }` takes no space until activated via JavaScript."),

        ("What are Lucide icons and how are they initialized?",
         "An open-source SVG icon library. In HTML, icons are declared via `<i data-lucide='icon-name'></i>` and converted into inline SVGs via `lucide.createIcons()`.",
         "Example: `lucide.createIcons()` runs in `base.html` after the DOM loads."),

        ("How does Plotly.js handle responsive resizing on window resize?",
         "By calling `Plotly.Plots.resize(chartElement)` inside a window `resize` event listener or setting `{responsive: true}` in the Plotly configuration dictionary.",
         "Example: `window.addEventListener('resize', () => Plotly.Plots.resize(document.getElementById('stockChart')));`."),

        ("What is `localStorage` vs `sessionStorage` vs Cookies?",
         "`localStorage` persists data indefinitely until explicitly cleared; `sessionStorage` lasts only for the duration of the browser tab session; Cookies are sent with every HTTP request to the server.",
         "Example: Authentication sessions use HTTP-only cookies, while UI preferences (e.g. sidebar collapse) can use `localStorage`."),

        ("What is JSON and how do you serialize/deserialize it in JavaScript?",
         "JavaScript Object Notation: a lightweight, text-based data interchange format.",
         "`JSON.stringify(object)` serializes a JavaScript object into a JSON string; `JSON.parse(string)` deserializes a JSON string into a JavaScript object.",
         "Example: `const payload = JSON.stringify({symbol: 'TCS.NS', shares: 10});`."),

        ("What is a CSS pseudo-class and give examples?",
         "A keyword added to a selector specifying a special state of the selected elements.",
         "Examples include `:hover` (cursor over element), `:focus` (element active/selected), and `:nth-child()` (positional selector).",
         "Example: `.article-card:hover { border-color: var(--border-strong); }`."),

        ("What does `event.preventDefault()` do in JavaScript?",
         "It cancels the default event behavior defined by the browser without stopping event propagation.",
         "Commonly used to prevent form submission from reloading the page during AJAX operations.",
         "Example: `form.addEventListener('submit', (e) => { e.preventDefault(); submitTradeViaAjax(); });`."),

        ("What is Semantic HTML and why is it important?",
         "Using HTML markup that conveys the meaning and structure of content (e.g., `<article>`, `<nav>`, `<header>`, `<main>`) rather than generic `<div>` tags.",
         "Improves accessibility for screen readers, SEO rankings, and code maintainability.",
         "Example: Using `<article class='article-card'>` for news stories."),

        ("What is the box model in CSS?",
         "Every HTML element is rendered as a rectangular box comprising: Content, Padding (space inside border), Border, and Margin (space outside border).",
         "Using `box-sizing: border-box` ensures padding and border are included in total width and height.",
         "Example: `* { box-sizing: border-box; }` is declared globally in StockSense CSS."),

        ("How do you select DOM elements in modern JavaScript?",
         "Using `document.getElementById('id')`, `document.querySelector('.class')`, or `document.querySelectorAll('tag')`.",
         "Example: `const select = document.querySelector('select[name=\"symbol\"]');`."),

        ("What is a CSS animation / transition and how is it used?",
         "Transitions smoothly animate changes between property values over a defined duration and timing curve.",
         "Example: `.spinner { animation: spin 0.8s linear infinite; }` animates the loading spinner on news fetch.")
    ]
}

# Add remaining categories: SQL_Database, API, Machine_Learning, NLP_Sentiment, Project_Specific
QA_DATA["SQL_Database"] = [
    ("What is the difference between SQL and NoSQL databases?",
     "SQL databases are relational, table-based with rigid schemas and ACID transactions (e.g., PostgreSQL, SQLite). NoSQL databases are non-relational, document/key-value based with flexible schemas (e.g., MongoDB, Redis).",
     "Financial applications strictly require relational databases to guarantee atomic transactions, foreign key integrity, and exact double-entry accounting.",
     "Example: StockSense AI uses SQLite/PostgreSQL to prevent corrupting portfolio balances during trades."),

    ("What are ACID properties in database transactions?",
     "Atomicity (all operations succeed or all fail), Consistency (data satisfies all constraints), Isolation (concurrent transactions do not interfere), and Durability (committed data survives crashes).",
     "Example: Buying shares requires deducting cash and adding shares atomically; if cash deduction fails, share addition is rolled back."),

    ("What is an SQL Index and how does it improve query performance?",
     "An index is a data structure (typically a B-Tree) created on table columns that enables rapid binary search lookups without scanning every row in the table.",
     "Speeds up `SELECT ... WHERE` queries at the cost of slightly slower `INSERT`/`UPDATE` operations and additional disk storage.",
     "Example: In `Stock`, `symbol = CharField(max_length=20, db_index=True)` ensures ticker lookups complete in O(log N) time."),

    ("What is a Foreign Key constraint?",
     "A database key used to link two tables together, ensuring referential integrity by requiring that a value in the child table matches a primary key in the parent table.",
     "Example: `Transaction.stock` references `Stock.id`. If a stock is deleted, Django handles cascading rules (`CASCADE` or `SET_NULL`)."),

    ("Explain the difference between `INNER JOIN` and `LEFT JOIN`.",
     "`INNER JOIN` returns only rows that have matching values in both tables. `LEFT JOIN` returns all rows from the left table and matched rows from the right table (filling with NULL if no match).",
     "Example: An `INNER JOIN` between User and Portfolio returns only users who have portfolios; a `LEFT JOIN` returns all users regardless of portfolio existence."),

    ("What is database normalization and why is it important?",
     "The process of organizing data into tables to reduce data redundancy and eliminate update/delete anomalies (1NF, 2NF, 3NF).",
     "Example: Storing stock company names in the `Stock` table rather than repeating the full company string in every single `Transaction` row."),

    ("What is the difference between `GROUP BY` and `WHERE` in SQL?",
     "`WHERE` filters individual rows before any grouping or aggregation takes place. `GROUP BY` groups rows sharing common column values to compute aggregates (SUM, AVG, COUNT).",
     "Example: `SELECT symbol, SUM(shares) FROM transactions WHERE type='BUY' GROUP BY symbol;`."),

    ("What is the `HAVING` clause in SQL?",
     "`HAVING` filters aggregated groups after `GROUP BY` has executed, whereas `WHERE` cannot filter on aggregate functions.",
     "Example: `SELECT symbol, SUM(shares) FROM transactions GROUP BY symbol HAVING SUM(shares) > 100;`."),

    ("What is database connection pooling and why is it needed?",
     "Connection pooling maintains a cache of active database connections that can be reused across requests, avoiding the overhead of creating a new TCP connection on every HTTP query.",
     "In production PostgreSQL deployments, tools like PgBouncer manage pooling for high-concurrency throughput.",
     "Example: Reusing connections reduces request latency from ~50ms to ~2ms."),

    ("What causes a database deadlock and how can it be avoided?",
     "A deadlock occurs when two concurrent transactions each hold a lock the other needs, causing both to wait indefinitely.",
     "Avoided by always acquiring locks in a consistent global order and keeping transaction blocks as short as possible.",
     "Example: Always locking `Portfolio` before inserting `Transaction` prevents lock inversion across concurrent trade requests."),

    ("What is an SQL injection attack and how does Django prevent it?",
     "An attack where malicious SQL statements are inserted into entry fields to execute unauthorized database commands.",
     "Django ORM uses parameterized queries (prepared statements) that strictly separate SQL command syntax from user data parameters.",
     "Example: Passing `' OR '1'='1` into `filter(symbol=val)` is safely escaped as a string literal rather than executing a logic bypass."),

    ("What is the difference between `DELETE`, `TRUNCATE`, and `DROP`?",
     "`DELETE` removes specific rows matching a WHERE clause and can be rolled back; `TRUNCATE` quickly removes all rows in a table without logging individual deletions; `DROP` destroys the entire table structure and data.",
     "Example: Testing suites use transaction rollbacks or `TRUNCATE` to clean tables between test runs."),

    ("What is a composite primary key?",
     "A primary key composed of two or more columns that together uniquely identify a row in a table.",
     "In Django, this is represented via `unique_together = ('stock', 'date')` on `HistoricalPrice`.",
     "Example: Neither stock ID alone nor date alone is unique, but the combination of TCS and 2026-09-30 is globally unique."),

    ("What is a database transaction log (WAL)?",
     "Write-Ahead Logging (WAL) is a technique where changes are recorded in a sequential append-only log on disk before being applied to database pages.",
     "Guarantees durability and fast recovery after unexpected system power loss.",
     "Example: SQLite uses WAL mode (`PRAGMA journal_mode=WAL;`) for improved concurrent read performance."),

    ("How do you back up and restore an SQLite database?",
     "Because SQLite is self-contained in a single file (`db.sqlite3`), backups can be made by copying the file or using the SQLite `.backup` CLI command.",
     "Example: `copy db.sqlite3 db_backup.sqlite3` creates an immediate complete snapshot of the database state.")
]

QA_DATA["API"] = [
    ("What are the core HTTP request methods used in REST APIs?",
     "GET (retrieve resource), POST (create resource), PUT (replace entire resource), PATCH (partial update), and DELETE (remove resource).",
     "Example: `GET /api/stocks/` lists stocks, while `POST /api/portfolio/transactions/` creates a new trade execution."),

    ("What is the difference between HTTP status codes 200, 201, 400, 401, 403, 404, and 500?",
     "200 OK (successful request), 201 Created (resource created), 400 Bad Request (invalid client input), 401 Unauthorized (unauthenticated), 403 Forbidden (authenticated but no permission), 404 Not Found (resource missing), 500 Internal Server Error (unhandled server crash).",
     "Example: Requesting an unknown ticker returns 400 with a structured error JSON message."),

    ("What is API rate limiting and why is it essential?",
     "A strategy to control the rate of incoming requests from a client within a specified timeframe (e.g., 60 requests per minute).",
     "Prevents denial-of-service (DoS) attacks, ensures fair resource sharing, and protects third-party API quotas.",
     "Example: StockSense AI caches quote requests in memory to avoid exceeding Yahoo Finance's connection limits."),

    ("How do you secure API endpoints in Django REST Framework?",
     "By applying permission classes such as `IsAuthenticated` or `AllowAny`, and authentication classes such as `SessionAuthentication` or `TokenAuthentication`.",
     "Example: `@permission_classes([IsAuthenticated])` ensures only logged-in users can record portfolio transactions."),

    ("What is an API contract and why is it important?",
     "A formal agreement defining endpoint URLs, HTTP methods, expected request parameters/headers, and structured JSON response schemas.",
     "Ensures frontend and backend developers can develop independently without integration mismatches.",
     "Example: `/api/predictions/<symbol>/` guarantees returning `success`, `predicted_price`, `metrics`, and `future_forecast` keys."),

    ("What is JSON serialization in Django REST Framework?",
     "The process of translating complex Django model instances or QuerySets into native Python datatypes that can be rendered into JSON.",
     "Serializers also handle deserialization, validating incoming client payloads before saving to database models.",
     "Example: `NewsArticleSerializer(articles, many=True).data` converts article QuerySets into clean JSON dictionaries."),

    ("What is the difference between REST and GraphQL?",
     "REST exposes multiple fixed endpoints returning fixed data structures; GraphQL exposes a single endpoint where clients query exact fields needed in a single request.",
     "REST is simpler to cache via standard HTTP caching proxies; GraphQL prevents over-fetching and under-fetching.",
     "Example: StockSense AI uses REST endpoints for clean, standard HTTP caching."),

    ("What is CORS and how does a preflight `OPTIONS` request work?",
     "Cross-Origin Resource Sharing is a browser security protocol. When a client makes a complex request across origins, the browser sends an `OPTIONS` request first.",
     "The server must respond with headers like `Access-Control-Allow-Methods` and `Access-Control-Allow-Origin` before the browser sends the actual request.",
     "Example: Configured via `django-cors-headers` middleware."),

    ("What is API versioning and how is it achieved?",
     "Managing changes to an API without breaking existing client integrations.",
     "Common strategies: URL path versioning (`/api/v1/stocks/`), query parameters (`?version=1`), or custom request headers (`Accept: application/vnd.company.v1+json`).",
     "Example: StockSense AI exposes `/api/` endpoints ready for `/api/v2/` expansion."),

    ("What is an idempotent HTTP method?",
     "An HTTP method where multiple identical requests produce the exact same server state as a single request.",
     "GET, PUT, and DELETE are idempotent; POST is not (submitting multiple POST requests creates multiple records).",
     "Example: `GET /api/stocks/TCS.NS/` can be executed 100 times without altering any stock price records."),

    ("What are webhooks and how do they differ from polling?",
     "Polling involves the client repeatedly querying an endpoint on an interval. Webhooks are automated push notifications where the server sends an HTTP POST to the client when an event occurs.",
     "Webhooks are more efficient, eliminating wasteful empty polling queries.",
     "Example: When an external broker fills an order, it sends a webhook to update the user's transaction ledger."),

    ("What is an API gateway?",
     "A reverse proxy that sits between clients and microservices, handling routing, SSL termination, rate limiting, authentication, and load balancing centrally.",
     "Example: Kong, AWS API Gateway, or Nginx managing traffic across backend service pods."),

    ("How do you handle API pagination in Django REST Framework?",
     "By configuring a pagination class (`PageNumberPagination` or `LimitOffsetPagination`) in `REST_FRAMEWORK` settings.",
     "Splits large datasets into smaller chunks (e.g., 20 items per page) with `next` and `previous` navigation links.",
     "Example: `PAGE_SIZE = 20` prevents loading 100,000 historical price candles in a single memory-heavy response."),

    ("What is Bearer Token Authentication in APIs?",
     "An HTTP authentication scheme where the client includes an encrypted token in the `Authorization` header: `Authorization: Bearer <token>`.",
     "The server validates the token on each request without requiring session cookies, making it ideal for mobile apps and single-page apps.",
     "Example: JSON Web Tokens (JWT) containing encoded user IDs and expiration timestamps."),

    ("How do you test REST API endpoints automatically in Django?",
     "Using Django REST Framework's `APIClient` inside `TestCase` classes, asserting status codes, headers, and JSON content.",
     "Example: `response = self.client.get('/api/news/?symbol=TCS.NS'); self.assertEqual(response.status_code, 200)`.")
]

QA_DATA["Machine_Learning"] = [
    ("What is the difference between supervised and unsupervised learning?",
     "Supervised learning trains on labeled data (features X paired with target labels y); unsupervised learning finds hidden patterns or clusters in unlabeled data X without targets.",
     "Example: Time-series price regression is supervised; clustering stocks into risk categories based on correlation is unsupervised."),

    ("What is overfitting and how do you detect and prevent it?",
     "Overfitting occurs when a model learns noise and peculiarities of training data rather than underlying patterns, performing well on training data but poorly on test data.",
     "Prevented by using cross-validation, regularization (L1/L2), dropout layers in neural networks, early stopping, and simpler model architectures.",
     "Example: In our LSTM model, `Dropout(0.2)` and `EarlyStopping(patience=5)` prevent memorizing noise."),

    ("What is underfitting?",
     "Underfitting happens when a model is too simple to capture the underlying structure of the data, resulting in poor accuracy on both training and test sets.",
     "Solved by adding more relevant features, increasing model complexity (e.g., moving from Linear Regression to Random Forest), or reducing regularization.",
     "Example: A single constant line underfits a complex oscillating stock price trend."),

    ("What is the bias-variance tradeoff?",
     "High bias causes underfitting (oversimplified assumptions); high variance causes overfitting (excessive sensitivity to training fluctuations).",
     "The optimal model minimizes total error by balancing bias and variance.",
     "Example: Our Hybrid Ensemble balances the high bias of linear ARIMA with the high variance of deep LSTM."),

    ("Why do we normalize or scale features before training neural networks?",
     "Neural networks use gradient descent. Unscaled features with large numerical magnitudes (e.g., Volume in millions vs Price in hundreds) create elongated gradient contours that slow or destabilize convergence.",
     "Scaling transforms features into a uniform range (e.g., 0 to 1 via `MinMaxScaler`), ensuring smooth, isotropic gradient steps.",
     "Example: In `TimeSeriesDataPipeline`, prices and volumes are scaled to `[0, 1]`."),

    ("What is the difference between `MinMaxScaler` and `StandardScaler`?",
     "`MinMaxScaler` bounds data into a fixed interval `[0, 1]` based on minimum and maximum values. `StandardScaler` centers data around mean 0 with unit variance (standard deviation 1).",
     "`MinMaxScaler` is preferred for neural networks with bounded activation functions (e.g., Sigmoid, Tanh); `StandardScaler` is preferred when outliers are present.",
     "Example: `MinMaxScaler` is used in our LSTM pipeline."),

    ("What is Gradient Descent and what is a learning rate?",
     "An iterative optimization algorithm that minimizes a loss function by taking steps proportional to the negative of the gradient.",
     "The learning rate determines the size of each step: too high causes divergence; too low results in slow training or getting stuck in local minima.",
     "Example: In `ForecastingService`, Adam optimizer uses `learning_rate=0.001`."),

    ("What is the Adam optimizer and why is it preferred?",
     "Adaptive Moment Estimation: an optimization algorithm that combines the advantages of AdaGrad (handling sparse gradients) and RMSProp (handling non-stationary objectives).",
     "It maintains individual adaptive learning rates for each parameter based on first and second moments of the gradients.",
     "Example: Default optimizer for our Keras LSTM models."),

    ("What is an activation function and why is non-linearity necessary in neural networks?",
     "A mathematical function applied to a neuron's weighted sum (e.g., ReLU, Sigmoid, Tanh).",
     "Without non-linear activation functions, stacking multiple neural network layers collapses mathematically into a single linear transformation, unable to learn complex non-linear patterns.",
     "Example: ReLU (`f(x) = max(0, x)`) is used in dense layers for computational efficiency and preventing vanishing gradients."),

    ("What is the Vanishing Gradient problem in Recurrent Neural Networks?",
     "During backpropagation through time, gradients are repeatedly multiplied by weight matrices. In deep or long sequences, gradients shrink exponentially to zero, preventing earlier layers from learning.",
     "LSTMs solve this by introducing an internal cell state with additive updates controlled by gating mechanisms.",
     "Example: Allows the LSTM to retain price memory across a 30-day lookback sequence."),

    ("How do the gates in an LSTM work?",
     "Forget Gate decides what information to discard from the cell state; Input Gate decides which new information to store; Output Gate controls what parts of the cell state to output to the hidden state.",
     "All gates use Sigmoid activations to produce values between 0 (completely block) and 1 (completely let through).",
     "Example: A forget gate can learn to discard price levels when a company executes a stock split."),

    ("What is Mean Squared Error (MSE) vs Mean Absolute Error (MAE)?",
     "MAE is the average of absolute differences: `(1/N) * sum(|y_true - y_pred|)`. MSE squares errors before averaging: `(1/N) * sum((y_true - y_pred)^2)`.",
     "MSE penalizes large outlier mistakes much more heavily than MAE due to the squaring operation.",
     "Example: In StockSense AI, we display MAE and RMSE so analysts see both average error and the impact of large deviations."),

    ("What is Root Mean Squared Error (RMSE)?",
     "The square root of MSE: `sqrt(MSE)`. It returns the metric into the original units of the target variable (e.g., Rupees or Dollars), making it directly interpretable alongside prices.",
     "Example: An RMSE of Rs 45.20 indicates that typical prediction errors are in the 45-rupee magnitude."),

    ("What is Directional Accuracy and how is it calculated?",
     "The percentage of trading days where the model correctly predicted the sign (+ or -) of the price change relative to the previous day.",
     "`DA = (sum(sign(y_pred_t - y_{t-1}) == sign(y_true_t - y_{t-1})) / N) * 100`.",
     "Example: A model predicting 60 out of 100 daily price directions correctly has 60% Directional Accuracy."),

    ("What is a confusion matrix?",
     "A performance measurement table for classification problems with four quadrants: True Positives (TP), True Negatives (TN), False Positives (FP), and False Negatives (FN).",
     "Allows calculating Precision, Recall, Specificity, and F1-Score.",
     "Example: Classifying whether tomorrow is an UP day or DOWN day."),

    ("What is regularized regression (L1 Lasso vs L2 Ridge)?",
     "L1 (Lasso) adds a penalty equal to the absolute value of coefficients, driving non-essential coefficients to zero (feature selection). L2 (Ridge) penalizes squared coefficients, shrinking weights smoothly.",
     "Prevents multicollinearity and overfitting in linear models.",
     "Example: Using Ridge regression when multiple moving average indicators are highly correlated."),

    ("What is hyperparameter tuning and how is it performed?",
     "The process of selecting optimal configuration variables (learning rate, tree depth, number of estimators) that are not learned directly during training.",
     "Common techniques include Grid Search (exhaustive search over parameter combinations), Random Search, and Bayesian Optimization.",
     "Example: Searching optimal lookback windows between 10, 20, and 30 days."),

    ("What is an ensemble model and what are the main types?",
     "A technique combining predictions from multiple diverse models to produce better generalizability than any single model.",
     "Main types: Bagging (e.g., Random Forest), Boosting (e.g., XGBoost, Gradient Boosting), and Blending/Stacking (e.g., our Hybrid LSTM-ARIMA).",
     "Example: Blending linear ARIMA with non-linear LSTM reduces overall test MSE."),

    ("What is the curse of dimensionality?",
     "As the number of features (dimensions) increases, the volume of the feature space grows exponentially, causing data points to become sparse.",
     "Requires exponentially more data to prevent overfitting and makes distance metrics less meaningful.",
     "Example: Limiting stock features to essential momentum and volatility metrics rather than adding 200 redundant indicators."),

    ("Why is model interpretability important in finance?",
     "Financial institutions face regulatory compliance requirements where investment decisions, risk models, and algorithmic recommendations must be explainable to auditors and clients.",
     "Black-box predictions without clear feature attributions carry legal and capital risk.",
     "Example: StockSense AI explicitly displays model architecture, evaluation errors, and disclaimers rather than opaque buy signals.")
]

QA_DATA["NLP_Sentiment"] = [
    ("What is Natural Language Processing (NLP)?",
     "A subfield of artificial intelligence focused on enabling computers to understand, interpret, and generate human language.",
     "In finance, NLP analyzes corporate annual reports, earnings calls, and news headlines to gauge market sentiment.",
     "Example: Parsing financial headlines to determine market sentiment on TCS."),

    ("What is a sentiment lexicon?",
     "A curated dictionary of words mapped to predefined emotional polarities or numerical sentiment weights.",
     "Example: In VADER, 'rally' has a positive score (+2.1), while 'plunge' has a negative score (-2.4)."),

    ("How does VADER handle punctuation, capitalization, and emojis?",
     "VADER applies heuristic rules: exclamation marks increase intensity ('rally!' vs 'rally!!!'); ALL-CAPS words boost intensity ('SURGE' vs 'surge'); negation words invert polarity ('not bad').",
     "These rules make it particularly effective for social and media text without requiring deep syntactic parsing.",
     "Example: 'TCS reports HUGE profit surge!' scores higher than 'TCS reports profit surge'."),

    ("What is tokenization in NLP?",
     "The process of breaking a continuous stream of text into individual units (tokens), such as words, subwords, or characters.",
     "The first essential step in any NLP preprocessing pipeline.",
     "Example: 'Tata Consultancy Services' is tokenized into `['Tata', 'Consultancy', 'Services']`."),

    ("What are stop words and why are they sometimes removed?",
     "Common words (e.g., 'the', 'is', 'at', 'which') that appear frequently across all documents and carry little discriminative information.",
     "Removing them reduces vocabulary size and computational overhead in traditional bag-of-words models.",
     "Example: VADER retains negation stop words like 'not' and 'never' because removing them would alter sentiment completely."),

    ("What is stemming vs lemmatization?",
     "Stemming is a crude heuristic process that chops off word ends (e.g., 'running' -> 'run', 'studies' -> 'studi'). Lemmatization uses vocabulary and morphological analysis to return the base dictionary form (lemma) (e.g., 'better' -> 'good', 'studies' -> 'study').",
     "Example: Lemmatization is more linguistically accurate but computationally slower than stemming."),

    ("What is TF-IDF?",
     "Term Frequency-Inverse Document Frequency: a numerical statistic reflecting how important a word is to a document in a corpus.",
     "`TF` measures frequency in a document; `IDF` down-weights words that appear across all documents (like 'stock' or 'market').",
     "Example: A financial report mentioning 'lithium' 20 times when other reports rarely mention it gives 'lithium' a high TF-IDF score."),

    ("What are word embeddings (e.g., Word2Vec, GloVe)?",
     "Dense vector representations of words in continuous vector spaces where semantically similar words are positioned close together.",
     "Captures relationships like `vector('King') - vector('Man') + vector('Woman') ~ vector('Queen')`.",
     "Example: 'Bullish' and 'Optimistic' share similar directional vector coordinates."),

    ("What is the Transformer architecture in NLP?",
     "A deep learning architecture introduced in 2017 ('Attention Is All You Need') relying entirely on self-attention mechanisms to compute representations of input and output without recurrent sequential steps.",
     "Forms the foundation of modern Large Language Models like BERT, GPT, and Gemini.",
     "Example: Transformers process entire sentences in parallel rather than token-by-token."),

    ("What is Self-Attention in simple terms?",
     "A mechanism that allows a model to weigh the importance of different words in a sentence relative to each other, regardless of their positional distance.",
     "Example: In 'The bank refused the loan because it was insolvent', self-attention connects 'it' to 'bank' rather than 'loan' based on semantic context."),

    ("What is FinBERT?",
     "A domain-specific BERT language model pre-trained and fine-tuned on financial corpora (corporate 10-K filings, earnings call transcripts, analyst reports).",
     "Standard NLP models might classify 'share' as positive or neutral, but FinBERT understands financial terminology like 'cost of capital', 'liability', and 'headwinds'.",
     "Example: FinBERT accurately scores 'debt restructuring' as cautionary rather than positive."),

    ("Why is financial news sentiment analysis challenging?",
     "1. Complex domain vocabulary and nuanced phrasing. 2. Heavy context dependence ('interest rates rose' is bad for tech stocks but good for banks). 3. Sarcasm, market rumors, and rapid temporal decay.",
     "A news item published 48 hours ago is already fully priced into market quotes.",
     "Example: Headline sentiment must be weighted by publication recency to maintain analytical relevance."),

    ("How do you clean raw HTML from RSS descriptions?",
     "Using regular expressions (`re.sub(r'<[^>]+>', ' ', text)`) and `html.unescape` to decode entities like `&amp;` and `&bull;`.",
     "In `NewsSentimentService`, description text is cleaned and stripped of extra whitespace to construct readable summaries.",
     "Example: `<a href='...'>Headline</a>&nbsp;&nbsp;Source` converts cleanly to `Headline Source`."),

    ("What is the compound score in VADER and how is it normalized?",
     "The compound score is computed by summing the valence scores of each word in the lexicon, adjusted according to heuristics, and normalized between -1 and +1 using: `x / sqrt(x^2 + alpha)` where alpha is typically 15.",
     "Provides a single unidimensional measure of overall sentiment.",
     "Example: A score of +0.65 indicates strong positive consensus."),

    ("How do you handle situations when an external news API is down?",
     "Through a tiered fallback architecture: 1. Try primary API. 2. On error, try secondary RSS feed. 3. If all network feeds fail, load previously saved articles from the local database.",
     "The view serves cached records with an informational banner, ensuring the page never crashes or displays empty.",
     "Example: When testing in offline mode, previously saved TCS news items render seamlessly.")
]

QA_DATA["Project_Specific"] = [
    ("Why did you decide to build StockSense AI as your final year project?",
     "I wanted to build an end-to-end, production-grade financial platform that combined my passions for Python backend engineering, financial analytics, and applied machine learning.",
     "Most student stock projects are either basic Flask dashboards with hardcoded tables or unrealistic '99% accurate' black-box scripts. I wanted to build an institutional-grade platform with real data, auditability, and zero data leakage.",
     "Example: Implementing 5 different forecasting models with walk-forward evaluation showcases practical data science engineering."),

    ("What is the exact directory layout of your project?",
     "A modular Django structure: root project folder contains `config/` (settings, urls, wsgi), `apps/` partitioned into 8 domain apps (`accounts`, `market`, `portfolio`, `watchlists`, `analytics`, `predictions`, `news`, `assistant`), `templates/`, `static/`, `tests/`, `ml_models/`, and `manage.py`.",
     "This separation ensures each app remains decoupled and maintainable.",
     "Example: Swapping news providers only touches `apps/news/` without risking breaking `apps/portfolio/`."),

    ("How many Django apps are in your project and what does each do?",
     "8 apps: 1. `accounts` (auth, sessions, profiles), 2. `market` (quotes, history, screener), 3. `portfolio` (ledger, positions, FIFO), 4. `watchlists` (custom lists, price alerts), 5. `analytics` (technical indicators), 6. `predictions` (ML models, evaluation), 7. `news` (RSS, VADER sentiment), 8. `assistant` (Gemini RAG copilot).",
     "Each app follows the Single Responsibility Principle.",
     "Example: Keeps code modular, readable, and interview-explainable."),

    ("Explain the authentication bug you resolved with special characters in usernames.",
     "Users registered with '@' in their username (e.g., `Kiran@123`) were unable to log in because the default backend treated any input containing '@' strictly as an email query.",
     "If `email == 'Kiran@123'` returned no record, login failed even though the username existed.",
     "I created `EmailOrUsernameModelBackend` which queries: `User.objects.filter(Q(email__iexact=ident) | Q(username__iexact=ident)).first()`, resolving the issue permanently.",
     "Example: Users can now log in using either email or usernames containing special characters."),

    ("Explain the ML Forecasting bug where the browser displayed `SyntaxError: Unexpected token '<'`.",
     "The frontend clicked 'Execute Model' and expected a JSON response from `/api/predictions/<symbol>/`. However, due to unhandled exceptions or route redirects, Django returned an HTML error page (`<!DOCTYPE html>`).",
     "When JavaScript called `response.json()`, parsing an HTML page threw the SyntaxError.",
     "I fixed this by: 1. Ensuring API views return `JsonResponse` or DRF `Response` with proper status codes (400 on error), 2. Updating frontend JS to check `response.ok` and `Content-Type: application/json` before calling `.json()`.",
     "Example: If an invalid ticker is submitted, the frontend displays a structured toast message rather than crashing."),

    ("Explain the News Sentiment bug where the page was blank or showed 0 articles.",
     "`yfinance.Ticker.news` relied on Yahoo Finance's internal API via `curl_cffi`, which threw abrupt connection drop errors on Windows (`curl 56 Connection closed`).",
     "The exception handler caught this and fell back to `NewsArticle.objects.all()`, which had 0 records in SQLite, resulting in an empty list and blank screen.",
     "I replaced it with a multi-tier pipeline: Google News Financial RSS as default, NewsAPI.org as optional, and VADER scoring with SQLite persistence.",
     "Example: TCS.NS now instantly fetches 25 verified articles with 52% Positive, 40% Neutral, and 8% Negative distribution metrics."),

    ("Where are pre-trained machine learning models stored?",
     "Trained model artifacts, weights, and scalers are saved in the `ml_models/` directory configured in `settings.py`: `ML_MODELS_DIR = BASE_DIR / 'ml_models'`.",
     "Scikit-learn and ARIMA pipelines are serialized using `joblib`, while Keras LSTM networks are saved in standard `.keras` format.",
     "Example: Models can be loaded instantly for inference without re-running 50-epoch training on every page load."),

    ("How does the platform handle timezones for Indian vs US market sessions?",
     "All internal database dates are stored in UTC (`USE_TZ = True`). In `MarketDataService`, the market status beacon checks local trading hours: IST (09:15 to 15:30) for NSE/BSE and EST (09:30 to 16:00) for US exchanges.",
     "Example: Shows 'Market Open' during Indian hours for TCS and 'Market Closed' during evening hours."),

    ("What is the difference between `Stock` and `HistoricalPrice` models?",
     "`Stock` stores high-level metadata: ticker symbol, company name, exchange, sector, currency, and active status. `HistoricalPrice` stores daily OHLCV price series linked via a ForeignKey to `Stock`.",
     "Example: One `Stock` row has 500+ related `HistoricalPrice` rows representing daily trading sessions."),

    ("How do you ensure historical price records are not duplicated?",
     "Through a composite unique constraint in `HistoricalPrice.Meta`: `unique_together = ('stock', 'date')`.",
     "When caching daily prices, the service uses `bulk_create(records, ignore_conflicts=True)` or `update_or_create` to ensure idempotency.",
     "Example: Running data ingestion twice on the same day never creates duplicate candles."),

    ("How does your portfolio transaction ledger record buys and sells?",
     "Each trade creates a row in the `Transaction` table with `type` ('BUY' or 'SELL'), `shares`, `price`, `execution_date`, and optional `notes`.",
     "Holdings are derived dynamically by aggregating buy lots and deducting executed sell orders.",
     "Example: `Transaction.objects.filter(portfolio=p, stock=s)`."),

    ("What validation rules protect the portfolio from invalid transactions?",
     "1. Share quantities must be strictly positive (`shares > 0`). 2. Execution price must be positive (`price > 0`). 3. Sell orders cannot exceed the user's currently open share balance.",
     "Validation is enforced in `PortfolioAnalyticsService.record_transaction()` before database commit.",
     "Example: Submitting -5 shares or selling 100 shares when owning 50 immediately raises a `ValidationError`."),

    ("How does the Screener feature work under the hood?",
     "The user selects filters: Sector (IT, Banking, Energy), Exchange (NSE, NASDAQ), Min/Max Price, and Technical Indicators (RSI, MA).",
     "`MarketDataService.screen_stocks()` filters the active universe and returns matching equities with current prices and daily change percentages.",
     "Example: Selecting 'Sector: IT' and 'RSI < 45' returns TCS and Infosys for accumulation analysis."),

    ("How does the Stock Comparison tool work?",
     "It normalizes closing price series for up to 4 selected equities to a common baseline of 100 on the start date: `Normalized_t = (Price_t / Price_0) * 100`.",
     "Plotly.js renders the normalized percentage series on a single multi-line chart, allowing direct visual comparison of relative performance regardless of absolute stock prices.",
     "Example: Allows comparing TCS (trading at Rs 3,400) directly with Apple (trading at $180) over a 1-year timeline."),

    ("What is the demo trader account configured in the database?",
     "Username: `demo_trader`, Password: `StockSense@2026`.",
     "It comes pre-populated with a demo portfolio containing real transactions (TCS, Reliance, Apple), custom watchlists, and price alerts for immediate evaluation.",
     "Example: Interviewers can click 'Use Demo Credentials' on the login page to inspect the live workspace in one click."),

    ("How does the RAG (Retrieval-Augmented Generation) copilot work?",
     "When a user submits a query to the Research Assistant, the service extracts mentioned stock tickers, fetches real-time quotes, technical indicator values, and user portfolio holdings.",
     "These verified factual data points are injected into the prompt sent to Google Gemini (`gemini-2.5-flash`), grounding the response in real platform data.",
     "Example: Asking 'Analyze my TCS position' provides Gemini with exact purchase cost, current price, unrealized P&L, and 14-day RSI."),

    ("What is the fallback mechanism if Gemini API key is missing or quota is exhausted?",
     "The assistant falls back to a deterministic rule-based quantitative engine that evaluates indicator conditions (RSI overbought/oversold, MACD crossovers, MA trends) and returns structured analysis.",
     "Ensures the feature never breaks even in air-gapped or unauthenticated environments.",
     "Example: Users without API keys still receive clear technical analysis."),

    ("How is the database pre-seeded with stocks?",
     "Via a custom Django management command: `python manage.py seed_stocks`.",
     "The command populates the database with 30+ top Indian and US equities, their exchanges, industry sectors, and currencies.",
     "Example: Runs automatically during build steps on cloud deployment platforms."),

    ("How are technical indicator calculations tested for mathematical accuracy?",
     "In `tests/test_platform.py`, synthetic price series with known mathematical values are fed into `TechnicalIndicatorService`.",
     "Tests assert that RSI stays bounded between 0 and 100, SMA matches rolling arithmetic means, and Bollinger Bands maintain `Upper > Middle > Lower`.",
     "Example: `self.assertTrue((df['bb_upper'] >= df['bb_middle']).all())`."),

    ("What happens when an invalid stock symbol is passed to the ML prediction API?",
     "The view validates the symbol. If `MarketDataService.get_stock_history()` returns an empty dataframe (e.g. invalid ticker `XYZ123`), the API immediately returns HTTP 400 Bad Request with: `{'success': False, 'error': 'Invalid or unresolvable equity symbol: XYZ123'}`.",
     "Prevents unhandled crashes and provides clean user feedback.",
     "Example: Tested via `test_api_predict_invalid_symbol_returns_json_error` in unit test suite."),

    ("How does the Watchlist toggle API work?",
     "`POST /api/watchlists/toggle/<symbol>/` adds the stock to the user's default watchlist if absent, or removes it if already present.",
     "Returns a JSON response with `{action: 'added' | 'removed', symbol: '...'}`.",
     "Example: Clicking the star icon on any stock page dynamically toggles watchlist tracking without reloading."),

    ("How does the Price Alert evaluation service work?",
     "`PriceAlertService.check_alerts()` queries all `ACTIVE` alerts, fetches current prices for their associated stocks, and compares them against target thresholds.",
     "If triggered, it updates `is_triggered = True` and records `triggered_at = timezone.now()`.",
     "Example: Can be run on a periodic schedule (e.g. via Celery Beat or cron)."),

    ("How are static files and templates organized in StockSense AI?",
     "`templates/` contains shared layouts (`base.html`), reusable components (`components/sidebar.html`, `navbar.html`), and app-specific directories (`market/`, `portfolio/`, `news/`).",
     "`static/` contains modular CSS (`stocksense.css`) and JavaScript libraries (`stocksense.js`, `charts.js`).",
     "Example: Base template defines blocks (`{% block content %}`) extended by child pages."),

    ("Why did you use Plotly.js instead of Chart.js or D3.js?",
     "Plotly.js has native out-of-the-box support for high-performance financial candlestick charts, multi-panel subplots (volume, RSI, MACD), range sliders, and hover tooltips.",
     "Chart.js requires third-party plugins for candlesticks; D3.js requires thousands of lines of low-level canvas code.",
     "Example: Plotly's candlestick trace renders OHLC wicks and bodies in 2 lines of configuration."),

    ("What HTTP headers are sent by the frontend for secure AJAX requests?",
     "`X-CSRFToken` containing the value read from `document.cookie` or meta tags, and `Accept: application/json`.",
     "Example: `fetch(url, {method: 'POST', headers: {'X-CSRFToken': getCookie('csrftoken')}})`."),

    ("What is the role of `requirements.txt` in your project?",
     "Lists all external Python dependencies with pinned minimum versions (Django 5, pandas, yfinance, tensorflow, vaderSentiment, etc.) for reproducible environment installation.",
     "Example: `pip install -r requirements.txt` reinstalls the exact environment on any machine."),

    ("How is the project configured for production deployment on Render or Railway?",
     "1. `gunicorn config.wsgi:application` as the web process. 2. `WhiteNoiseMiddleware` for static asset serving. 3. Environment variables configured in dashboard (`DEBUG=False`, `SECRET_KEY`, `ALLOWED_HOSTS`, `DATABASE_URL`).",
     "Example: Documented step-by-step in `README.md`."),

    ("What are the key differences between the original Flask app and this Django platform?",
     "Original Flask app was a single 600-line monolithic file with basic routes and in-memory variables. Django platform is a full-stack architecture with 8 modular apps, persistent database models, double-entry portfolio ledger, 5 ML models, VADER news sentiment, user auth, and 22 automated tests.",
     "Example: Migrated from an exploratory prototype to an institutional-grade full-stack platform."),

    ("How many unit and integration tests are in your automated test suite?",
     "22 comprehensive automated tests in `tests/test_platform.py`.",
     "Covering User Authentication, Market Data Ingestion, Technical Indicators, Portfolio Accounting, Watchlists & Alerts, Machine Learning Pipelines, and News Sentiment Analysis.",
     "Example: All 22 tests pass cleanly in under 95 seconds via `python manage.py test tests.test_platform`."),

    ("If you had another month to work on StockSense AI, what would you add next?",
     "1. WebSocket integration via Django Channels for live sub-second order book streaming. 2. Brokerage API integration (e.g. Zerodha Kite Connect or Alpaca) for paper trading execution. 3. Advanced portfolio optimization (Black-Litterman and Sharpe Ratio efficient frontier). 4. FinBERT sentiment model fine-tuning on Indian financial news.",
     "Shows maturity, strategic engineering vision, and practical product understanding.")
]

# Write out docs/qa_bank.py
with open(os.path.join(os.path.dirname(__file__), 'qa_bank.py'), 'w', encoding='utf-8') as f:
    f.write('"""\nStockSense AI - Master Interview Question Bank\nAuto-compiled database of 235+ categorized technical questions and answers.\n"""\n\n')
    f.write('QA_DATABASE = ' + repr(QA_DATA) + '\n')

print(f"Successfully generated docs/qa_bank.py with {sum(len(v) for v in QA_DATA.values())} questions across {len(QA_DATA)} categories!")
for cat, qs in QA_DATA.items():
    print(f" - {cat}: {len(qs)} questions")
