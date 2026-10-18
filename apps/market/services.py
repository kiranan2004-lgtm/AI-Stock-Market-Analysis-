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
    'TCS.NS': {'name': 'Tata Consultancy Services', 'sector': 'Information Technology', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR', 'price': 4125.50, 'change': 32.40, 'change_pct': 0.79, 'high': 4160.00, 'low': 4095.00, 'volume': 1845200},
    'INFY.NS': {'name': 'Infosys Limited', 'sector': 'Information Technology', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR', 'price': 1895.20, 'change': -12.10, 'change_pct': -0.63, 'high': 1915.00, 'low': 1882.00, 'volume': 4521000},
    'WIPRO.NS': {'name': 'Wipro Limited', 'sector': 'Information Technology', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR', 'price': 542.75, 'change': 4.30, 'change_pct': 0.80, 'high': 548.00, 'low': 539.10, 'volume': 3120000},
    'HCLTECH.NS': {'name': 'HCL Technologies', 'sector': 'Information Technology', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR', 'price': 1780.00, 'change': 14.50, 'change_pct': 0.82, 'high': 1795.00, 'low': 1768.00, 'volume': 1420000},
    'TECHM.NS': {'name': 'Tech Mahindra', 'sector': 'Information Technology', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR', 'price': 1640.30, 'change': -8.20, 'change_pct': -0.50, 'high': 1660.00, 'low': 1632.00, 'volume': 980000},
    
    # Indian Banking & Finance (NSE)
    'HDFCBANK.NS': {'name': 'HDFC Bank Limited', 'sector': 'Banking', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR', 'price': 1682.40, 'change': 8.60, 'change_pct': 0.51, 'high': 1695.00, 'low': 1674.00, 'volume': 8920000},
    'ICICIBANK.NS': {'name': 'ICICI Bank Limited', 'sector': 'Banking', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR', 'price': 1245.80, 'change': 11.20, 'change_pct': 0.91, 'high': 1252.00, 'low': 1235.00, 'volume': 6430000},
    'SBIN.NS': {'name': 'State Bank of India', 'sector': 'Banking', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR', 'price': 815.60, 'change': -3.40, 'change_pct': -0.42, 'high': 824.00, 'low': 811.20, 'volume': 7210000},
    'KOTAKBANK.NS': {'name': 'Kotak Mahindra Bank', 'sector': 'Banking', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR', 'price': 1785.00, 'change': 5.50, 'change_pct': 0.31, 'high': 1798.00, 'low': 1776.00, 'volume': 2140000},
    'AXISBANK.NS': {'name': 'Axis Bank Limited', 'sector': 'Banking', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR', 'price': 1190.25, 'change': 7.80, 'change_pct': 0.66, 'high': 1202.00, 'low': 1182.00, 'volume': 3890000},
    
    # Indian Energy & Conglomerates (NSE)
    'RELIANCE.NS': {'name': 'Reliance Industries Limited', 'sector': 'Energy & Conglomerate', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR', 'price': 2965.80, 'change': 18.40, 'change_pct': 0.62, 'high': 2985.00, 'low': 2942.00, 'volume': 4120000},
    'ONGC.NS': {'name': 'Oil and Natural Gas Corp', 'sector': 'Oil & Gas', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR', 'price': 288.40, 'change': -2.10, 'change_pct': -0.72, 'high': 293.00, 'low': 286.50, 'volume': 8100000},
    'BPCL.NS': {'name': 'Bharat Petroleum Corp', 'sector': 'Oil & Gas', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR', 'price': 345.20, 'change': 3.10, 'change_pct': 0.91, 'high': 349.00, 'low': 341.00, 'volume': 4500000},
    'ADANIGREEN.NS': {'name': 'Adani Green Energy', 'sector': 'Renewable Energy', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR', 'price': 1780.00, 'change': 24.50, 'change_pct': 1.40, 'high': 1810.00, 'low': 1755.00, 'volume': 1250000},
    'TATAPOWER.NS': {'name': 'Tata Power Company', 'sector': 'Utilities & Power', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR', 'price': 442.80, 'change': 6.20, 'change_pct': 1.42, 'high': 448.50, 'low': 436.00, 'volume': 5600000},
    
    # US Technology (NASDAQ)
    'AAPL': {'name': 'Apple Inc.', 'sector': 'Technology', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD', 'price': 232.50, 'change': 1.85, 'change_pct': 0.80, 'high': 234.20, 'low': 230.10, 'volume': 48500000},
    'MSFT': {'name': 'Microsoft Corporation', 'sector': 'Technology', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD', 'price': 428.15, 'change': 3.40, 'change_pct': 0.80, 'high': 431.00, 'low': 425.20, 'volume': 19200000},
    'GOOGL': {'name': 'Alphabet Inc. (Google)', 'sector': 'Technology', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD', 'price': 166.40, 'change': -1.20, 'change_pct': -0.72, 'high': 168.50, 'low': 165.10, 'volume': 22400000},
    'AMZN': {'name': 'Amazon.com Inc.', 'sector': 'Consumer Discretionary', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD', 'price': 188.90, 'change': 2.30, 'change_pct': 1.23, 'high': 190.40, 'low': 186.50, 'volume': 31000000},
    'TSLA': {'name': 'Tesla Inc.', 'sector': 'Automotive & Clean Energy', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD', 'price': 218.80, 'change': -4.50, 'change_pct': -2.02, 'high': 225.00, 'low': 216.20, 'volume': 65000000},
    'META': {'name': 'Meta Platforms Inc.', 'sector': 'Communication Services', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD', 'price': 585.20, 'change': 7.80, 'change_pct': 1.35, 'high': 590.00, 'low': 578.50, 'volume': 14800000},
    'NVDA': {'name': 'NVIDIA Corporation', 'sector': 'Semiconductors', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD', 'price': 138.40, 'change': 3.90, 'change_pct': 2.90, 'high': 140.20, 'low': 134.80, 'volume': 52000000},
    'NFLX': {'name': 'Netflix Inc.', 'sector': 'Entertainment', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD', 'price': 722.50, 'change': 8.60, 'change_pct': 1.20, 'high': 728.00, 'low': 714.00, 'volume': 3400000},
    
    # US Financial (NYSE)
    'JPM': {'name': 'JPMorgan Chase & Co.', 'sector': 'Banking', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD', 'price': 222.10, 'change': 1.40, 'change_pct': 0.63, 'high': 224.00, 'low': 220.50, 'volume': 8900000},
    'BAC': {'name': 'Bank of America Corp.', 'sector': 'Banking', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD', 'price': 42.80, 'change': 0.35, 'change_pct': 0.82, 'high': 43.20, 'low': 42.40, 'volume': 28000000},
    'V': {'name': 'Visa Inc.', 'sector': 'Financial Services', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD', 'price': 282.40, 'change': 1.10, 'change_pct': 0.39, 'high': 284.50, 'low': 280.80, 'volume': 5100000},
    'MA': {'name': 'Mastercard Incorporated', 'sector': 'Financial Services', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD', 'price': 495.60, 'change': 2.40, 'change_pct': 0.49, 'high': 498.00, 'low': 492.00, 'volume': 2400000},
    
    # US Healthcare (NYSE)
    'JNJ': {'name': 'Johnson & Johnson', 'sector': 'Healthcare', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD', 'price': 162.30, 'change': -0.40, 'change_pct': -0.25, 'high': 163.50, 'low': 161.80, 'volume': 6200000},
    'PFE': {'name': 'Pfizer Inc.', 'sector': 'Pharmaceuticals', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD', 'price': 28.90, 'change': 0.15, 'change_pct': 0.52, 'high': 29.20, 'low': 28.70, 'volume': 24000000},
    'UNH': {'name': 'UnitedHealth Group', 'sector': 'Healthcare', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD', 'price': 578.40, 'change': 4.20, 'change_pct': 0.73, 'high': 582.00, 'low': 574.00, 'volume': 2900000},
    
    # Major ETFs
    'SPY': {'name': 'SPDR S&P 500 ETF Trust', 'sector': 'Broad Market ETF', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD', 'price': 584.20, 'change': 2.80, 'change_pct': 0.48, 'high': 586.00, 'low': 581.50, 'volume': 42000000},
    'QQQ': {'name': 'Invesco QQQ Trust (Nasdaq 100)', 'sector': 'Tech ETF', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD', 'price': 492.80, 'change': 4.10, 'change_pct': 0.84, 'high': 495.20, 'low': 489.00, 'volume': 33000000},
    'VTI': {'name': 'Vanguard Total Stock Market ETF', 'sector': 'Total Market ETF', 'exchange': 'NYSE', 'country': 'USA', 'currency': 'USD', 'price': 286.50, 'change': 1.40, 'change_pct': 0.49, 'high': 287.80, 'low': 284.90, 'volume': 3100000},
}

MARKET_INDICES = {
    '^NSEI': {'name': 'NIFTY 50', 'exchange': 'NSE', 'country': 'India', 'currency': 'INR', 'price': 24850.30, 'change': 125.40, 'change_pct': 0.51},
    '^BSESN': {'name': 'BSE SENSEX', 'exchange': 'BSE', 'country': 'India', 'currency': 'INR', 'price': 81220.50, 'change': 380.20, 'change_pct': 0.47},
    '^GSPC': {'name': 'S&P 500', 'exchange': 'US', 'country': 'USA', 'currency': 'USD', 'price': 5845.20, 'change': 24.10, 'change_pct': 0.41},
    '^IXIC': {'name': 'NASDAQ Composite', 'exchange': 'NASDAQ', 'country': 'USA', 'currency': 'USD', 'price': 18520.60, 'change': 110.80, 'change_pct': 0.60},
}

class MarketDataService:
    """Production service for fetching, caching, and serving financial market data."""

    @staticmethod
    def get_stock_quote(symbol: str, fast_mode: bool = False) -> dict:
        """
        Fetch the latest quote for a ticker symbol.
        Uses in-memory cache and database snapshots to ensure millisecond response times.
        """
        symbol = symbol.upper().strip()
        cache_key = f"stock_quote_{symbol}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        # Check local DB for stock metadata and cached price
        stock = Stock.objects.filter(symbol=symbol).first()
        info = DEFAULT_STOCK_UNIVERSE.get(symbol, {})
        name = stock.name if stock else info.get('name', symbol)
        exchange = stock.exchange if stock else info.get('exchange', 'NSE' if '.NS' in symbol else 'NASDAQ')
        sector = stock.sector if stock else info.get('sector', 'Equities')
        country = stock.country if stock else info.get('country', 'India' if '.NS' in symbol else 'USA')
        currency = stock.currency if stock else info.get('currency', 'INR' if '.NS' in symbol else 'USD')

        # Fast mode: immediately return saved database price or universe baseline
        if fast_mode:
            if stock and stock.last_price:
                quote = {
                    'symbol': symbol,
                    'name': name,
                    'exchange': exchange,
                    'sector': sector,
                    'country': country,
                    'currency': currency,
                    'currency_symbol': '₹' if currency == 'INR' else '$',
                    'current_price': float(stock.last_price),
                    'change': float(stock.last_change or 0.0),
                    'change_pct': float(stock.last_change_pct or 0.0),
                    'day_high': float(stock.day_high or stock.last_price),
                    'day_low': float(stock.day_low or stock.last_price),
                    'open_price': float(stock.last_price),
                    'prev_close': float(stock.last_price),
                    'volume': stock.volume or 0,
                    'data_source': 'Database Snapshot',
                    'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'success': True
                }
                cache.set(cache_key, quote, 90)
                return quote
            elif info and 'price' in info:
                quote = {
                    'symbol': symbol,
                    'name': name,
                    'exchange': exchange,
                    'sector': sector,
                    'country': country,
                    'currency': currency,
                    'currency_symbol': '₹' if currency == 'INR' else '$',
                    'current_price': float(info['price']),
                    'change': float(info.get('change', 0.0)),
                    'change_pct': float(info.get('change_pct', 0.0)),
                    'day_high': float(info.get('high', info['price'])),
                    'day_low': float(info.get('low', info['price'])),
                    'open_price': float(info['price']),
                    'prev_close': float(info['price']),
                    'volume': int(info.get('volume', 0)),
                    'data_source': 'Curated Universe Baseline',
                    'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'success': True
                }
                cache.set(cache_key, quote, 90)
                return quote

        # Live fetch with quick timeout fallback
        try:
            ticker = yf.Ticker(symbol)
            fast_info = getattr(ticker, 'fast_info', None)
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

                cache.set(cache_key, quote, 90)

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
            pass

        # Robust Fallback to Database Snapshot
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
                'success': True
            }

        # Baseline Universe Fallback
        if info and 'price' in info:
            return {
                'symbol': symbol,
                'name': name,
                'exchange': exchange,
                'sector': sector,
                'country': country,
                'currency': currency,
                'currency_symbol': '₹' if currency == 'INR' else '$',
                'current_price': float(info['price']),
                'change': float(info.get('change', 0.0)),
                'change_pct': float(info.get('change_pct', 0.0)),
                'day_high': float(info.get('high', info['price'])),
                'day_low': float(info.get('low', info['price'])),
                'open_price': float(info['price']),
                'prev_close': float(info['price']),
                'volume': int(info.get('volume', 0)),
                'data_source': 'Curated Universe Baseline',
                'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'success': True
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
            base_price = float(meta.get('price', 0.0))
            base_change = float(meta.get('change', 0.0))
            base_change_pct = float(meta.get('change_pct', 0.0))
            is_open = is_india_open if meta['country'] == 'India' else is_us_open

            # Attempt quick live fetch; immediately fallback to baseline if delayed
            current_price = base_price
            change = base_change
            change_pct = base_change_pct

            try:
                t = yf.Ticker(ticker_symbol)
                hist = t.history(period="3d", interval="1d")
                if hist is not None and not hist.empty:
                    current_price = float(hist['Close'].iloc[-1])
                    prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
                    change = current_price - prev_close
                    change_pct = (change / prev_close * 100) if prev_close else 0.0
            except Exception:
                pass

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

        result = {
            'indices': indices_data,
            'is_india_open': is_india_open,
            'is_us_open': is_us_open,
            'updated_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Cache for 5 minutes
        cache.set(cache_key, result, 300)
        return result

    @staticmethod
    def get_market_movers() -> dict:
        """
        Retrieves top gainers, top losers, and most active stocks across the tracked universe.
        Queries database snapshots and cached universe to achieve millisecond response time.
        """
        cache_key = "market_movers_overview"
        cached = cache.get(cache_key)
        if cached:
            return cached

        quotes = []
        # 1. First inspect database stocks
        db_stocks = list(Stock.objects.filter(is_active=True).exclude(last_price__isnull=True))
        if db_stocks:
            for s in db_stocks:
                quotes.append({
                    'symbol': s.symbol,
                    'name': s.name,
                    'exchange': s.exchange,
                    'sector': s.sector,
                    'country': s.country,
                    'currency': s.currency,
                    'currency_symbol': s.currency_symbol,
                    'current_price': float(s.last_price),
                    'change': float(s.last_change or 0.0),
                    'change_pct': float(s.last_change_pct or 0.0),
                    'volume': s.volume or 0,
                    'success': True
                })
        else:
            # 2. Fall back to curated universe baseline
            for sym, info in DEFAULT_STOCK_UNIVERSE.items():
                quotes.append({
                    'symbol': sym,
                    'name': info['name'],
                    'exchange': info['exchange'],
                    'sector': info['sector'],
                    'country': info['country'],
                    'currency': info['currency'],
                    'currency_symbol': '₹' if info['currency'] == 'INR' else '$',
                    'current_price': float(info.get('price', 100.0)),
                    'change': float(info.get('change', 0.0)),
                    'change_pct': float(info.get('change_pct', 0.0)),
                    'volume': int(info.get('volume', 1000000)),
                    'success': True
                })

        gainers = sorted([q for q in quotes if q['change'] > 0], key=lambda x: x['change_pct'], reverse=True)[:5]
        losers = sorted([q for q in quotes if q['change'] < 0], key=lambda x: x['change_pct'])[:5]
        active = sorted(quotes, key=lambda x: x.get('volume', 0), reverse=True)[:5]

        result = {
            'gainers': gainers,
            'losers': losers,
            'active': active,
            'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        cache.set(cache_key, result, 300)
        return result
