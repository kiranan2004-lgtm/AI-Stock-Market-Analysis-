from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from apps.market.models import Stock
from apps.market.services import MarketDataService
from .services import TechnicalIndicatorService, ScreenerService

@login_required
def screener_view(request):
    """Stock Screener and Multi-Equity Comparison interface."""
    sectors = Stock.objects.values_list('sector', flat=True).distinct().order_by('sector')
    exchanges = Stock.objects.values_list('exchange', flat=True).distinct().order_by('exchange')
    default_symbols = ['TCS.NS', 'INFY.NS', 'AAPL', 'MSFT', 'RELIANCE.NS']
    
    return render(request, 'analytics/screener.html', {
        'sectors': sectors,
        'exchanges': exchanges,
        'default_symbols': default_symbols,
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def api_stock_indicators(request, symbol):
    """
    Computes all technical indicators for a given symbol and time horizon.
    """
    symbol = symbol.upper().strip()
    period = request.GET.get('period', '1y')
    df, _ = MarketDataService.get_historical_ohlcv(symbol, period=period)

    if df is None or df.empty:
        return Response({'error': f'No historical data found for {symbol}'}, status=404)

    indicators_result = TechnicalIndicatorService.calculate_indicators(df)
    return Response(indicators_result)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def api_screener(request):
    """
    Filters equities according to user criteria.
    """
    filters = request.data if request.method == 'POST' else request.GET.dict()
    results = ScreenerService.screen_universe(filters)
    return Response({'count': len(results), 'results': results})


@api_view(['GET'])
@permission_classes([AllowAny])
def api_compare(request):
    """
    Returns normalized comparative return series for up to 5 tickers.
    """
    symbols_param = request.GET.get('symbols', 'TCS.NS,INFY.NS,AAPL')
    period = request.GET.get('period', '6mo')
    symbols = [s.strip().upper() for s in symbols_param.split(',') if s.strip()]

    if not symbols:
        return Response({'error': 'No symbols specified for comparison.'}, status=400)

    comparison = ScreenerService.compare_stocks(symbols, period=period)
    return Response(comparison)
