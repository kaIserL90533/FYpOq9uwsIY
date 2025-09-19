# 代码生成时间: 2025-09-19 08:08:08
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.urls import path

"""
This Django app handles order processing.
"""

# models.py
class Order(models.Model):
    """Model representing an order."""
    customer_name = models.CharField(max_length=100)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Order {self.id} from {self.customer_name}"


# views.py
from .models import Order

def order_list(request):
    """View to display a list of orders."""
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})


def order_detail(request, order_id):
    """View to display a single order detail."""
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        raise Http404("Order does not exist")
    return render(request, 'orders/order_detail.html', {'order': order})


def process_order(request, order_id):
    """View to process an order."""
    try:
        order = Order.objects.get(pk=order_id)
        if order.status != 'Pending':
            return HttpResponse("Order is already processed.")
        order.status = 'Processed'
        order.save()
        return HttpResponse("Order processed successfully.")
    except Order.DoesNotExist:
        raise Http404("Order does not exist")


# urls.py
from django.urls import path
from .views import order_list, order_detail, process_order

urlpatterns = [
d
    path('', order_list, name='order_list'),
    path('<int:order_id>/', order_detail, name='order_detail'),
    path('process/<int:order_id>/', process_order, name='process_order'),
]
