from django.urls import path
from . import views

urlpatterns = [
    path('screener/', views.screener_view, name='screener'),
    
    # REST APIs
    path('api/stocks/<str:symbol>/indicators/', views.api_stock_indicators, name='api_stock_indicators'),
    path('api/screener/', views.api_screener, name='api_screener'),
    path('api/compare/', views.api_compare, name='api_compare'),
]
