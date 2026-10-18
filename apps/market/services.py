import datetime
import pytz
from decimal import Decimal
import pandas as pd
import numpy as np
from django.core.cache import cache
from django.utils import timezone
import yfinance as yf
from .models import Stock, HistoricalPrice

# Core curated universe preserving and expanding the project's original stocks
DEFAULT_STOCK_UNIVERSE = {
    # Indian IT Sector (NSE)
    'TCS.NS': {'name': 'Tata Consultancy Services', 'sector': 'Information Technology', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR'},
    'INFY.NS': {'name': 'Infosys Limited', 'sector': 'Information Technology', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR'},
    'WIPRO.NS': {'name': 'Wipro Limited', 'sector': 'Information Technology', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR'},
    'HCLTECH.NS': {'name': 'HCL Technologies', 'sector': 'Information Technology', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR'},
    'TECHM.NS': {'name': 'Tech Mahindra', 'sector': 'Information Technology', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR'},
    
    # Indian Banking & Finance (NSE)
    'HDFCBANK.NS': {'name': 'HDFC Bank Limited', 'sector': 'Banking', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR'},
    'ICICIBANK.NS': {'name': 'ICICI Bank Limited', 'sector': 'Banking', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR'},
    'SBIN.NS': {'name': 'State Bank of India', 'sector': 'Banking', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR'},
    'KOTAKBANK.NS': {'name': 'Kotak Mahindra Bank', 'sector': 'Banking', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR'},
    'AXISBANK.NS': {'name': 'Axis Bank Limited', 'sector': 'Banking', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR'},
    
    # Indian Energy & Conglomerates (NSE)
    'RELIANCE.NS': {'name': 'Reliance Industries Limited', 'sector': 'Energy & Conglomerate', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR'},
    'ONGC.NS': {'name': 'Oil and Natural Gas Corp', 'sector': 'Oil & Gas', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR'},
    'BPCL.NS': {'name': 'Bharat Petroleum Corp', 'sector': 'Oil & Gas', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR'},
    'ADANIGREEN.NS': {'name': 'Adani Green Energy', 'sector': 'Renewable Energy', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR'},
    'TATAPOWER.NS': {'name': 'Tata Power Company', 'sector': 'Utilities & Power', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR'},
    
    # US Technology (NASDAQ)
    'AAPL': {'name': 'Apple Inc.', 'sector': 'Technology', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD'},
    'MSFT': {'name': 'Microsoft Corporation', 'sector': 'Technology', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD'},
    'GOOGL': {'name': 'Alphabet Inc. (Google)', 'sector': 'Technology', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD'},
    'AMZN': {'name': 'Amazon.com Inc.', 'sector': 'Consumer Discretionary', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD'},
    'TSLA': {'name': 'Tesla Inc.', 'sector': 'Automotive & Clean Energy', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD'},
    'META': {'name': 'Meta Platforms Inc.', 'sector': 'Communication Services', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD'},
    'NVDA': {'name': 'NVIDIA Corporation', 'sector': 'Semiconductors', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD'},
    'NFLX': {'name': 'Netflix Inc.', 'sector': 'Entertainment', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD'},
    
    # US Financial (NYSE)
    'JPM': {'name': 'JPMorgan Chase & Co.', 'sector': 'Banking', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD'},
    'BAC': {'name': 'Bank of America Corp.', 'sector': 'Banking', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD'},
    'V': {'name': 'Visa Inc.', 'sector': 'Financial Services', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD'},
    'MA': {'name': 'Mastercard Incorporated', 'sector': 'Financial Services', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD'},
    
    # US Healthcare (NYSE)
    'JNJ': {'name': 'Johnson & Johnson', 'sector': 'Healthcare', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD'},
    'PFE': {'name': 'Pfizer Inc.', 'sector': 'Pharmaceuticals', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD'},
    'UNH': {'name': 'UnitedHealth Group', 'sector': 'Healthcare', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD'},
    
    # Major ETFs
    'SPY': {'name': 'SPDR S&P 500 ETF Trust', 'sector': 'Broad Market ETF', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD'},
    'QQQ': {'name': 'Invesco QQQ Trust (Nasdaq 100)', 'sector': 'Tech ETF', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD'},
    'VTI': {'name': 'Vanguard Total Stock Market ETF', 'sector': 'Total Market ETF', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD'},
}

MARKET_INDICES = {
    '^NSEI': {'name': 'NIFTY 50', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR'},
    '^BSESN': {'name': 'BSE SENSEX', 'exchange': 'BSE', 'country': 'India', 'currency': 'INR'},
    '^GSPC': {'name': 'S&P 500', 'exchange': 'US', 'country': 'USA', 'currency': 'USD'},
    '^IXIC': {'name': 'NASDAQ Composite', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD'},
}

class MarketDataService:
    """Production service for fetching, caching, and serving financial market data."""

    @staticmethod
    def get_stock_quote(symbol: str) -> dict:
        """
        Fetch the latest quote for a ticker symbol.
        Uses in-memory cache to respect API rate limits.
        """
        symbol = symbol.upper().strip()
        cache_key = f"stock_quote_{symbol}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        # Check local DB for stock metadata
        stock = Stock.objects.filter(symbol=symbol).first()
        info = DEFAULT_STOCK_UNIVERSE.get(symbol, {})
        name = stock.name if stock else info.get('name', symbol)
        exchange = stock.exchange if stock else info.get('exchange', 'NSE' if '.NS' in symbol else 'NASDAQ')
        sector = stock.sector if stock else info.get('sector', 'Equities')
        country = stock.country if stock else info.get('country', 'India' if '.NS' in symbol else 'USA')
        currency = stock.currency if stock else info.get('currency', 'INR' if '.NS' in symbol else 'USD')

        try:
            ticker = yf.Ticker(symbol)
            # Try fast_info first (much faster than .info)
            fast_info = getattr(ticker, 'fast_info', None)
            
            # Fetch last 5 days of 1d data for reliable previous close and price
            hist = ticker.history(period="5d", interval="1d")
            
            if hist is not None and not hist.empty:
                current_price = float(hist['Close'].iloc[-1])
                prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
                open_price = float(hist['Open'].iloc[-1])
                day_high = float(hist['High'].iloc[-1])
                day_low = float(hist['Low'].iloc[-1])
                volume = int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0
                
                change = current_price - prev_close
                change_pct = (change / prev_close * 100) if prev_close else 0.0

                fifty_two_week_high = float(fast_info.year_high) if fast_info and hasattr(fast_info, 'year_high') and fast_info.year_high else day_high
                fifty_two_week_low = float(fast_info.year_low) if fast_info and hasattr(fast_info, 'year_low') and fast_info.year_low else day_low

                quote = {
                    'symbol': symbol,
                    'name': name,
                    'exchange': exchange,
                    'sector': sector,
                    'country': country,
                    'currency': currency,
                    'currency_symbol': '₹' if currency == 'INR' else '$',
                    'current_price': round(current_price, 2),
                    'change': round(change, 2),
                    'change_pct': round(change_pct, 2),
                    'day_high': round(day_high, 2),
                    'day_low': round(day_low, 2),
                    'open_price': round(open_price, 2),
                    'prev_close': round(prev_close, 2),
                    'volume': volume,
                    'fifty_two_week_high': round(fifty_two_week_high, 2) if fifty_two_week_high else None,
                    'fifty_two_week_low': round(fifty_two_week_low, 2) if fifty_two_week_low else None,
                    'data_source': 'Yahoo Finance (Delayed ~15m)',
                    'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'success': True
                }

                # Cache quote for 90 seconds
                cache.set(cache_key, quote, 90)

                # Update database cache fields if stock exists
                if stock:
                    stock.last_price = Decimal(str(round(current_price, 2)))
                    stock.last_change = Decimal(str(round(change, 2)))
                    stock.last_change_pct = Decimal(str(round(change_pct, 2)))
                    stock.day_high = Decimal(str(round(day_high, 2)))
                    stock.day_low = Decimal(str(round(day_low, 2)))
                    stock.volume = volume
                    stock.last_updated = timezone.now()
                    stock.save(update_fields=['last_price', 'last_change', 'last_change_pct', 'day_high', 'day_low', 'volume', 'last_updated'])

                return quote

        except Exception as e:
            # Check if stock has saved price in DB to fall back to
            if stock and stock.last_price:
                return {
                    'symbol': symbol,
                    'name': stock.name,
                    'exchange': stock.exchange,
                    'sector': stock.sector,
                    'country': stock.country,
                    'currency': stock.currency,
                    'currency_symbol': '₹' if stock.currency == 'INR' else '$',
                    'current_price': float(stock.last_price),
                    'change': float(stock.last_change or 0.0),
                    'change_pct': float(stock.last_change_pct or 0.0),
                    'day_high': float(stock.day_high or stock.last_price),
                    'day_low': float(stock.day_low or stock.last_price),
                    'open_price': float(stock.last_price),
                    'prev_close': float(stock.last_price),
                    'volume': stock.volume or 0,
                    'data_source': 'Database Cached Snapshot',
                    'timestamp': stock.last_updated.strftime('%Y-%m-%d %H:%M:%S') if stock.last_updated else timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'success': True,
                    'warning': f"Market provider unreachable: {str(e)}"
                }

        return {
            'symbol': symbol,
            'name': name,
            'exchange': exchange,
            'sector': sector,
            'country': country,
            'currency': currency,
            'currency_symbol': '₹' if currency == 'INR' else '$',
            'current_price': 0.0,
            'change': 0.0,
            'change_pct': 0.0,
            'volume': 0,
            'data_source': 'Data Unavailable',
            'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'success': False,
            'error': f"Could not retrieve quote for {symbol}."
        }

    @staticmethod
    def get_historical_ohlcv(symbol: str, period: str = '1y') -> tuple[pd.DataFrame | None, list]:
        """
        Fetch historical daily OHLCV dataframe and formatted JSON list.
        Valid periods: 1mo, 3mo, 6mo, 1y, 2y, 5y.
        """
        symbol = symbol.upper().strip()
        cache_key = f"ohlcv_{symbol}_{period}"
        cached_data = cache.get(cache_key)
        if cached_data:
            df, series = cached_data
            return df, series

        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval="1d")
            
            if df is not None and not df.empty:
                # Clean and format dataframe
                df = df.reset_index()
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
                elif 'Datetime' in df.columns:
                    df['Date'] = pd.to_datetime(df['Datetime']).dt.strftime('%Y-%m-%d')

                data_list = []
                for _, row in df.iterrows():
                    data_list.append({
                        'date': str(row['Date']),
                        'open': round(float(row['Open']), 2),
                        'high': round(float(row['High']), 2),
                        'low': round(float(row['Low']), 2),
                        'close': round(float(row['Close']), 2),
                        'volume': int(row['Volume']) if 'Volume' in row and not pd.isna(row['Volume']) else 0
                    })

                # Cache for 1 hour
                cache.set(cache_key, (df, data_list), 3600)
                return df, data_list

        except Exception as e:
            print(f"Error fetching OHLCV for {symbol} via yfinance: {e}")

        # Fallback to local database HistoricalPrice records if yfinance is throttled or offline
        try:
            stock = Stock.objects.filter(symbol=symbol).first()
            if stock:
                from apps.market.models import HistoricalPrice
                db_prices = list(HistoricalPrice.objects.filter(stock=stock).order_by('date'))
                if len(db_prices) >= 30:
                    rows = []
                    data_list = []
                    for p in db_prices:
                        d_str = p.date.strftime('%Y-%m-%d')
                        op = float(p.open_price or p.close_price)
                        hp = float(p.high_price or p.close_price)
                        lp = float(p.low_price or p.close_price)
                        cp = float(p.close_price)
                        vol = int(p.volume or 0)
                        rows.append({
                            'Date': d_str,
                            'Open': op,
                            'High': hp,
                            'Low': lp,
                            'Close': cp,
                            'Volume': vol
                        })
                        data_list.append({
                            'date': d_str,
                            'open': round(op, 2),
                            'high': round(hp, 2),
                            'low': round(lp, 2),
                            'close': round(cp, 2),
                            'volume': vol
                        })
                    df_fallback = pd.DataFrame(rows)
                    cache.set(cache_key, (df_fallback, data_list), 300)
                    return df_fallback, data_list
        except Exception as db_ex:
            print(f"Error reading local HistoricalPrice fallback for {symbol}: {db_ex}")

        return None, []

    @staticmethod
    def get_market_overview() -> dict:
        """
        Fetches live overview of key market indices: NIFTY 50, SENSEX, S&P 500, NASDAQ.
        Also computes market open/closed status.
        """
        cache_key = "market_overview_indices"
        cached = cache.get(cache_key)
        if cached:
            return cached

        indices_data = []
        now_utc = datetime.datetime.now(pytz.utc)
        now_ist = now_utc.astimezone(pytz.timezone('Asia/Kolkata'))
        now_est = now_utc.astimezone(pytz.timezone('America/New_York'))

        # Check Indian market hours (Mon-Fri 09:15 - 15:30 IST)
        is_india_open = (
            now_ist.weekday() < 5 and
            (datetime.time(9, 15) <= now_ist.time() <= datetime.time(15, 30))
        )

        # Check US market hours (Mon-Fri 09:30 - 16:00 EST)
        is_us_open = (
            now_est.weekday() < 5 and
            (datetime.time(9, 30) <= now_est.time() <= datetime.time(16, 0))
        )

        for ticker_symbol, meta in MARKET_INDICES.items():
            try:
                t = yf.Ticker(ticker_symbol)
                hist = t.history(period="5d", interval="1d")
                if hist is not None and not hist.empty:
                    current_price = float(hist['Close'].iloc[-1])
                    prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
                    change = current_price - prev_close
                    change_pct = (change / prev_close * 100) if prev_close else 0.0

                    is_open = is_india_open if meta['country'] == 'India' else is_us_open

                    indices_data.append({
                        'symbol': ticker_symbol,
                        'name': meta['name'],
                        'exchange': meta['exchange'],
                        'country': meta['country'],
                        'currency': meta['currency'],
                        'currency_symbol': '₹' if meta['currency'] == 'INR' else '$',
                        'current_price': round(current_price, 2),
                        'change': round(change, 2),
                        'change_pct': round(change_pct, 2),
                        'is_open': is_open,
                        'status_text': 'Market Open' if is_open else 'Market Closed',
                        'timestamp': timezone.now().strftime('%H:%M:%S')
                    })
                else:
                    indices_data.append({
                        'symbol': ticker_symbol,
                        'name': meta['name'],
                        'exchange': meta['exchange'],
                        'country': meta['country'],
                        'currency': meta['currency'],
                        'currency_symbol': '₹' if meta['currency'] == 'INR' else '$',
                        'current_price': 0.0,
                        'change': 0.0,
                        'change_pct': 0.0,
                        'is_open': False,
                        'status_text': 'Data Unavailable',
                        'timestamp': timezone.now().strftime('%H:%M:%S')
                    })
            except Exception as e:
                indices_data.append({
                    'symbol': ticker_symbol,
                    'name': meta['name'],
                    'exchange': meta['exchange'],
                    'country': meta['country'],
                    'currency': meta['currency'],
                    'currency_symbol': '₹' if meta['currency'] == 'INR' else '$',
                    'current_price': 0.0,
                    'change': 0.0,
                    'change_pct': 0.0,
                    'is_open': False,
                    'status_text': 'Error',
                    'timestamp': timezone.now().strftime('%H:%M:%S')
                })

        result = {
            'indices': indices_data,
            'is_india_open': is_india_open,
            'is_us_open': is_us_open,
            'updated_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Cache for 2 minutes
        cache.set(cache_key, result, 120)
        return result

    @staticmethod
    def get_market_movers() -> dict:
        """
        Retrieves top gainers, top losers, and most active stocks across the tracked universe.
        """
        cache_key = "market_movers_overview"
        cached = cache.get(cache_key)
        if cached:
            return cached

        tracked_symbols = list(DEFAULT_STOCK_UNIVERSE.keys())[:15]
        quotes = []

        for sym in tracked_symbols:
            q = MarketDataService.get_stock_quote(sym)
            if q.get('success') and q.get('current_price', 0) > 0:
                quotes.append(q)

        gainers = sorted([q for q in quotes if q['change'] > 0], key=lambda x: x['change_pct'], reverse=True)[:5]
        losers = sorted([q for q in quotes if q['change'] < 0], key=lambda x: x['change_pct'])[:5]
        active = sorted(quotes, key=lambda x: x.get('volume', 0), reverse=True)[:5]

        result = {
            'gainers': gainers,
            'losers': losers,
            'active': active,
            'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        cache.set(cache_key, result, 180)
        return result
