from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('stocks/', views.stock_explorer_view, name='stock_explorer'),
    path('stocks/<str:symbol>/', views.stock_detail_view, name='stock_detail'),

    # REST APIs
    path('api/market/overview/', views.api_market_overview, name='api_market_overview'),
    path('api/market/movers/', views.api_market_movers, name='api_market_movers'),
    path('api/stocks/', views.api_stocks_list, name='api_stocks_list'),
    path('api/stocks/<str:symbol>/', views.api_stock_quote, name='api_stock_quote'),
    path('api/stocks/<str:symbol>/history/', views.api_stock_history, name='api_stock_history'),
]
