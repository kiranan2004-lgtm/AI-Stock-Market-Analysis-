from rest_framework import serializers
from apps.market.serializers import StockSerializer
from .models import Portfolio, Transaction

class TransactionSerializer(serializers.ModelSerializer):
    stock_details = StockSerializer(source='stock', read_only=True)
    gross_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    net_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'portfolio', 'stock', 'stock_details', 'transaction_type',
            'quantity', 'price', 'charges', 'date', 'notes',
            'gross_amount', 'net_amount', 'created_at'
        ]
        read_only_fields = ['portfolio']


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['id', 'name', 'base_currency', 'created_at']
