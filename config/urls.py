"""
URL configuration for StockSense AI: Stock Market Intelligence & Portfolio Analytics Platform.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # App Routes
    path('', include('apps.market.urls')),
    path('', include('apps.accounts.urls')),
    path('', include('apps.portfolio.urls')),
    path('', include('apps.watchlists.urls')),
    path('', include('apps.predictions.urls')),
    path('', include('apps.analytics.urls')),
    path('', include('apps.news.urls')),
    path('', include('apps.assistant.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
