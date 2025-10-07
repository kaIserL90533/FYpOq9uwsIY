# 代码生成时间: 2025-10-08 02:16:22
includes models, views, and URLs, as well as proper docstrings and comments for clarity.
# 优化算法效率
Error handling is also included to manage any potential issues.
*/

from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class Item(models.Model):
    """ Model representing a sortable item. """
    name = models.CharField(max_length=255)
    sort_order = models.IntegerField(default=0, blank=True, null=True)
# NOTE: 重要实现细节

    def __str__(self):
# 改进用户体验
        return self.name

class DragAndDropView(View):
    """
    A view handling the drag-and-drop sorting functionality.
    It provides endpoints to retrieve, update, and reorder items.
    """
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request, *args, **kwargs):
        """
        Endpoint to handle the drag-and-drop reordering.
# 优化算法效率
        It expects a JSON payload with the new order of items.
        """
        try:
            data = request.POST.dict()
            items = Item.objects.all()
            # Update sort_order based on the received data
            for index, item_id in enumerate(data.get('item_ids', [])):
                item = items.get(id=item_id)
                if item:
# 增强安全性
                    item.sort_order = index
                    item.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    @method_decorator(csrf_exempt, name='dispatch')
# NOTE: 重要实现细节
    def get(self, request, *args, **kwargs):
        """
        Endpoint to fetch the current list of items.
# NOTE: 重要实现细节
        """
        items = Item.objects.all().order_by('sort_order')
        return JsonResponse({'items': [{'id': item.id, 'name': item.name} for item in items]}, status=200)
# FIXME: 处理边界情况

# Define URL patterns for the drag-and-drop sorting feature
urlpatterns = [
    path('drag-and-drop/', DragAndDropView.as_view(), name='drag-and-drop'),
# 优化算法效率
]
