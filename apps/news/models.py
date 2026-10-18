from django.db import models

class NewsArticle(models.Model):
    """Financial news item with NLP sentiment annotation."""
    SENTIMENT_CHOICES = [
        ('POSITIVE', 'Positive Sentiment'),
        ('NEUTRAL', 'Neutral Sentiment'),
        ('NEGATIVE', 'Negative Sentiment'),
    ]

    stock = models.ForeignKey(
        'market.Stock', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='news_articles'
    )
    headline = models.CharField(max_length=500)
    publisher = models.CharField(max_length=150, default='Financial Media')
    url = models.URLField(max_length=1000)
    published_at = models.DateTimeField()
    sentiment_label = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default='NEUTRAL')
    sentiment_score = models.FloatField(default=0.0, help_text="Compound sentiment score (-1.0 to +1.0)")
    summary = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']
        unique_together = ('url',)

    def __str__(self):
        return f"[{self.sentiment_label}] {self.headline[:60]}... ({self.publisher})"
