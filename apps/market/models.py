from django.db import models

class Stock(models.Model):
    """Stock entity representing tradable equities in India and US markets."""
    EXCHANGE_CHOICES = [
        ('NSE', 'National Stock Exchange (India)'),
        ('NASDAQ', 'NASDAQ (US)'),
        ('NYSE', 'New York Stock Exchange (US)'),
        ('INDEX', 'Market Index'),
    ]

    symbol = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    exchange = models.CharField(max_length=20, choices=EXCHANGE_CHOICES, db_index=True)
    sector = models.CharField(max_length=100, db_index=True)
    country = models.CharField(max_length=50, default='India')
    currency = models.CharField(max_length=10, default='INR')
    is_active = models.BooleanField(default=True)
    
    # Latest cached market stats
    last_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    last_change = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_change_pct = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    day_high = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    day_low = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    volume = models.BigIntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['symbol']
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'

    def __str__(self):
        return f"{self.symbol} - {self.name}"

    @property
    def currency_symbol(self):
        return '₹' if self.currency == 'INR' else '$'

    @property
    def is_indian(self):
        return self.exchange == 'NSE' or self.country == 'India' or self.symbol.endswith('.NS')


class HistoricalPrice(models.Model):
    """Daily OHLCV historical pricing data point."""
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='historical_prices')
    date = models.DateField(db_index=True)
    open_price = models.DecimalField(max_digits=12, decimal_places=2)
    high_price = models.DecimalField(max_digits=12, decimal_places=2)
    low_price = models.DecimalField(max_digits=12, decimal_places=2)
    close_price = models.DecimalField(max_digits=12, decimal_places=2)
    volume = models.BigIntegerField()
    source = models.CharField(max_length=50, default='Yahoo Finance')

    class Meta:
        unique_together = ('stock', 'date')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['stock', 'date']),
        ]

    def __str__(self):
        return f"{self.stock.symbol} ({self.date}): {self.close_price}"
