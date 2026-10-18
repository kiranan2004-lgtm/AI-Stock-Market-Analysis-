import numpy as np
import pandas as pd
from typing import Dict, Any, List

class TechnicalIndicatorService:
    """
    Pure Python and Pandas mathematical computation engine for technical indicators.
    Computes SMA, EMA, RSI, MACD, Bollinger Bands, ATR, returns, and volatility.
    """

    @staticmethod
    def calculate_indicators(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Takes an OHLCV DataFrame and computes all indicators with clean NaN handling
        and educational explanations.
        """
        if df is None or len(df) < 5:
            return {
                'success': False,
                'error': 'Insufficient historical price data points for technical analysis.'
            }

        df = df.copy()
        
        # Ensure proper column casing
        col_map = {col.lower(): col for col in df.columns}
        close_col = col_map.get('close', 'Close')
        high_col = col_map.get('high', 'High')
        low_col = col_map.get('low', 'Low')
        date_col = col_map.get('date', 'Date')

        close = df[close_col].astype(float)
        high = df[high_col].astype(float) if high_col in df.columns else close
        low = df[low_col].astype(float) if low_col in df.columns else close
        dates = df[date_col].astype(str).tolist() if date_col in df.columns else [str(i) for i in range(len(df))]

        total_points = len(df)
        warnings = []

        # 1. Simple Moving Averages (SMA 20, 50, 200)
        sma_20 = close.rolling(window=20).mean()
        sma_50 = close.rolling(window=50).mean() if total_points >= 50 else pd.Series([np.nan] * total_points)
        sma_200 = close.rolling(window=200).mean() if total_points >= 200 else pd.Series([np.nan] * total_points)

        if total_points < 200:
            warnings.append(f"SMA 200 requires 200 trading sessions; only {total_points} available.")
        if total_points < 50:
            warnings.append(f"SMA 50 requires 50 trading sessions; only {total_points} available.")

        # 2. Exponential Moving Averages (EMA 12, 26, 50)
        ema_12 = close.ewm(span=12, adjust=False).mean()
        ema_26 = close.ewm(span=26, adjust=False).mean()
        ema_50 = close.ewm(span=50, adjust=False).mean()

        # 3. Relative Strength Index (RSI 14) via Wilder's Exponential Smoothing
        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        
        avg_gain = gain.ewm(alpha=1/14, min_periods=14, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1/14, min_periods=14, adjust=False).mean()
        
        rs = avg_gain / avg_loss.replace(0, np.nan)
        rsi = 100 - (100 / (1 + rs))
        rsi = rsi.fillna(50.0)  # Default neutral for early periods

        # 4. Moving Average Convergence Divergence (MACD 12, 26, 9)
        macd_line = ema_12 - ema_26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        macd_histogram = macd_line - signal_line

        # 5. Bollinger Bands (20 period, 2 std dev)
        bb_middle = sma_20
        bb_std = close.rolling(window=20).std()
        bb_upper = bb_middle + (2.0 * bb_std)
        bb_lower = bb_middle - (2.0 * bb_std)
        bb_bandwidth = ((bb_upper - bb_lower) / bb_middle) * 100

        # 6. Average True Range (ATR 14)
        prev_close = close.shift(1)
        tr1 = high - low
        tr2 = (high - prev_close).abs()
        tr3 = (low - prev_close).abs()
        true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = true_range.ewm(alpha=1/14, min_periods=14, adjust=False).mean()

        # 7. Daily & Cumulative Returns
        daily_return = close.pct_change() * 100
        cum_return = (((close / close.iloc[0]) - 1) * 100)

        # 8. Historical Volatility (21-day rolling annualized standard deviation of log returns)
        log_ret = np.log(close / close.shift(1))
        rolling_vol = log_ret.rolling(window=21).std() * np.sqrt(252) * 100

        def clean_series(s: pd.Series) -> List[Any]:
            return [round(float(v), 2) if not pd.isna(v) and not np.isinf(v) else None for v in s]

        latest_idx = -1
        summary = {
            'latest_close': round(float(close.iloc[latest_idx]), 2),
            'sma_20': clean_series(sma_20)[latest_idx],
            'sma_50': clean_series(sma_50)[latest_idx],
            'sma_200': clean_series(sma_200)[latest_idx],
            'ema_12': clean_series(ema_12)[latest_idx],
            'ema_26': clean_series(ema_26)[latest_idx],
            'rsi_14': clean_series(rsi)[latest_idx],
            'macd_line': clean_series(macd_line)[latest_idx],
            'signal_line': clean_series(signal_line)[latest_idx],
            'macd_histogram': clean_series(macd_histogram)[latest_idx],
            'bb_upper': clean_series(bb_upper)[latest_idx],
            'bb_middle': clean_series(bb_middle)[latest_idx],
            'bb_lower': clean_series(bb_lower)[latest_idx],
            'atr_14': clean_series(atr)[latest_idx],
            'annualized_volatility': clean_series(rolling_vol)[latest_idx],
            'cumulative_return_pct': clean_series(cum_return)[latest_idx],
        }

        # Descriptive context for indicators
        explanations = {
            'rsi': {
                'title': 'Relative Strength Index (RSI 14)',
                'current_value': summary['rsi_14'],
                'interpretation': (
                    'Overbought (> 70) indicates potential short-term pullback pressure; '
                    'Oversold (< 30) suggests potential rebound territory. 30-70 represents normal equilibrium.'
                ),
                'disclaimer': 'RSI is a momentum oscillator and should not be used as a standalone trading signal.'
            },
            'macd': {
                'title': 'MACD (12, 26, 9)',
                'current_value': summary['macd_line'],
                'interpretation': (
                    'Measures relationship between two exponential moving averages. '
                    'Bullish when MACD line crosses above Signal line; Bearish when crossing below.'
                ),
                'disclaimer': 'Moving average crossovers lag price action and can generate false signals in ranging markets.'
            },
            'bollinger': {
                'title': 'Bollinger Bands (20, 2σ)',
                'interpretation': (
                    'Envelopes 95% of typical price distribution around the 20 SMA. '
                    'Band contraction indicates volatility compression preceding potential expansion.'
                ),
                'disclaimer': 'Prices touching upper or lower bands do not represent guaranteed reversal points.'
            },
            'atr': {
                'title': 'Average True Range (ATR 14)',
                'current_value': summary['atr_14'],
                'interpretation': 'Quantifies market volatility in absolute currency units per trading session.',
                'disclaimer': 'Measures price range magnitude regardless of market direction.'
            }
        }

        return {
            'success': True,
            'dates': dates,
            'summary': summary,
            'series': {
                'close': clean_series(close),
                'sma_20': clean_series(sma_20),
                'sma_50': clean_series(sma_50),
                'sma_200': clean_series(sma_200),
                'ema_12': clean_series(ema_12),
                'ema_26': clean_series(ema_26),
                'ema_50': clean_series(ema_50),
                'rsi_14': clean_series(rsi),
                'macd_line': clean_series(macd_line),
                'signal_line': clean_series(signal_line),
                'macd_histogram': clean_series(macd_histogram),
                'bb_upper': clean_series(bb_upper),
                'bb_middle': clean_series(bb_middle),
                'bb_lower': clean_series(bb_lower),
                'atr_14': clean_series(atr),
                'daily_return': clean_series(daily_return),
                'cumulative_return': clean_series(cum_return),
                'volatility': clean_series(rolling_vol),
            },
            'explanations': explanations,
            'warnings': warnings
        }


class ScreenerService:
    """Service for multi-equity comparison, ranking, and technical screening."""

    @staticmethod
    def screen_universe(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filters and ranks stocks based on technical and financial parameters.
        """
        from apps.market.models import Stock
        from apps.market.services import MarketDataService

        stocks = Stock.objects.filter(is_active=True)

        sector = filters.get('sector')
        if sector and sector != 'ALL':
            stocks = stocks.filter(sector=sector)

        exchange = filters.get('exchange')
        if exchange and exchange != 'ALL':
            stocks = stocks.filter(exchange=exchange)

        min_price = filters.get('min_price')
        max_price = filters.get('max_price')

        results = []
        for stock in stocks[:40]:
            quote = MarketDataService.get_stock_quote(stock.symbol)
            if not quote.get('success') or quote.get('current_price', 0) <= 0:
                continue

            price = quote['current_price']
            if min_price and price < float(min_price):
                continue
            if max_price and price > float(max_price):
                continue

            results.append({
                'symbol': stock.symbol,
                'name': stock.name,
                'exchange': stock.exchange,
                'sector': stock.sector,
                'currency': stock.currency,
                'currency_symbol': stock.currency_symbol,
                'current_price': price,
                'change_pct': quote['change_pct'],
                'day_high': quote['day_high'],
                'day_low': quote['day_low'],
                'volume': quote['volume'],
            })

        return results

    @staticmethod
    def compare_stocks(symbols: List[str], period: str = '6mo') -> Dict[str, Any]:
        """
        Generates normalized (base 100) return series for multi-stock comparative charts.
        """
        from apps.market.services import MarketDataService

        comparison_data = {}
        common_dates = None

        for sym in symbols[:5]:
            df, series = MarketDataService.get_historical_ohlcv(sym, period=period)
            if df is not None and not df.empty and len(df) > 5:
                df = df.sort_values('Date')
                base_price = float(df['Close'].iloc[0])
                if base_price > 0:
                    normalized = ((df['Close'].astype(float) / base_price) * 100).round(2).tolist()
                    dates = df['Date'].astype(str).tolist()
                    comparison_data[sym] = {
                        'symbol': sym,
                        'dates': dates,
                        'normalized': normalized,
                        'return_pct': round(((df['Close'].iloc[-1] / base_price) - 1) * 100, 2)
                    }
                    if common_dates is None or len(dates) > len(common_dates):
                        common_dates = dates

        return {
            'dates': common_dates or [],
            'stocks': comparison_data
        }
