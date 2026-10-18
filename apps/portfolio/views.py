from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Portfolio, Transaction
from .services import PortfolioAnalyticsService
from .forms import TransactionForm
from .serializers import TransactionSerializer

@login_required
def portfolio_dashboard_view(request):
    """Visual portfolio overview, holdings analysis, and asset allocations."""
    portfolio = PortfolioAnalyticsService.get_or_create_default_portfolio(request.user)
    analytics = PortfolioAnalyticsService.calculate_portfolio(portfolio)

    return render(request, 'portfolio/portfolio.html', {
        'portfolio': portfolio,
        'analytics': analytics,
    })


@login_required
def transactions_list_view(request):
    """Transaction ledger and order management view."""
    portfolio = PortfolioAnalyticsService.get_or_create_default_portfolio(request.user)
    transactions = portfolio.transactions.select_related('stock').order_by('-date', '-created_at')
    form = TransactionForm()

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            try:
                tx = form.save(commit=False)
                tx.portfolio = portfolio
                # Validate against overselling
                PortfolioAnalyticsService.validate_transaction(
                    portfolio=portfolio,
                    stock=tx.stock,
                    tx_type=tx.transaction_type,
                    quantity=tx.quantity
                )
                tx.save()
                messages.success(request, f"Successfully recorded {tx.transaction_type} order for {tx.stock.symbol}.")
                return redirect('portfolio_transactions')
            except ValidationError as e:
                form.add_error(None, e.message if hasattr(e, 'message') else str(e))
        else:
            messages.error(request, "Please correct the errors in the transaction form.")

    return render(request, 'portfolio/transactions.html', {
        'portfolio': portfolio,
        'transactions': transactions,
        'form': form,
    })


@login_required
def transaction_delete_view(request, pk):
    """Delete a transaction and revalidate positions."""
    portfolio = PortfolioAnalyticsService.get_or_create_default_portfolio(request.user)
    tx = get_object_or_404(Transaction, id=pk, portfolio=portfolio)

    if request.method == 'POST':
        symbol = tx.stock.symbol
        tx.delete()
        messages.success(request, f"Transaction for {symbol} deleted.")
        return redirect('portfolio_transactions')

    return redirect('portfolio_transactions')


# ---------------- REST API ENDPOINTS ----------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_portfolio_summary(request):
    """Retrieve full portfolio metrics and active holdings in JSON."""
    portfolio = PortfolioAnalyticsService.get_or_create_default_portfolio(request.user)
    data = PortfolioAnalyticsService.calculate_portfolio(portfolio)

    # Format holdings for JSON serialization
    serialized_holdings = []
    for h in data['holdings']:
        serialized_holdings.append({
            'symbol': h['stock'].symbol,
            'name': h['stock'].name,
            'sector': h['stock'].sector,
            'shares': float(h['shares']),
            'avg_cost': float(h['avg_cost']),
            'current_price': float(h['current_price']),
            'current_value': float(h['current_value']),
            'invested_amount': float(h['invested_amount']),
            'unrealized_pl': float(h['unrealized_pl']),
            'unrealized_pl_pct': float(h['unrealized_pl_pct']),
            'currency': h['currency'],
            'currency_symbol': h['currency_symbol'],
        })

    response_data = {
        'is_empty': data['is_empty'],
        'portfolio_name': data['portfolio_name'],
        'base_currency': data['base_currency'],
        'currency_symbol': data['currency_symbol'],
        'total_invested': float(data['total_invested']),
        'current_value': float(data['current_value']),
        'unrealized_pl': float(data['unrealized_pl']),
        'unrealized_pl_pct': float(data['unrealized_pl_pct']),
        'realized_pl': float(data['realized_pl']),
        'holdings': serialized_holdings,
        'sector_allocation': data['sector_allocation'],
        'stock_allocation': data['stock_allocation'],
    }
    return Response(response_data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_portfolio_transactions(request):
    """List or record portfolio transactions."""
    portfolio = PortfolioAnalyticsService.get_or_create_default_portfolio(request.user)

    if request.method == 'GET':
        transactions = portfolio.transactions.select_related('stock').order_by('-date', '-created_at')
        serializer = TransactionSerializer(transactions, many=True)
        return Response({'results': serializer.data})

    elif request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Perform oversell validation
                PortfolioAnalyticsService.validate_transaction(
                    portfolio=portfolio,
                    stock=serializer.validated_data['stock'],
                    tx_type=serializer.validated_data['transaction_type'],
                    quantity=serializer.validated_data['quantity']
                )
                tx = serializer.save(portfolio=portfolio)
                return Response(TransactionSerializer(tx).data, status=201)
            except ValidationError as e:
                return Response({'error': str(e)}, status=400)
        return Response(serializer.errors, status=400)
