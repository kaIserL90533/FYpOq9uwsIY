# 代码生成时间: 2025-08-18 18:02:42
from django.http import JsonResponse, HttpResponseBadRequest
# FIXME: 处理边界情况
from django.views import View
from django.urls import path
from urllib.parse import urlparse
import requests

def is_valid_url(url):
    """
    验证URL是否有效。
    
    参数:
# TODO: 优化性能
        url (str): 需要验证的URL。
    
    返回:
# 优化算法效率
        bool: 如果URL有效返回True，否则返回False。
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
# FIXME: 处理边界情况
        return False

def check_url(request):
    """
# NOTE: 重要实现细节
    检查传入的URL是否有效。
    
    参数:
        request (HttpRequest): Django的请求对象。
    
    返回:
        JsonResponse: 返回JSON响应，包含URL验证结果。
    """
    if request.method == 'POST':
# TODO: 优化性能
        url = request.POST.get('url')
        if not url:
            return HttpResponseBadRequest('URL is required.')
        if is_valid_url(url):
            try:
                # 尝试发起HEAD请求检查URL的可达性。
                response = requests.head(url, allow_redirects=True, timeout=5)
                if response.status_code == 200:
                    return JsonResponse({'message': 'URL is valid and reachable.'})
# 改进用户体验
                else:
                    return JsonResponse({'message': 'URL is valid but not reachable.'}, status=400)
# 增强安全性
            except requests.RequestException as e:
                return JsonResponse({'message': 'URL is not reachable.'}, status=400)
        else:
            return JsonResponse({'message': 'Invalid URL.'}, status=400)
    else:
        return HttpResponseBadRequest('Method not allowed.')

def url_check_app_urls():
    """
    定义URL检查应用的URL路由。
    """
    return [
        path('check-url/', check_url, name='check-url'),
    ]
