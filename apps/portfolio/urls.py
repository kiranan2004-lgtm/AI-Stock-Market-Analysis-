from django.urls import path
from . import views

urlpatterns = [
    path('portfolio/', views.portfolio_dashboard_view, name='portfolio_dashboard'),
    path('portfolio/transactions/', views.transactions_list_view, name='portfolio_transactions'),
    path('portfolio/transactions/<int:pk>/delete/', views.transaction_delete_view, name='portfolio_transaction_delete'),

    # REST APIs
    path('api/portfolio/', views.api_portfolio_summary, name='api_portfolio_summary'),
    path('api/portfolio/transactions/', views.api_portfolio_transactions, name='api_portfolio_transactions'),
]
