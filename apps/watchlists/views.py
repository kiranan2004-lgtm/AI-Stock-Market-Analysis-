from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.market.models import Stock
from apps.market.services import MarketDataService
from .models import Watchlist, WatchlistItem, PriceAlert
from .services import WatchlistService
from .serializers import WatchlistSerializer, PriceAlertSerializer

@login_required
def watchlists_view(request):
    """Manage multiple custom watchlists and saved equities."""
    watchlists = request.user.watchlists.prefetch_related('items__stock').all()
    if not watchlists.exists():
        WatchlistService.get_or_create_default_watchlist(request.user)
        watchlists = request.user.watchlists.prefetch_related('items__stock').all()

    selected_wl_id = request.GET.get('wl')
    current_watchlist = None
    if selected_wl_id:
        current_watchlist = watchlists.filter(id=selected_wl_id).first()
    if not current_watchlist:
        current_watchlist = watchlists.filter(is_default=True).first() or watchlists.first()

    # Handle creation of new named watchlist
    if request.method == 'POST' and 'create_watchlist' in request.POST:
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        if name:
            wl = Watchlist.objects.create(
                owner=request.user,
                name=name,
                description=description
            )
            messages.success(request, f"Watchlist '{name}' created.")
            return redirect(f"/watchlists/?wl={wl.id}")

    # Fetch live quotes for current watchlist items
    items_with_quotes = []
    if current_watchlist:
        for item in current_watchlist.items.all():
            q = MarketDataService.get_stock_quote(item.stock.symbol)
            items_with_quotes.append({
                'item': item,
                'quote': q
            })

    all_stocks = Stock.objects.filter(is_active=True).order_by('symbol')

    return render(request, 'watchlists/watchlists.html', {
        'watchlists': watchlists,
        'current_watchlist': current_watchlist,
        'items_with_quotes': items_with_quotes,
        'all_stocks': all_stocks,
    })


@login_required
def alerts_view(request):
    """User price alert configuration and alert monitor."""
    alerts = request.user.price_alerts.select_related('stock').order_by('-created_at')
    all_stocks = Stock.objects.filter(is_active=True).order_by('symbol')

    if request.method == 'POST' and 'create_alert' in request.POST:
        symbol = request.POST.get('symbol', '').strip().upper()
        target_price = request.POST.get('target_price', '').strip()
        condition = request.POST.get('condition', 'ABOVE')

        stock = Stock.objects.filter(symbol=symbol).first()
        if stock and target_price:
            PriceAlert.objects.create(
                owner=request.user,
                stock=stock,
                target_price=target_price,
                condition=condition,
                status='ACTIVE'
            )
            messages.success(request, f"Price alert configured for {symbol} at {target_price}.")
            return redirect('alerts')

    return render(request, 'watchlists/alerts.html', {
        'alerts': alerts,
        'all_stocks': all_stocks,
    })


# ---------------- REST API ENDPOINTS ----------------

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_watchlists_list(request):
    """List or create watchlists."""
    if request.method == 'GET':
        watchlists = request.user.watchlists.prefetch_related('items__stock').all()
        serializer = WatchlistSerializer(watchlists, many=True)
        return Response({'results': serializer.data})

    elif request.method == 'POST':
        name = request.data.get('name', '').strip()
        desc = request.data.get('description', '').strip()
        if not name:
            return Response({'error': 'Name is required'}, status=400)
        wl = Watchlist.objects.create(owner=request.user, name=name, description=desc)
        return Response(WatchlistSerializer(wl).data, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_toggle_watchlist(request, symbol):
    """Toggle adding or removing stock from watchlist."""
    watchlist_id = request.data.get('watchlist_id')
    res = WatchlistService.toggle_stock_in_watchlist(request.user, symbol, watchlist_id)
    if not res.get('success'):
        return Response(res, status=400)
    return Response(res)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_alerts_list(request):
    """List or create price alerts."""
    if request.method == 'GET':
        alerts = request.user.price_alerts.select_related('stock').order_by('-created_at')
        serializer = PriceAlertSerializer(alerts, many=True)
        return Response({'results': serializer.data})

    elif request.method == 'POST':
        serializer = PriceAlertSerializer(data=request.data)
        if serializer.is_valid():
            alert = serializer.save(owner=request.user)
            return Response(PriceAlertSerializer(alert).data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_check_alerts(request):
    """Evaluate active price alerts against live quotes."""
    triggered = WatchlistService.evaluate_user_alerts(request.user)
    return Response({
        'triggered_count': len(triggered),
        'triggered_alerts': triggered,
        'message': f"{len(triggered)} price alerts triggered." if triggered else "No price alerts triggered at this time."
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_cancel_alert(request, pk):
    """Cancel an active price alert."""
    alert = get_object_or_404(PriceAlert, id=pk, owner=request.user)
    alert.status = 'CANCELLED'
    alert.save(update_fields=['status'])
    return Response({'success': True, 'message': 'Alert cancelled.'})
