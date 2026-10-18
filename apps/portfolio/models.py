from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class Portfolio(models.Model):
    """User investment portfolio entity."""
    CURRENCY_CHOICES = [
        ('INR', '₹ INR'),
        ('USD', '$ USD'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    name = models.CharField(max_length=100, default='Primary Portfolio')
    description = models.TextField(blank=True, default='')
    base_currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default='INR')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('owner', 'name')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner.username} - {self.name} ({self.base_currency})"


class Transaction(models.Model):
    """Buy or Sell execution ledger entry within a user portfolio."""
    TRANSACTION_TYPES = [
        ('BUY', 'Buy / Long Acquisition'),
        ('SELL', 'Sell / Liquidation'),
    ]

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='transactions')
    stock = models.ForeignKey('market.Stock', on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    charges = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} {self.stock.symbol} @ {self.price} on {self.date}"

    @property
    def gross_amount(self):
        return (self.quantity * self.price).quantize(Decimal('0.01'))

    @property
    def net_amount(self):
        if self.transaction_type == 'BUY':
            return (self.gross_amount + self.charges).quantize(Decimal('0.01'))
        else:
            return (self.gross_amount - self.charges).quantize(Decimal('0.01'))
