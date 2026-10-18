from rest_framework import serializers
from .models import NewsArticle

class NewsArticleSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(source='stock.symbol', read_only=True)

    class Meta:
        model = NewsArticle
        fields = [
            'id', 'symbol', 'headline', 'publisher', 'url',
            'published_at', 'sentiment_label', 'sentiment_score', 'summary'
        ]
