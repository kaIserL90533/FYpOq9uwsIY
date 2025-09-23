# 代码生成时间: 2025-09-23 21:43:57
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.sessions.models import Session

# Model for storing user theme preferences
class UserTheme(models.Model):
    """
    A model to store user's theme preferences.
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    theme = models.CharField(max_length=100, blank=True)

    # String representation of the model
    def __str__(self):
        return f"{self.user.username}: {self.theme}"

# View to handle theme switching
class ThemeSwitchView(View):
    """
    A view to handle theme switching based on user preference.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle POST request to update user's theme preference.
        """
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)
        
        # Get the theme from the POST data
        theme = request.POST.get('theme')
        
        # Update the user's theme preference in the database
        UserTheme.objects.update_or_create(
            user=request.user,
            defaults={'theme': theme}
        )
        
        # Return a success response
        return HttpResponse('Theme updated successfully')

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

# URL configuration for the theme switcher view
from django.urls import path

urlpatterns = [
    path('switch_theme/', ThemeSwitchView.as_view(), name='switch_theme'),
]
