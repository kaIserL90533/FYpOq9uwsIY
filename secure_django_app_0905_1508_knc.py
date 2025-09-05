# 代码生成时间: 2025-09-05 15:08:15
from django.db import models, IntegrityError
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from django.urls import path
from django.db.models import Q

# Models
class User(models.Model):
    """Model to represent a user."""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

# Views
class UserListView(View):
    """View to list all users."""
    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            users = User.objects.all()
            return render(request, 'users.html', {'users': users})
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        # Prevent SQL injection by using Django's ORM
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            User.objects.create(name=name, email=email)
            return redirect('user_list')
        except IntegrityError as e:
            return HttpResponse(f"IntegrityError: {e}", status=400)
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)

# URLs
urlpatterns = [
    path('users/', UserListView.as_view(), name='user_list'),
]

# Templates
# users.html
# {% extends "base.html" %}
# {% block content %}
# <h1>User List</h1>
# <ul>
#     {% for user in users %}
#         <li>{{ user.name }} - {{ user.email }}</li>
#     {% endfor %}
# </ul>
# <form method="post" action="users/">
#     <input type="text" name="name" placeholder="Name"/>
#     <input type="email" name="email" placeholder="Email"/>
#     <button type="submit">Add User</button>
# </form>
# {% endblock %}