# 代码生成时间: 2025-09-09 01:48:57
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import path
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

"""
This Django app is responsible for handling user authentication.
It includes models, views, and URLs for user login and logout functionality.
"""

# Define the models section
class UserProfile(models.Model):
    """
    A simple user profile model that extends Django's built-in User model.
    It can be extended with additional fields as needed.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # You can add additional fields here

    def __str__(self):
        return self.user.username

# Define the views section
class LoginView(View):
    """
    Handles user login functionality.
    """
    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        """
        Authenticates the user and logs them in.
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'User logged in successfully.'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid credentials.'}, status=401)

class LogoutView(View):
    """
    Handles user logout functionality.
    """
    def post(self, request):
        """
        Logs the user out.
        """
        logout(request)
        return JsonResponse({'message': 'User logged out successfully.'}, status=200)

# Define the URLs section
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
