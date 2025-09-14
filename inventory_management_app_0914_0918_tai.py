# 代码生成时间: 2025-09-14 09:18:32
from django.db import models
# 改进用户体验
from django.shortcuts import render
# TODO: 优化性能
from django.http import HttpResponse, Http404
from django.urls import path
# 扩展功能模块
from django.views import View

# 模型（Models）
class Product(models.Model):
    """库存产品模型"""
    name = models.CharField(max_length=255, verbose_name="产品名称")
    quantity = models.IntegerField(default=0, verbose_name="产品数量")
# 扩展功能模块
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="产品价格")
    
    def __str__(self):
        return self.name

    # 确保库存数量不能小于0
    def save(self, *args, **kwargs):
        if self.quantity < 0:
# 添加错误处理
            raise ValueError("库存数量不能小于0")
        super(Product, self).save(*args, **kwargs)

# 视图（Views）
class ProductListView(View):
    """显示所有产品列表"""
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'inventory/product_list.html', {'products': products})

class ProductDetailView(View):
    """显示单个产品详情"""
    def get(self, request, pk):
        try:
# 改进用户体验
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404("Product not found")
        return render(request, 'inventory/product_detail.html', {'product': product})
# 改进用户体验

# URL配置（Urls）
urlpatterns = [
# 扩展功能模块
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
# 扩展功能模块
]

# 模板（Templates） - 应该放在templates/inventory/目录下
# product_list.html
# {% for product in products %}
#     <p>{{ product.name }} - {{ product.quantity }} - {{ product.price }}</p>
# {% endfor %}

# product_detail.html
# <p>{{ product.name }}</p>
# <p>{{ product.quantity }}</p>
# <p>{{ product.price }}</p>