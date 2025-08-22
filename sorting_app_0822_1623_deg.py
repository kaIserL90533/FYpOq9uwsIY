# 代码生成时间: 2025-08-22 16:23:18
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ValidationError
from .models import SortedList
# NOTE: 重要实现细节

# Models
# 扩展功能模块
class SortedList(models.Model):
    values = models.TextField(help_text="Comma-separated list of integers")

    def __str__(self):
# TODO: 优化性能
        return self.values

    def sort(self):
        """
        Sorts the comma-separated integers in the values field.
        """
        try:
            value_list = [int(x) for x in self.values.split(',')]
            sorted_list = sorted(value_list)
            self.values = ','.join(str(x) for x in sorted_list)
# 优化算法效率
            self.save()
# 扩展功能模块
            return sorted_list
# 改进用户体验
        except ValueError:
            raise ValidationError("Please ensure all values are integers")

# Views
class SortView(View):
    def post(self, request, *args, **kwargs):
# 扩展功能模块
        """
        Handles POST requests to sort a list of numbers.
        """
        data = request.POST.get('values')
        if not data:
            return JsonResponse({'error': 'No data provided'}, status=400)
        
        try:
            sorted_list = [int(x) for x in data.split(',')]
            sorted_list = sorted(sorted_list)
            return JsonResponse({'sorted_list': sorted_list}, status=200)
# 优化算法效率
        except ValueError:
            return JsonResponse({'error': 'Invalid input. Please ensure all values are integers'}, status=400)
# 改进用户体验

# URLs
from django.urls import path

urlpatterns = [
    path('sort/', SortView.as_view(), name='sort'),
]
