from django.urls import path
from . import views

urlpatterns = [
    path('predictions/', views.predictions_view, name='predictions'),

    # REST APIs
    path('api/predictions/train/', views.api_train, name='api_predictions_train'),
    path('api/predictions/train', views.api_train, name='api_predictions_train_noslash'),
    path('api/predictions/compare/<str:symbol>/', views.api_compare_models, name='api_predictions_compare'),
    path('api/predictions/compare/<str:symbol>', views.api_compare_models, name='api_predictions_compare_noslash'),
    path('api/predictions/<str:symbol>/', views.api_predict, name='api_predictions_symbol'),
    path('api/predictions/<str:symbol>', views.api_predict, name='api_predictions_symbol_noslash'),
]
