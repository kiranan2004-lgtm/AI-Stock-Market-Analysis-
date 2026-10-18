from django.db import models
from django.contrib.auth.models import User

class ChatConversation(models.Model):
    """A research session between the user and StockSense Research Assistant."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_conversations')
    title = models.CharField(max_length=255, default='Financial Research Session')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"


class ChatMessage(models.Model):
    """An individual message turn within a research conversation."""
    ROLE_CHOICES = [
        ('user', 'User Query'),
        ('assistant', 'Assistant Response'),
        ('system', 'System Context'),
    ]

    conversation = models.ForeignKey(ChatConversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
    content = models.TextField()
    context_data = models.JSONField(default=dict, blank=True, help_text="Market or portfolio data grounded into the response")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role} @ {self.created_at.strftime('%H:%M:%S')}: {self.content[:40]}..."
