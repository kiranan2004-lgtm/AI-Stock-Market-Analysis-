from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Stock, HistoricalPrice
from .services import MarketDataService, DEFAULT_STOCK_UNIVERSE
from .serializers import StockSerializer

def landing_view(request):
    """Platform institutional landing page."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Showcase preview stocks
    featured_symbols = ['RELIANCE.NS', 'TCS.NS', 'AAPL', 'NVDA', 'HDFCBANK.NS', 'MSFT']
    featured = []
    for s in featured_symbols:
        q = MarketDataService.get_stock_quote(s)
        if q.get('success'):
            featured.append(q)

    return render(request, 'landing.html', {
        'featured_stocks': featured
    })


@login_required
def dashboard_view(request):
    """
    Main Financial Intelligence Dashboard.
    Connects real market indices, user's saved portfolio, and watchlist items.
    """
    market_overview = MarketDataService.get_market_overview()
    market_movers = MarketDataService.get_market_movers()

    # User's watchlists
    user_watchlists = request.user.watchlists.prefetch_related('items__stock').all()
    default_watchlist = user_watchlists.filter(is_default=True).first() or user_watchlists.first()
    
    watchlist_quotes = []
    if default_watchlist:
        for item in default_watchlist.items.all()[:8]:
            q = MarketDataService.get_stock_quote(item.stock.symbol)
            if q.get('success'):
                watchlist_quotes.append(q)

    # Portfolio metrics (calculated by PortfolioAnalyticsService)
    from apps.portfolio.services import PortfolioAnalyticsService
    portfolio_summary = PortfolioAnalyticsService.get_user_portfolio_summary(request.user)

    return render(request, 'market/dashboard.html', {
        'indices': market_overview.get('indices', []),
        'is_india_open': market_overview.get('is_india_open', False),
        'is_us_open': market_overview.get('is_us_open', False),
        'market_movers': market_movers,
        'watchlist_quotes': watchlist_quotes,
        'default_watchlist': default_watchlist,
        'portfolio_summary': portfolio_summary,
    })


@login_required
def stock_explorer_view(request):
    """Stock explorer and search directory."""
    query = request.GET.get('q', '').strip()
    exchange = request.GET.get('exchange', '').strip()
    sector = request.GET.get('sector', '').strip()

    stocks = Stock.objects.filter(is_active=True)

    if query:
        stocks = stocks.filter(Q(symbol__icontains=query) | Q(name__icontains=query))
    if exchange:
        stocks = stocks.filter(exchange=exchange)
    if sector:
        stocks = stocks.filter(sector=sector)

    sectors = Stock.objects.values_list('sector', flat=True).distinct().order_by('sector')
    exchanges = Stock.objects.values_list('exchange', flat=True).distinct().order_by('exchange')

    # Fetch live quotes for display items
    stocks_with_quotes = []
    for s in stocks[:30]:
        q = MarketDataService.get_stock_quote(s.symbol)
        stocks_with_quotes.append({
            'stock': s,
            'quote': q
        })

    return render(request, 'market/stock_explorer.html', {
        'stocks_data': stocks_with_quotes,
        'query': query,
        'selected_exchange': exchange,
        'selected_sector': sector,
        'sectors': sectors,
        'exchanges': exchanges,
    })


@login_required
def stock_detail_view(request, symbol):
    """
    Dedicated stock workspace with interactive candlestick/line charts,
    OHLCV data, indicators, watchlist toggle, and alert configuration.
    """
    symbol = symbol.upper().strip()
    stock = Stock.objects.filter(symbol=symbol).first()
    
    # If not in DB yet, attempt to load from default universe or seed
    if not stock and symbol in DEFAULT_STOCK_UNIVERSE:
        info = DEFAULT_STOCK_UNIVERSE[symbol]
        stock = Stock.objects.create(
            symbol=symbol,
            name=info['name'],
            sector=info['sector'],
            exchange=info['exchange'],
            country=info['country'],
            currency=info['currency']
        )

    quote = MarketDataService.get_stock_quote(symbol)

    # Check if stock is in user's watchlist
    is_in_watchlist = False
    if request.user.is_authenticated and stock:
        is_in_watchlist = request.user.watchlists.filter(items__stock=stock).exists()

    # User's price alerts for this stock
    user_alerts = []
    if request.user.is_authenticated and stock:
        user_alerts = request.user.price_alerts.filter(stock=stock).order_by('-created_at')

    return render(request, 'market/stock_detail.html', {
        'symbol': symbol,
        'stock': stock,
        'quote': quote,
        'is_in_watchlist': is_in_watchlist,
        'user_alerts': user_alerts,
    })


# ---------------- REST API ENDPOINTS ----------------

@api_view(['GET'])
@permission_classes([AllowAny])
def api_market_overview(request):
    """Return live status of major benchmark market indices."""
    data = MarketDataService.get_market_overview()
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_market_movers(request):
    """Return top gainers, losers, and most active equities."""
    data = MarketDataService.get_market_movers()
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_stocks_list(request):
    """List or search equities in the universe."""
    query = request.GET.get('q', '').strip()
    stocks = Stock.objects.filter(is_active=True)
    if query:
        stocks = stocks.filter(Q(symbol__icontains=query) | Q(name__icontains=query))
    
    serializer = StockSerializer(stocks[:50], many=True)
    return Response({'count': len(serializer.data), 'results': serializer.data})


@api_view(['GET'])
@permission_classes([AllowAny])
def api_stock_quote(request, symbol):
    """Get latest detailed quote for a ticker."""
    quote = MarketDataService.get_stock_quote(symbol)
    if not quote.get('success') and quote.get('current_price', 0) == 0:
        return Response(quote, status=404)
    return Response(quote)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_stock_history(request, symbol):
    """Get historical OHLCV series for charting."""
    period = request.GET.get('period', '1y')
    if period not in ['1mo', '3mo', '6mo', '1y', '2y', '5y', 'max']:
        period = '1y'
        
    df, series = MarketDataService.get_historical_ohlcv(symbol, period=period)
    if not series:
        return Response({'error': f'No historical data available for {symbol}'}, status=404)

    return Response({
        'symbol': symbol.upper(),
        'period': period,
        'count': len(series),
        'candles': series
    })
