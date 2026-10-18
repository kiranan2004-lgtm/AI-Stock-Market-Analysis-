import numpy as np
import pandas as pd
from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.accounts.models import UserProfile
from apps.market.models import Stock, HistoricalPrice
from apps.market.services import MarketDataService
from apps.portfolio.models import Portfolio, Transaction
from apps.portfolio.services import PortfolioAnalyticsService
from apps.watchlists.models import Watchlist, WatchlistItem, PriceAlert
from apps.watchlists.services import WatchlistService
from apps.analytics.services import TechnicalIndicatorService
from apps.predictions.services.pipeline import TimeSeriesDataPipeline, ModelEvaluator
from apps.predictions.services.forecasting import ForecastingService

class UserAuthenticationTests(TestCase):
    """Test user registration, login, special username handling, demo credentials, session persistence, and logout."""

    def setUp(self):
        self.client = Client()
        self.kiran_user = User.objects.create_user(
            username='Kiran@123',
            email='kiranan2004@gmail.com',
            password='Password@123',
            first_name='Kiran',
            last_name='Kumar'
        )
        self.demo_user = User.objects.create_user(
            username='demo_trader',
            email='trader@stocksense.ai',
            password='StockSense@2026'
        )

    def test_user_creation_and_profile_signal(self):
        user = User.objects.create_user(
            username='investor1',
            email='investor1@example.com',
            password='TestPassword123'
        )
        self.assertIsNotNone(user.profile)
        self.assertEqual(user.profile.preferred_currency, 'INR')

    def test_login_with_username_containing_at_symbol(self):
        """Users with '@' in their username (e.g., Kiran@123) must be able to log in successfully."""
        response = self.client.post('/login/', {
            'username': 'Kiran@123',
            'password': 'Password@123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard/', response.url)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.kiran_user.id)

    def test_login_with_email_address(self):
        """Users must be able to log in using their registered email address."""
        response = self.client.post('/login/', {
            'username': 'kiranan2004@gmail.com',
            'password': 'Password@123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard/', response.url)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.kiran_user.id)

    def test_login_case_insensitivity_and_whitespace_trimming(self):
        """Username/email lookups should be case-insensitive and trim outer whitespace."""
        response = self.client.post('/login/', {
            'username': '  kiran@123  ',
            'password': 'Password@123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.kiran_user.id)

    def test_demo_credentials_login(self):
        """Demo trader account must log in successfully with configured credentials."""
        response = self.client.post('/login/', {
            'username': 'demo_trader',
            'password': 'StockSense@2026'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard/', response.url)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.demo_user.id)

    def test_incorrect_password_rejected(self):
        """Incorrect passwords must be strictly rejected without bypassing authentication."""
        response = self.client.post('/login/', {
            'username': 'Kiran@123',
            'password': 'WrongPassword999'
        })
        # Stays on login page with error (HTTP 200)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertContains(response, "Invalid username/email or password.")

    def test_user_logout(self):
        """Logout must invalidate user session and redirect to login."""
        self.client.login(username='Kiran@123', password='Password@123')
        self.assertIn('_auth_user_id', self.client.session)

        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_session_persistence_across_simulated_server_restart(self):
        """
        Verify that database-backed sessions persist across server restarts or client reconnections.
        """
        from django.contrib.sessions.models import Session

        # 1. User logs in
        login_res = self.client.post('/login/', {
            'username': 'Kiran@123',
            'password': 'Password@123'
        })
        self.assertEqual(login_res.status_code, 302)

        # 2. Check session is saved in the database
        session_cookie = self.client.cookies.get('stocksense_sessionid')
        self.assertIsNotNone(session_cookie)
        session_key = session_cookie.value
        self.assertTrue(Session.objects.filter(session_key=session_key).exists())

        # 3. Simulate server restart: new client instance using the persisted session cookie
        new_client = Client()
        new_client.cookies['stocksense_sessionid'] = session_key

        # 4. Verify access to protected view without re-authenticating
        profile_res = new_client.get('/profile/')
        self.assertEqual(profile_res.status_code, 200)
        self.assertEqual(profile_res.context['user'].username, 'Kiran@123')

    def test_passwords_are_securely_hashed(self):
        """Verify passwords are never stored in plaintext and use standard PBKDF2 hashing."""
        self.assertTrue(self.kiran_user.password.startswith('pbkdf2_sha256$'))
        self.assertTrue(self.kiran_user.check_password('Password@123'))
        self.assertFalse(self.kiran_user.check_password('WrongPassword'))


class PortfolioAccountingAndValidationTests(TestCase):
    """Test portfolio position accounting, average cost basis, FIFO, and overselling guards."""

    def setUp(self):
        self.user = User.objects.create_user(username='portfoliouser', password='PassWord123!')
        self.portfolio = PortfolioAnalyticsService.get_or_create_default_portfolio(self.user)
        self.stock = Stock.objects.create(
            symbol='TCS.NS', name='Tata Consultancy Services',
            exchange='NSE', sector='IT', currency='INR'
        )

    def test_buy_and_sell_cost_basis_calculation(self):
        # 1. Buy 10 shares @ 3000 = 30,000 + 50 charges = 30,050 (avg: 3005)
        Transaction.objects.create(
            portfolio=self.portfolio, stock=self.stock,
            transaction_type='BUY', quantity=Decimal('10'),
            price=Decimal('3000.00'), charges=Decimal('50.00')
        )
        # 2. Buy 10 shares @ 4000 = 40,000 + 50 charges = 40,050
        # Total 20 shares, total cost = 70,100, avg cost = 3505.00
        Transaction.objects.create(
            portfolio=self.portfolio, stock=self.stock,
            transaction_type='BUY', quantity=Decimal('10'),
            price=Decimal('4000.00'), charges=Decimal('50.00')
        )

        res = PortfolioAnalyticsService.calculate_portfolio(self.portfolio)
        self.assertEqual(len(res['holdings']), 1)
        h = res['holdings'][0]
        self.assertEqual(h['shares'], Decimal('20'))
        self.assertEqual(h['avg_cost'], Decimal('3505.00'))

        # 3. Sell 5 shares @ 4500 (proceeds = 22,500 - 20 charges = 22,480)
        # Cost of 5 shares = 5 * 3505 = 17,525
        # Realized profit = 22,480 - 17,525 = 4,955
        Transaction.objects.create(
            portfolio=self.portfolio, stock=self.stock,
            transaction_type='SELL', quantity=Decimal('5'),
            price=Decimal('4500.00'), charges=Decimal('20.00')
        )

        res_after = PortfolioAnalyticsService.calculate_portfolio(self.portfolio)
        h_after = res_after['holdings'][0]
        self.assertEqual(h_after['shares'], Decimal('15'))
        self.assertEqual(res_after['realized_pl'], Decimal('4955.00'))

    def test_prevent_overselling_validation(self):
        # Only buy 5 shares
        Transaction.objects.create(
            portfolio=self.portfolio, stock=self.stock,
            transaction_type='BUY', quantity=Decimal('5'),
            price=Decimal('3000.00')
        )

        # Attempting to sell 10 shares must raise ValidationError
        with self.assertRaises(ValidationError):
            PortfolioAnalyticsService.validate_transaction(
                portfolio=self.portfolio, stock=self.stock,
                tx_type='SELL', quantity=Decimal('10')
            )


class TechnicalIndicatorCalculationTests(TestCase):
    """Test Pandas indicator calculations: SMA, EMA, RSI, MACD, Bollinger Bands, ATR."""

    def test_indicator_mathematical_formulas(self):
        # Create 100 days of deterministic test pricing data
        dates = pd.date_range('2025-01-01', periods=100)
        close_prices = np.linspace(100, 200, 100) + np.sin(np.linspace(0, 10, 100)) * 5
        df = pd.DataFrame({
            'Date': dates,
            'Open': close_prices - 1,
            'High': close_prices + 2,
            'Low': close_prices - 2,
            'Close': close_prices,
            'Volume': [100000] * 100
        })

        res = TechnicalIndicatorService.calculate_indicators(df)
        self.assertTrue(res['success'])
        s = res['summary']

        # Assert indicators are populated
        self.assertIsNotNone(s['sma_20'])
        self.assertIsNotNone(s['sma_50'])
        self.assertIsNotNone(s['rsi_14'])
        self.assertIsNotNone(s['macd_line'])
        self.assertIsNotNone(s['bb_upper'])
        self.assertIsNotNone(s['bb_lower'])
        self.assertIsNotNone(s['atr_14'])

        # Upper Bollinger Band must be strictly greater than lower Bollinger Band
        self.assertGreater(s['bb_upper'], s['bb_lower'])

        # RSI must be strictly bounded between 0 and 100
        self.assertGreaterEqual(s['rsi_14'], 0.0)
        self.assertLessEqual(s['rsi_14'], 100.0)


class MachineLearningDataPipelineTests(TestCase):
    """Test data splitting without data leakage and out-of-sample evaluation metrics."""

    def test_zero_data_leakage_and_chronological_split(self):
        dates = pd.date_range('2024-01-01', periods=100)
        prices = np.linspace(50, 150, 100)
        df = pd.DataFrame({'Date': dates, 'Close': prices})

        pipeline = TimeSeriesDataPipeline(sequence_length=10, test_ratio=0.2)
        train_p, test_p, scaled_train, scaled_test, all_p = pipeline.prepare_raw_data(df)

        # 80% train / 20% test split check
        self.assertEqual(len(train_p), 80)
        self.assertEqual(len(test_p), 20)

        # Scaler minimum must match train minimum (50.0), NOT test minimum
        self.assertAlmostEqual(pipeline.scaler.data_min_[0], 50.0)
        # Scaler maximum must match train maximum, NOT the overall highest test point
        self.assertAlmostEqual(pipeline.scaler.data_max_[0], train_p[-1])

    def test_model_evaluator_metrics(self):
        y_true = np.array([100.0, 105.0, 103.0, 110.0])
        y_pred = np.array([99.0, 104.0, 102.0, 111.0])

        metrics = ModelEvaluator.calculate_metrics(y_true, y_pred)
        self.assertEqual(metrics['mae'], 1.0)
        self.assertEqual(metrics['rmse'], 1.0)
        # Directional accuracy: all 3 direction steps match!
        self.assertEqual(metrics['directional_accuracy'], 100.0)


class WatchlistAndAlertTests(TestCase):
    """Test watchlists and price alerts monitoring."""

    def setUp(self):
        self.user = User.objects.create_user(username='alertuser', password='Password@123')
        self.stock = Stock.objects.create(
            symbol='INFY.NS', name='Infosys',
            exchange='NSE', sector='IT', currency='INR'
        )

    def test_watchlist_toggle(self):
        res1 = WatchlistService.toggle_stock_in_watchlist(self.user, 'INFY.NS')
        self.assertTrue(res1['success'])
        self.assertTrue(res1['is_in_watchlist'])

        # Toggle again removes it
        res2 = WatchlistService.toggle_stock_in_watchlist(self.user, 'INFY.NS')
        self.assertTrue(res2['success'])
        self.assertFalse(res2['is_in_watchlist'])

    def test_price_alert_trigger(self):
        alert = PriceAlert.objects.create(
            owner=self.user,
            stock=self.stock,
            target_price=Decimal('1500.00'),
            condition='ABOVE',
            status='ACTIVE'
        )
        self.assertEqual(alert.status, 'ACTIVE')


class ForecastingServiceAndApiTests(TestCase):
    """Test machine learning models execution, JSON response format, and error handling."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='mltrader', password='Password@123')
        self.stock = Stock.objects.create(
            symbol='TCS.NS', name='Tata Consultancy Services',
            exchange='NSE', sector='IT', currency='INR'
        )
        # Pre-seed 65 daily historical prices so tests run fast, deterministic, and offline
        from datetime import date, timedelta
        from decimal import Decimal
        from apps.market.models import HistoricalPrice
        base_price = 3200.0
        start_date = date.today() - timedelta(days=90)
        historical_records = []
        for i in range(65):
            d = start_date + timedelta(days=i)
            p = round(base_price + (i * 2.5) + (((i % 5) - 2) * 10.0), 2)
            historical_records.append(HistoricalPrice(
                stock=self.stock,
                date=d,
                open_price=Decimal(str(p - 5.0)),
                high_price=Decimal(str(p + 15.0)),
                low_price=Decimal(str(p - 10.0)),
                close_price=Decimal(str(p)),
                volume=1500000 + i * 1000
            ))
        HistoricalPrice.objects.bulk_create(historical_records, ignore_conflicts=True)

    def test_api_predict_json_contract_and_status(self):
        """API must return valid JSON with proper Content-Type application/json."""
        response = self.client.get('/api/predictions/TCS.NS/?model=linear&horizon=14')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.get('Content-Type', ''))
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('symbol'), 'TCS.NS')
        self.assertIn('predicted_price', data)
        self.assertIn('metrics', data)
        self.assertIn('future_forecast', data)
        self.assertEqual(len(data['future_forecast']), 14)

    def test_api_predict_invalid_symbol_returns_json_error(self):
        """API must return structured JSON with 400 status on unresolvable symbol rather than 500 HTML."""
        response = self.client.get('/api/predictions/NONEXISTENT_TICKER_999/?model=linear&horizon=7')
        self.assertEqual(response.status_code, 400)
        self.assertIn('application/json', response.get('Content-Type', ''))
        data = response.json()
        self.assertFalse(data.get('success'))
        self.assertIn('error', data)

    def test_predictions_view_authenticated(self):
        """Authenticated user can open the forecasting workspace and see default stock."""
        self.client.login(username='mltrader', password='Password@123')
        response = self.client.get('/predictions/?symbol=TCS.NS')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Machine Learning Econometric Forecasting")
        self.assertEqual(response.context['selected_symbol'], 'TCS.NS')


class NewsSentimentServiceAndViewsTests(TestCase):
    """Test real news ingestion, VADER sentiment calculation, template rendering, and REST API."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='newstrader', password='Password@123')
        self.stock = Stock.objects.create(
            symbol='TCS.NS',
            name='Tata Consultancy Services',
            exchange='NSE',
            sector='IT',
            currency='INR'
        )

    def test_news_service_live_ingestion_and_vader_scoring(self):
        """NewsSentimentService must ingest real articles, compute VADER sentiment, and return distribution metrics."""
        from apps.news.services import NewsSentimentService
        result = NewsSentimentService.get_stock_news('TCS.NS', force_refresh=True)

        self.assertIn('articles', result)
        self.assertIn('distribution', result)
        self.assertIn('provider', result)
        self.assertGreater(len(result['articles']), 0)

        dist = result['distribution']
        self.assertIn('positive_pct', dist)
        self.assertIn('neutral_pct', dist)
        self.assertIn('negative_pct', dist)
        self.assertIn('average_score', dist)
        self.assertEqual(dist['total_articles'], len(result['articles']))

        # Inspect first article
        art = result['articles'][0]
        self.assertTrue(len(art.headline) > 0)
        self.assertTrue(len(art.publisher) > 0)
        self.assertTrue(len(art.url) > 0)
        self.assertIn(art.sentiment_label, ['POSITIVE', 'NEUTRAL', 'NEGATIVE'])
        self.assertGreaterEqual(art.sentiment_score, -1.0)
        self.assertLessEqual(art.sentiment_score, 1.0)

    def test_news_html_view_authenticated(self):
        """Authenticated user can access /news/ with symbol filter and view rendered articles."""
        self.client.login(username='newstrader', password='Password@123')
        response = self.client.get('/news/?symbol=TCS.NS')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Financial Media & Sentiment Analytics")
        self.assertContains(response, "TCS.NS")
        self.assertIn('articles', response.context)
        self.assertIn('distribution', response.context)
        self.assertIn('provider', response.context)

    def test_api_news_json_endpoint(self):
        """API endpoint /api/news/ must return valid JSON with serialized articles and distribution."""
        response = self.client.get('/api/news/?symbol=TCS.NS')

        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.get('Content-Type', ''))
        data = response.json()
        self.assertEqual(data.get('symbol'), 'TCS.NS')
        self.assertIn('distribution', data)
        self.assertIn('articles', data)
        self.assertIsInstance(data['articles'], list)
        self.assertGreater(len(data['articles']), 0)
        self.assertIn('headline', data['articles'][0])
        self.assertIn('sentiment_score', data['articles'][0])

