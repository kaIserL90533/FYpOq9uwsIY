# 代码生成时间: 2025-10-14 03:01:28
from django.db import models
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator

""" Models """

class DataDictionary(models.Model):
    """
    Data dictionary model to store key-value pairs.
    """
    key = models.CharField(max_length=255, unique=True, help_text="Unique key for the data dictionary.")
    value = models.TextField(help_text="Value associated with the key.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the entry was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the entry was last updated.")

    def __str__(self):
        return self.key

""" Views """

@method_decorator(login_required, name='dispatch')
class DataDictionaryView(models.ModelView):
    """
    Class-based view for managing data dictionaries.
    """
    queryset = DataDictionary.objects.all()
    template_name = 'data_dictionary/data_dictionary.html'
    fields = ['key', 'value']

    @require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to retrieve data dictionary entries.
        """
        try:
            data = self.get_queryset()
            return JsonResponse({'data': [dict(key=entry.key, value=entry.value) for entry in data]}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create a new data dictionary entry.
        """
        try:
            key = request.POST.get('key')
            value = request.POST.get('value')
            if key and value:
                DataDictionary.objects.create(key=key, value=value)
                return JsonResponse({'success': True, 'key': key, 'value': value})
            else:
                return JsonResponse({'error': 'Key and value are required.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def put(self, request, *args, **kwargs):
        """
        Handle PUT request to update an existing data dictionary entry.
        """
        try:
            key = request.PUT.get('key')
            value = request.PUT.get('value')
            if key and value:
                entry = DataDictionary.objects.get(key=key)
                entry.value = value
                entry.save()
                return JsonResponse({'success': True, 'key': key, 'value': value})
            else:
                return JsonResponse({'error': 'Key and value are required.'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Data dictionary entry not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE request to remove a data dictionary entry.
        """
        try:
            key = request.DELETE.get('key')
            if key:
                DataDictionary.objects.get(key=key).delete()
                return JsonResponse({'success': True, 'key': key})
            else:
                return JsonResponse({'error': 'Key is required.'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Data dictionary entry not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

""" URLs """
urlpatterns = [
    path('data-dictionary/', DataDictionaryView.as_view(), name='data_dictionary'),
]
{% endraw %}