# 代码生成时间: 2025-09-09 19:48:35
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Order model
class Order(models.Model):
    """
    An Order model to store order details.
    """
    customer_name = models.CharField(max_length=100)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, default='pending')

    def __str__(self):
        return f"Order {self.id} for {self.customer_name}"

# Views
@method_decorator(csrf_exempt, name='dispatch')
class OrderView(View):
    """
    A View to handle order creation and status update.
    """
    def post(self, request):
        """
        Handles order creation.
        """
        try:
            data = request.POST.dict()
            customer_name = data.get('customer_name')
            order_total = data.get('order_total')

            # Validate input
            if not customer_name or not order_total:
                return JsonResponse({'error': 'Missing customer name or order total'}, status=400)

            # Create a new order
            order = Order.objects.create(
                customer_name=customer_name,
                order_total=order_total,
            )

            # Return success response with order ID
            return JsonResponse({'id': order.id}, status=201)
        except Exception as e:
            # Handle any unexpected errors
            return JsonResponse({'error': str(e)}, status=500)

    def put(self, request, order_id):
        """
        Handles order status update.
        """
        try:
            data = request.POST.dict()
            status = data.get('status')
            order = Order.objects.get(id=order_id)

            # Validate status input
            if not status:
                return JsonResponse({'error': 'Missing status'}, status=400)

            # Update the order status
            order.status = status
            order.save()
            return JsonResponse({'status': order.status}, status=200)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Exception as e:
            # Handle any unexpected errors
            return JsonResponse({'error': str(e)}, status=500)

# URL patterns
urlpatterns = [
    path('order/', OrderView.as_view(), name='order'),
]
