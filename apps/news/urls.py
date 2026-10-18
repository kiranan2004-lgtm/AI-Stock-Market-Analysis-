from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news_view, name='news'),
    path('api/news/', views.api_news, name='api_news'),
]
