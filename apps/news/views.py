from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.market.models import Stock
from .services import NewsSentimentService
from .serializers import NewsArticleSerializer


@login_required
def news_view(request):
    """Financial news stream with NLP sentiment categorization."""
    selected_symbol = request.GET.get('symbol', '').strip().upper()
    force_refresh = request.GET.get('refresh', '').lower() in ['1', 'true', 'yes']

    selected_stock = None
    if selected_symbol and selected_symbol != 'MARKET':
        selected_stock = Stock.objects.filter(symbol=selected_symbol).first()

    news_data = NewsSentimentService.get_stock_news(
        selected_symbol if selected_symbol else None,
        force_refresh=force_refresh
    )
    stocks = Stock.objects.filter(is_active=True).order_by('symbol')

    return render(request, 'news/news.html', {
        'stocks': stocks,
        'selected_symbol': selected_symbol,
        'selected_stock': selected_stock,
        'articles': news_data.get('articles', []),
        'distribution': news_data.get('distribution', {}),
        'disclaimer': news_data.get('disclaimer', ''),
        'provider': news_data.get('provider', 'Google News Financial RSS'),
        'error_message': news_data.get('error'),
        'total_count': news_data.get('distribution', {}).get('total_articles', 0),
    })


# ---------------- REST API ENDPOINTS ----------------

@api_view(['GET'])
@permission_classes([AllowAny])
def api_news(request):
    """Retrieve financial news and sentiment distribution."""
    symbol = request.GET.get('symbol', '').strip().upper()
    force_refresh = request.GET.get('refresh', '').lower() in ['1', 'true', 'yes']

    data = NewsSentimentService.get_stock_news(
        symbol if symbol else None,
        force_refresh=force_refresh
    )
    
    serializer = NewsArticleSerializer(data.get('articles', []), many=True)
    return Response({
        'symbol': data.get('symbol', 'MARKET'),
        'provider': data.get('provider', 'Google News Financial RSS'),
        'distribution': data.get('distribution', {}),
        'disclaimer': data.get('disclaimer', ''),
        'error': data.get('error'),
        'articles': serializer.data
    })
