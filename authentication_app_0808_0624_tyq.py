# 代码生成时间: 2025-08-08 06:24:39
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from .models import UserProfile
from .forms import UserRegistrationForm

"""
Django application for handling user authentication.
Includes user registration, login, and logout functionality.
"""

class UserLoginView(View):
    """
    View for user login.
    """
    def get(self, request):
        """
        Return login form.
        """
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        """
        Authenticate user and login if credentials are valid.
        """
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return HttpResponse('Invalid login credentials', status=401)
        else:
            return render(request, 'login.html', {'form': form})

class UserLogoutView(View):
    """
    View for user logout.
    """
    def get(self, request):
        """
        Logout the user.
        """
        logout(request)
        return redirect('login')

@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    """
    View for the user profile page.
    """
    def get(self, request):
        """
        Return the user's profile page.
        """
        return render(request, 'profile.html', {'profile': UserProfile.objects.get(user=request.user)})

class UserRegistrationView(View):
    """
    View for user registration.
    """
    def get(self, request):
        """
        Return a blank registration form.
        """
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        """
        Create a new user and profile, then log them in.
        """
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set to False initially, user needs to confirm their email
            user.save()
            UserProfile.objects.create(user=user)
            # Send email confirmation link to user
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form})

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('register/', UserRegistrationView.as_view(), name='register'),
]
