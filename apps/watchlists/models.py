from django.db import models
from django.contrib.auth.models import User

class Watchlist(models.Model):
    """Named collection of tracked equities for an authenticated user."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlists')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, default='')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('owner', 'name')
        ordering = ['-is_default', 'name']

    def __str__(self):
        return f"{self.owner.username}'s {self.name}"


class WatchlistItem(models.Model):
    """An equity entry belonging to a specific user watchlist."""
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name='items')
    stock = models.ForeignKey('market.Stock', on_delete=models.CASCADE, related_name='watchlist_items')
    notes = models.CharField(max_length=255, blank=True, default='')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('watchlist', 'stock')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.watchlist.name} -> {self.stock.symbol}"


class PriceAlert(models.Model):
    """Automated price threshold alert configured by a user."""
    CONDITION_CHOICES = [
        ('ABOVE', 'Price Rises Above (>=)'),
        ('BELOW', 'Price Falls Below (<=)'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active Monitoring'),
        ('TRIGGERED', 'Triggered'),
        ('CANCELLED', 'Cancelled'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='price_alerts')
    stock = models.ForeignKey('market.Stock', on_delete=models.CASCADE, related_name='price_alerts')
    target_price = models.DecimalField(max_digits=12, decimal_places=2)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    triggered_at = models.DateTimeField(null=True, blank=True)
    trigger_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Alert: {self.stock.symbol} {self.condition} {self.target_price} ({self.status})"
