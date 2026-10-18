from django.db import models
from django.contrib.auth.models import User

class SavedScreener(models.Model):
    """User-saved custom stock screening criteria."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_screeners')
    name = models.CharField(max_length=100)
    filters = models.JSONField(default=dict, help_text="Configured filters like sector, min_pe, min_volume, etc.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name}"
