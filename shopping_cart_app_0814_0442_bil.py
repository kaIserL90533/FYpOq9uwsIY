# 代码生成时间: 2025-08-14 04:42:23
from django.db import models
from django.urls import path
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# 购物车模型
class Cart(models.Model):
# 改进用户体验
    """购物车模型

    Attributes:
# 扩展功能模块
        items (list): 购物车中的商品列表
    """
    items = models.JSONField(default=list)

# 购物车视图
class CartView(View):
    """购物车视图"""

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
# 优化算法效率
        # 允许跨站请求
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        """添加商品到购物车"""
        data = request.POST.json()
# 添加错误处理
        try:
            product_id = data['product_id']
            quantity = data['quantity']
            cart, created = Cart.objects.get_or_create()
            cart.items.append({'product_id': product_id, 'quantity': quantity})
            cart.save()
            return JsonResponse({'message': 'Product added to cart'})
        except KeyError:
            return JsonResponse({'error': 'Missing product_id or quantity'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request):
        """获取购物车中的商品"""
        try:
            cart = Cart.objects.first()
            if cart:
                return JsonResponse({'items': cart.items}, safe=False)
            else:
                return JsonResponse({'error': 'Cart not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# 购物车URL配置
# 添加错误处理
urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
]
