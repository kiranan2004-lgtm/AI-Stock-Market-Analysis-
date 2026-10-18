from decimal import Decimal
from typing import Dict, Any, List
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.market.models import Stock
from apps.market.services import MarketDataService
from .models import Portfolio, Transaction

# Fixed realistic benchmark exchange rate for dual-currency reporting
USD_INR_RATE = Decimal('86.50')

class PortfolioAnalyticsService:
    """
    Mathematical and accounting engine for portfolio positions,
    FIFO/average cost-basis calculations, and P&L tracking.
    """

    @staticmethod
    def get_or_create_default_portfolio(user) -> Portfolio:
        """Retrieve or initialize the primary user portfolio."""
        currency = 'INR'
        if hasattr(user, 'profile') and user.profile.preferred_currency:
            currency = user.profile.preferred_currency

        portfolio, _ = Portfolio.objects.get_or_create(
            owner=user,
            name='Primary Portfolio',
            defaults={'base_currency': currency}
        )
        return portfolio

    @staticmethod
    def validate_transaction(portfolio: Portfolio, stock: Stock, tx_type: str, quantity: Decimal, exclude_tx_id=None) -> None:
        """
        Validates that a SELL transaction does not exceed currently held shares.
        """
        if tx_type == 'SELL':
            qs = portfolio.transactions.filter(stock=stock)
            if exclude_tx_id:
                qs = qs.exclude(id=exclude_tx_id)

            total_bought = sum(t.quantity for t in qs.filter(transaction_type='BUY'))
            total_sold = sum(t.quantity for t in qs.filter(transaction_type='SELL'))
            available_shares = total_bought - total_sold

            if quantity > available_shares:
                raise ValidationError(
                    f"Cannot sell {quantity} shares of {stock.symbol}. You currently own {available_shares} shares."
                )

    @staticmethod
    def calculate_portfolio(portfolio: Portfolio) -> Dict[str, Any]:
        """
        Computes accurate positions, cost-basis, market values, and P&L.
        """
        transactions = portfolio.transactions.select_related('stock').order_by('date', 'created_at')

        if not transactions.exists():
            return {
                'is_empty': True,
                'portfolio_name': portfolio.name,
                'base_currency': portfolio.base_currency,
                'currency_symbol': '₹' if portfolio.base_currency == 'INR' else '$',
                'total_invested': Decimal('0.00'),
                'current_value': Decimal('0.00'),
                'unrealized_pl': Decimal('0.00'),
                'unrealized_pl_pct': Decimal('0.00'),
                'realized_pl': Decimal('0.00'),
                'holdings': [],
                'sector_allocation': [],
                'stock_allocation': [],
                'total_holdings_count': 0
            }

        # Track per-stock positions
        stock_positions: Dict[int, Dict[str, Any]] = {}
        total_realized_pl_inr = Decimal('0.00')

        for tx in transactions:
            s_id = tx.stock.id
            if s_id not in stock_positions:
                stock_positions[s_id] = {
                    'stock': tx.stock,
                    'shares': Decimal('0.0000'),
                    'total_cost': Decimal('0.00'),
                    'realized_pl': Decimal('0.00'),
                }

            pos = stock_positions[s_id]

            if tx.transaction_type == 'BUY':
                pos['shares'] += tx.quantity
                cost = (tx.quantity * tx.price) + tx.charges
                pos['total_cost'] += cost
            elif tx.transaction_type == 'SELL':
                if pos['shares'] > 0:
                    avg_cost_per_share = pos['total_cost'] / pos['shares']
                    cost_basis_sold = tx.quantity * avg_cost_per_share
                    proceeds = (tx.quantity * tx.price) - tx.charges
                    pnl = proceeds - cost_basis_sold
                    pos['realized_pl'] += pnl
                    pos['shares'] -= tx.quantity
                    pos['total_cost'] = max(Decimal('0.00'), pos['total_cost'] - cost_basis_sold)

        # Compute current valuation for active holdings
        holdings_list = []
        total_invested_portfolio = Decimal('0.00')
        total_current_value_portfolio = Decimal('0.00')
        total_realized_portfolio = Decimal('0.00')

        sector_totals: Dict[str, Decimal] = {}

        for s_id, pos in stock_positions.items():
            stock = pos['stock']
            shares = pos['shares']
            realized = pos['realized_pl']
            
            # Account for stock currency
            fx_to_portfolio = Decimal('1.0')
            if portfolio.base_currency == 'INR' and stock.currency == 'USD':
                fx_to_portfolio = USD_INR_RATE
            elif portfolio.base_currency == 'USD' and stock.currency == 'INR':
                fx_to_portfolio = Decimal('1.0') / USD_INR_RATE

            total_realized_portfolio += (realized * fx_to_portfolio)

            if shares <= 0:
                continue

            avg_cost = (pos['total_cost'] / shares).quantize(Decimal('0.01'))
            quote = MarketDataService.get_stock_quote(stock.symbol)
            current_price = Decimal(str(quote.get('current_price', 0.0)))
            
            # If quote unavailable, fallback to average acquisition cost
            if current_price <= 0:
                current_price = avg_cost

            current_value_native = (shares * current_price).quantize(Decimal('0.01'))
            invested_native = pos['total_cost'].quantize(Decimal('0.01'))
            unrealized_pl_native = current_value_native - invested_native
            unrealized_pl_pct = ((unrealized_pl_native / invested_native) * 100).quantize(Decimal('0.01')) if invested_native > 0 else Decimal('0.00')

            # Converted values for unified portfolio reporting
            invested_unified = (invested_native * fx_to_portfolio).quantize(Decimal('0.01'))
            current_value_unified = (current_value_native * fx_to_portfolio).quantize(Decimal('0.01'))

            total_invested_portfolio += invested_unified
            total_current_value_portfolio += current_value_unified

            # Sector aggregation
            sector_name = stock.sector or 'Other'
            sector_totals[sector_name] = sector_totals.get(sector_name, Decimal('0.00')) + current_value_unified

            holdings_list.append({
                'stock': stock,
                'shares': shares,
                'avg_cost': avg_cost,
                'current_price': current_price,
                'current_value': current_value_native,
                'invested_amount': invested_native,
                'unrealized_pl': unrealized_pl_native,
                'unrealized_pl_pct': unrealized_pl_pct,
                'realized_pl': realized,
                'currency': stock.currency,
                'currency_symbol': '₹' if stock.currency == 'INR' else '$',
                'day_change_pct': Decimal(str(quote.get('change_pct', 0.0))),
                'current_value_unified': current_value_unified,
            })

        total_unrealized_pl = total_current_value_portfolio - total_invested_portfolio
        total_unrealized_pl_pct = (
            ((total_unrealized_pl / total_invested_portfolio) * 100).quantize(Decimal('0.01'))
            if total_invested_portfolio > 0 else Decimal('0.00')
        )

        # Asset allocations
        sector_allocation = []
        for sec, val in sorted(sector_totals.items(), key=lambda x: x[1], reverse=True):
            pct = (val / total_current_value_portfolio * 100).quantize(Decimal('0.01')) if total_current_value_portfolio > 0 else Decimal('0.00')
            sector_allocation.append({
                'sector': sec,
                'value': float(val),
                'percentage': float(pct)
            })

        stock_allocation = []
        for h in sorted(holdings_list, key=lambda x: x['current_value_unified'], reverse=True):
            pct = (h['current_value_unified'] / total_current_value_portfolio * 100).quantize(Decimal('0.01')) if total_current_value_portfolio > 0 else Decimal('0.00')
            stock_allocation.append({
                'symbol': h['stock'].symbol,
                'name': h['stock'].name,
                'value': float(h['current_value_unified']),
                'percentage': float(pct)
            })

        return {
            'is_empty': len(holdings_list) == 0,
            'portfolio_name': portfolio.name,
            'base_currency': portfolio.base_currency,
            'currency_symbol': '₹' if portfolio.base_currency == 'INR' else '$',
            'total_invested': total_invested_portfolio,
            'current_value': total_current_value_portfolio,
            'unrealized_pl': total_unrealized_pl,
            'unrealized_pl_pct': total_unrealized_pl_pct,
            'realized_pl': total_realized_portfolio,
            'holdings': holdings_list,
            'sector_allocation': sector_allocation,
            'stock_allocation': stock_allocation,
            'total_holdings_count': len(holdings_list),
            'exchange_rate_applied': f"1 USD = {USD_INR_RATE} INR for cross-currency holdings" if portfolio.base_currency == 'INR' else f"1 INR = {(Decimal('1.0')/USD_INR_RATE).quantize(Decimal('0.0001'))} USD"
        }

    @staticmethod
    def get_user_portfolio_summary(user) -> Dict[str, Any]:
        """Convenience method to retrieve summary for dashboard widget."""
        portfolio = PortfolioAnalyticsService.get_or_create_default_portfolio(user)
        return PortfolioAnalyticsService.calculate_portfolio(portfolio)
