from django.utils import timezone
from decimal import Decimal
from typing import List, Dict, Any
from apps.market.models import Stock
from apps.market.services import MarketDataService
from .models import Watchlist, WatchlistItem, PriceAlert

class WatchlistService:
    """Service handling watchlist operations and price alert evaluations."""

    @staticmethod
    def get_or_create_default_watchlist(user) -> Watchlist:
        """Returns the user's default watchlist, creating one if none exist."""
        watchlist = Watchlist.objects.filter(owner=user, is_default=True).first()
        if not watchlist:
            watchlist = Watchlist.objects.filter(owner=user).first()
        if not watchlist:
            watchlist = Watchlist.objects.create(
                owner=user,
                name='Default Watchlist',
                description='Core tracked equities',
                is_default=True
            )
            # Pre-populate with 3 standard large caps for instant usability
            starter_symbols = ['TCS.NS', 'RELIANCE.NS', 'AAPL']
            for sym in starter_symbols:
                stk = Stock.objects.filter(symbol=sym).first()
                if stk:
                    WatchlistItem.objects.get_or_create(watchlist=watchlist, stock=stk)

        return watchlist

    @staticmethod
    def toggle_stock_in_watchlist(user, symbol: str, watchlist_id=None) -> Dict[str, Any]:
        """Toggles addition or removal of a stock for the user."""
        symbol = symbol.upper().strip()
        stock = Stock.objects.filter(symbol=symbol).first()
        if not stock:
            return {'success': False, 'error': f'Stock {symbol} not found'}

        if watchlist_id:
            watchlist = Watchlist.objects.filter(id=watchlist_id, owner=user).first()
        else:
            watchlist = WatchlistService.get_or_create_default_watchlist(user)

        if not watchlist:
            return {'success': False, 'error': 'Watchlist not found'}

        item = WatchlistItem.objects.filter(watchlist=watchlist, stock=stock).first()
        if item:
            item.delete()
            return {'success': True, 'action': 'removed', 'is_in_watchlist': False, 'message': f'{symbol} removed from {watchlist.name}'}
        else:
            WatchlistItem.objects.create(watchlist=watchlist, stock=stock)
            return {'success': True, 'action': 'added', 'is_in_watchlist': True, 'message': f'{symbol} added to {watchlist.name}'}

    @staticmethod
    def evaluate_user_alerts(user) -> List[Dict[str, Any]]:
        """
        Evaluates active price alerts for the user against live quotes.
        Marks triggered alerts and records the execution price.
        """
        active_alerts = PriceAlert.objects.filter(owner=user, status='ACTIVE').select_related('stock')
        triggered_results = []

        for alert in active_alerts:
            quote = MarketDataService.get_stock_quote(alert.stock.symbol)
            if not quote.get('success') or quote.get('current_price', 0) <= 0:
                continue

            current_price = Decimal(str(quote['current_price']))
            is_triggered = False

            if alert.condition == 'ABOVE' and current_price >= alert.target_price:
                is_triggered = True
            elif alert.condition == 'BELOW' and current_price <= alert.target_price:
                is_triggered = True

            if is_triggered:
                alert.status = 'TRIGGERED'
                alert.triggered_at = timezone.now()
                alert.trigger_price = current_price
                alert.save(update_fields=['status', 'triggered_at', 'trigger_price'])
                
                triggered_results.append({
                    'id': alert.id,
                    'symbol': alert.stock.symbol,
                    'condition': alert.condition,
                    'target_price': float(alert.target_price),
                    'trigger_price': float(current_price),
                    'triggered_at': alert.triggered_at.strftime('%Y-%m-%d %H:%M:%S')
                })

        return triggered_results
