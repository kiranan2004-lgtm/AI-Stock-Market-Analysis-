from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from apps.market.models import Stock
from apps.market.services import DEFAULT_STOCK_UNIVERSE
from .models import PredictionRun
from .serializers import PredictionRunSerializer

@login_required
def predictions_view(request):
    """Machine learning stock forecasting and model comparison workspace."""
    requested_symbol = request.GET.get('symbol', 'TCS.NS').upper().strip()

    # Pre-seed requested stock if from known stock universe
    if requested_symbol in DEFAULT_STOCK_UNIVERSE and not Stock.objects.filter(symbol=requested_symbol).exists():
        info = DEFAULT_STOCK_UNIVERSE[requested_symbol]
        Stock.objects.create(
            symbol=requested_symbol, name=info['name'], sector=info['sector'],
            exchange=info['exchange'], country=info['country'], currency=info['currency']
        )

    stocks = Stock.objects.filter(is_active=True).order_by('symbol')
    default_stock = stocks.filter(symbol=requested_symbol).first() or stocks.filter(symbol='TCS.NS').first() or stocks.first()
    
    # Recent runs history
    recent_runs = PredictionRun.objects.select_related('stock').order_by('-trained_at')[:10]

    return render(request, 'predictions/predictions.html', {
        'stocks': stocks,
        'default_stock': default_stock,
        'selected_symbol': default_stock.symbol if default_stock else 'TCS.NS',
        'recent_runs': recent_runs,
        'model_choices': PredictionRun.MODEL_CHOICES,
    })


# ---------------- REST API ENDPOINTS ----------------

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def api_predict(request, symbol):
    """
    Get or execute prediction for a stock.
    Query parameters or POST body:
    - model: 'linear' | 'random_forest' | 'arima' | 'lstm' | 'hybrid' (default: 'hybrid')
    - horizon: integer 7 | 14 | 30 (default: 30)
    Guaranteed application/json contract.
    """
    clean_symbol = (symbol or '').upper().strip()
    if not clean_symbol:
        return Response({'success': False, 'error': 'Stock symbol is required.'}, status=400)

    if request.method == 'POST':
        model_type = request.data.get('model', request.GET.get('model', 'hybrid'))
        raw_horizon = request.data.get('horizon', request.GET.get('horizon', 30))
    else:
        model_type = request.GET.get('model', 'hybrid')
        raw_horizon = request.GET.get('horizon', 30)

    model_type = str(model_type or 'hybrid').lower().strip()
    valid_models = {'linear', 'random_forest', 'arima', 'lstm', 'hybrid'}
    if model_type not in valid_models:
        model_type = 'hybrid'

    try:
        horizon = int(raw_horizon)
        horizon = max(7, min(horizon, 90))
    except (ValueError, TypeError):
        horizon = 30

    try:
        from .services.forecasting import ForecastingService
        result = ForecastingService.train_and_forecast(clean_symbol, model_type=model_type, horizon=horizon)
        if not result.get('success'):
            return Response(result, status=400)
        return Response(result, status=200)
    except Exception as exc:
        return Response({
            'success': False,
            'error': f'Prediction execution failed: {str(exc)}',
            'symbol': clean_symbol
        }, status=500)


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def api_train(request):
    """Train requested model and return evaluation results. Always returns JSON."""
    try:
        if request.method == 'POST':
            symbol = str(request.data.get('symbol', request.GET.get('symbol', 'TCS.NS'))).upper().strip()
            model_type = str(request.data.get('model_type', request.data.get('model', 'hybrid'))).lower().strip()
            raw_horizon = request.data.get('horizon', request.GET.get('horizon', 30))
        else:
            symbol = str(request.GET.get('symbol', 'TCS.NS')).upper().strip()
            model_type = str(request.GET.get('model_type', request.GET.get('model', 'hybrid'))).lower().strip()
            raw_horizon = request.GET.get('horizon', 30)

        try:
            horizon = int(raw_horizon)
            horizon = max(7, min(horizon, 90))
        except (ValueError, TypeError):
            horizon = 30

        from .services.forecasting import ForecastingService
        result = ForecastingService.train_and_forecast(symbol, model_type=model_type, horizon=horizon)
        if not result.get('success'):
            return Response(result, status=400)
        return Response(result, status=200)
    except Exception as exc:
        return Response({'success': False, 'error': f'Training failed: {str(exc)}'}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def api_compare_models(request, symbol):
    """Run and compare all models on identical test data. Always returns JSON."""
    clean_symbol = (symbol or '').upper().strip()
    try:
        from .services.forecasting import ForecastingService
        result = ForecastingService.compare_models(clean_symbol)
        if not result.get('success'):
            return Response(result, status=400)
        return Response(result, status=200)
    except Exception as exc:
        return Response({
            'success': False,
            'error': f'Model comparison failed: {str(exc)}',
            'symbol': clean_symbol
        }, status=500)
