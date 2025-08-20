# 代码生成时间: 2025-08-20 14:31:24
from django.db import models
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.urls import path
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods

# Models
class Permission(models.Model):
    """
    Permission model to store user permissions.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class GroupPermission(models.Model):
    """
    Many-to-many relationship between Group and Permission.
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("group", "permission")

# Views
class PermissionListView(View):
    """
    View to display list of permissions.
    """
    @require_http_methods(["GET"])
    def get(self, request, *args, **kwargs):
        try:
            permissions = Permission.objects.all()
            return JsonResponse(list(permissions.values()), safe=False)
        except Exception as e:
            return HttpResponse("Error: " + str(e), status=500)

class PermissionDetailView(View):
    """
    View to display a single permission detail.
    """
    @require_http_methods(["GET"])
    def get(self, request, pk, *args, **kwargs):
        try:
            permission = Permission.objects.get(pk=pk)
            return JsonResponse(permission.serialize(), safe=False)
        except ObjectDoesNotExist:
            return HttpResponse("Permission not found.", status=404)
        except Exception as e:
            return HttpResponse("Error: " + str(e), status=500)

class AssignPermissionView(View):
    """
    View to assign a permission to a group.
    """
    @require_http_methods(["POST"])
    def post(self, request, *args, **kwargs):
        try:
            group_id = request.POST.get("group_id")
            permission_id = request.POST.get("permission_id")
            group = Group.objects.get(pk=group_id)
            permission = Permission.objects.get(pk=permission_id)
            GroupPermission.objects.create(group=group, permission=permission)
            return HttpResponse("Permission assigned successfully.", status=201)
        except ObjectDoesNotExist:
            return HttpResponse("Group or Permission not found.", status=404)
        except Exception as e:
            return HttpResponse("Error: " + str(e), status=500)

# URLs
urlpatterns = [
    path("permissions/", PermissionListView.as_view(), name="permission_list"),
    path("permissions/<int:pk>/", PermissionDetailView.as_view(), name="permission_detail"),
    path("assign_permission/", AssignPermissionView.as_view(), name="assign_permission"),
]
