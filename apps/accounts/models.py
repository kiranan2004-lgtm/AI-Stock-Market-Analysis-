from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """Extended user profile with platform preferences."""
    CURRENCY_CHOICES = [
        ('INR', '₹ INR (Indian Rupee)'),
        ('USD', '$ USD (US Dollar)'),
    ]
    
    THEME_CHOICES = [
        ('dark', 'Terminal Dark'),
        ('light', 'Clean Light'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    preferred_currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default='INR')
    preferred_theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='dark')
    initial_capital = models.DecimalField(max_digits=14, decimal_places=2, default=100000.00)
    bio = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Profile ({self.preferred_currency})"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
