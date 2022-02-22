from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404)
from django.contrib import messages
from products.models import Product

# Create your views here.


def view_cart(request):
    """ View that renders the cart contents page """

    return render(request, 'cart/cart.html')


def add_to_cart(request, product_id):
    """ Add a specified quantity of a product to shopping cart """

    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if product_id in list(cart.keys()):
        cart[product_id] += quantity
        messages.success(
            request, f'Updated {product.name} quantity to {cart[product_id]}')
    else:
        cart[product_id] = quantity
        messages.success(request, f'You have added {product.name} to your cart')

    request.session['cart'] = cart
    print(request.session['cart'])
    return redirect(redirect_url)


def update_cart(request, product_id):
    """Adjust quantity of specified product"""

    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[product_id] = quantity
        messages.success(
            request, f'Updated {product.name} quantity to {cart[product_id]}')
    else:
        cart.pop(product_id)
        messages.success(request, f'Removed {product.name} from your cart')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, product_id):
    """Remove product from shopping cart"""

    try:
        product = get_object_or_404(Product, pk=product_id)
        cart = request.session.get('cart', {})

        cart.pop(product_id)
        messages.success(request, f'Removed {product.name} from your cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing product: {e}')
        return HttpResponse(status=500)
