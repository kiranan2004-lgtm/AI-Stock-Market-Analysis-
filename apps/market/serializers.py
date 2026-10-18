from rest_framework import serializers
from .models import Stock, HistoricalPrice

class StockSerializer(serializers.ModelSerializer):
    currency_symbol = serializers.CharField(read_only=True)
    is_indian = serializers.BooleanField(read_only=True)

    class Meta:
        model = Stock
        fields = [
            'id', 'symbol', 'name', 'exchange', 'sector', 'country',
            'currency', 'currency_symbol', 'is_indian', 'is_active',
            'last_price', 'last_change', 'last_change_pct',
            'day_high', 'day_low', 'volume', 'last_updated'
        ]


class HistoricalPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPrice
        fields = ['id', 'date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'source']
