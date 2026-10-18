from django.urls import path
from . import views

urlpatterns = [
    path('assistant/', views.assistant_view, name='assistant'),
    path('api/assistant/chat/', views.api_chat, name='api_assistant_chat'),
    path('api/assistant/conversations/', views.api_conversations, name='api_assistant_conversations'),
]
