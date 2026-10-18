from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import UserProfile

def signup_view(request):
    """User registration page and handler."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Update user profile with selected currency
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.preferred_currency = form.cleaned_data.get('preferred_currency', 'INR')
            profile.save()

            # Automatically log in the user after successful signup
            login(request, user)
            messages.success(request, f"Welcome to StockSense AI, {user.first_name or user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """User login page and handler."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']

            # Support login with either username or email (delegated to EmailOrUsernameModelBackend)
            user = authenticate(request, username=identifier, password=password)

            if user is not None:
                login(request, user)
                next_url = request.GET.get('next') or request.POST.get('next') or 'dashboard'
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username/email or password.")
        else:
            messages.error(request, "Please enter your credentials.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """User logout view."""
    logout(request)
    messages.info(request, "You have been successfully signed out.")
    return redirect('login')


@login_required
def profile_view(request):
    """User profile and platform settings."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Update User model fields
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()

            form.save()
            messages.success(request, "Profile preferences updated successfully.")
            return redirect('profile')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = UserProfileForm(instance=profile, initial=initial)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile
    })


# ---------------- REST API ENDPOINTS ----------------

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """API endpoint for JSON authentication."""
    data = request.data
    identifier = (data.get('username') or data.get('email') or '').strip()
    password = data.get('password')

    if not identifier or not password:
        return Response({'success': False, 'error': 'Username and password are required.'}, status=400)

    # Support login with either username or email (delegated to EmailOrUsernameModelBackend)
    user = authenticate(request, username=identifier, password=password)

    if user is not None:
        login(request, user)
        return Response({
            'success': True,
            'message': 'Login successful',
            'user': {
                'username': user.username,
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}".strip() or user.username
            }
        })
    return Response({'success': False, 'error': 'Invalid credentials.'}, status=401)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_signup(request):
    """API endpoint for JSON registration."""
    data = request.data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    name = data.get('name', '')

    if not username or not email or not password:
        return Response({'success': False, 'error': 'Username, email, and password are required.'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'success': False, 'error': 'Username is already taken.'}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({'success': False, 'error': 'Email is already registered.'}, status=400)

    if len(password) < 8:
        return Response({'success': False, 'error': 'Password must be at least 8 characters long.'}, status=400)

    first_name = name.split(' ')[0] if name else ''
    last_name = ' '.join(name.split(' ')[1:]) if ' ' in name else ''

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    login(request, user)
    return Response({
        'success': True,
        'message': 'Registration successful',
        'user': {
            'username': user.username,
            'email': user.email,
            'name': f"{user.first_name} {user.last_name}".strip() or user.username
        }
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    """API endpoint for logging out."""
    logout(request)
    return Response({'success': True, 'message': 'Logged out successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_me(request):
    """API endpoint to get current authenticated user data."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return Response({
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'currency': profile.preferred_currency,
        'theme': profile.preferred_theme,
    })
