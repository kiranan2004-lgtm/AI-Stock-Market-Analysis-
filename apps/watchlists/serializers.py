from rest_framework import serializers
from apps.market.serializers import StockSerializer
from .models import Watchlist, WatchlistItem, PriceAlert

class WatchlistItemSerializer(serializers.ModelSerializer):
    stock_details = StockSerializer(source='stock', read_only=True)

    class Meta:
        model = WatchlistItem
        fields = ['id', 'watchlist', 'stock', 'stock_details', 'notes', 'added_at']


class WatchlistSerializer(serializers.ModelSerializer):
    items = WatchlistItemSerializer(many=True, read_only=True)
    items_count = serializers.IntegerField(source='items.count', read_only=True)

    class Meta:
        model = Watchlist
        fields = ['id', 'name', 'description', 'is_default', 'created_at', 'items', 'items_count']
        read_only_fields = ['owner']


class PriceAlertSerializer(serializers.ModelSerializer):
    stock_details = StockSerializer(source='stock', read_only=True)

    class Meta:
        model = PriceAlert
        fields = [
            'id', 'stock', 'stock_details', 'target_price', 'condition',
            'status', 'created_at', 'triggered_at', 'trigger_price'
        ]
        read_only_fields = ['owner', 'status', 'triggered_at', 'trigger_price']
