# 代码生成时间: 2025-08-11 08:01:32
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Models
class Product(models.Model):
    """Model for a Product in the shopping cart application."""
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Cart(models.Model):
    """Model for a Shopping Cart."""
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"{self.user.username}'s Cart"

class CartItem(models.Model):
    """Model for Cart Items, representing the many-to-many relationship."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

# Views
@method_decorator(csrf_exempt, name='dispatch')
class CartView(View):
    """View for handling shopping cart operations."""

    def add_to_cart(self, request, product_id, quantity):
        """Adds a product to the cart."""
        try:
            product = Product.objects.get(id=product_id)
            cart = Cart.objects.get_or_create(user=request.user)[0]
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity = max(cart_item.quantity + quantity, 0)
            cart_item.save()
            return JsonResponse({'success': True, 'message': 'Product added to cart.'})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found.'})
        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Cart not found.'})

    def remove_from_cart(self, request, product_id):
        """Removes a product from the cart."""
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            return JsonResponse({'success': True, 'message': 'Product removed from cart.'})
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return JsonResponse({'success': False, 'message': 'Product or cart not found.'})

    def get_cart(self, request):
        """Returns all items in the cart."""
        try:
            cart = Cart.objects.get(user=request.user)
            items = CartItem.objects.filter(cart=cart)
            cart_items = []
            for item in items:
                cart_items.append({'product_name': item.product.name, 'quantity': item.quantity})
            return JsonResponse({'success': True, 'cart_items': cart_items})
        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Cart not found.'})

# URL Configuration
urlpatterns = [
    path('add/<int:product_id>/<int:quantity>/', login_required(CartView.as_view()), name='add_to_cart'),
    path('remove/<int:product_id>/', login_required(CartView.as_view()), name='remove_from_cart'),
    path('get/', login_required(CartView.as_view()), name='get_cart'),
]
