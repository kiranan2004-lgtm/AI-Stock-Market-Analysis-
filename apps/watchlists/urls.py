from django.urls import path
from . import views

urlpatterns = [
    path('watchlists/', views.watchlists_view, name='watchlists'),
    path('alerts/', views.alerts_view, name='alerts'),

    # REST APIs
    path('api/watchlists/', views.api_watchlists_list, name='api_watchlists_list'),
    path('api/watchlists/toggle/<str:symbol>/', views.api_toggle_watchlist, name='api_toggle_watchlist'),
    path('api/alerts/', views.api_alerts_list, name='api_alerts_list'),
    path('api/alerts/check/', views.api_check_alerts, name='api_check_alerts'),
    path('api/alerts/<int:pk>/cancel/', views.api_cancel_alert, name='api_cancel_alert'),
]
