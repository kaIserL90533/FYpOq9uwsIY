# 代码生成时间: 2025-09-16 01:17:01
from django.db import models
a
def create_shopping_cart_session(request):
    """
    This function creates or retrieves a shopping cart session for the current
    user based on their session ID. It ensures that each user has a unique
    shopping cart.
    """
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']
a
def add_to_cart(request, product_id, quantity):
    """
    Adds a product to the shopping cart. If the product is already in the cart,
    it increases the quantity.
    :param product_id: The ID of the product to add to the cart.
    :param quantity: The quantity of the product to add.
    """
    cart = create_shopping_cart_session(request)
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    request.session['cart'] = cart
    return cart
a
def remove_from_cart(request, product_id):
    """
    Removes a product from the shopping cart. If the product is not in the cart,
    it does nothing.
    :param product_id: The ID of the product to remove from the cart.
    """
    cart = create_shopping_cart_session(request)
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
a
def get_cart(request):
    """
    Retrieves the shopping cart for the current user.
    :param request: The current request object.
    :return: The shopping cart as a dictionary.
    """
    return create_shopping_cart_session(request)
a
def clear_cart(request):
    """
    Clears the shopping cart for the current user."""
    request.session['cart'] = {}
a
def cart_view(request):
    """
    The view function that handles displaying the shopping cart.
    :param request: The current request object.
    :return: A rendered template with the shopping cart data.
    """
    try:
        cart = get_cart(request)
    except Exception as e:
        # Handle the error appropriately
        cart = {}
    template_name = 'cart.html'
    context = {'cart': cart}
    return render(request, template_name, context)
a
def update_cart_view(request):
    """
    The view function that handles updating the shopping cart, such as adding or
    removing items.
    :param request: The current request object.
    :return: A redirect to the cart view.
    """
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 0))
        if product_id:
            add_to_cart(request, product_id, quantity)
        else:
            remove_from_cart(request, product_id)
    return redirect('cart')

