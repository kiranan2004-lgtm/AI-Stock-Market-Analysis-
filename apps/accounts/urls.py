from django.urls import path
from . import views

urlpatterns = [
    # Top-level routes
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # Standard accounts/ prefixed aliases
    path('accounts/login/', views.login_view, name='accounts_login'),
    path('accounts/signup/', views.signup_view, name='accounts_signup'),
    path('accounts/logout/', views.logout_view, name='accounts_logout'),
    path('accounts/profile/', views.profile_view, name='accounts_profile'),
    
    # API endpoints
    path('api/auth/login', views.api_login, name='api_auth_login'),
    path('api/auth/signup', views.api_signup, name='api_auth_signup'),
    path('api/auth/logout', views.api_logout, name='api_auth_logout'),
    path('api/auth/me', views.api_me, name='api_auth_me'),
]
