from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404)
from django.contrib import messages
from bikes.models import Bike

# Create your views here.


def view_cart(request):
    """ View that renders the cart contents page """

    return render(request, 'cart/cart.html')


def add_to_cart(request, bike_id):
    """ Add a specified quantity of a bike to shopping cart """

    bike = get_object_or_404(Bike, pk=bike_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if bike_id in list(cart.keys()):
        cart[bike_id] += quantity
        messages.success(
            request, f'Updated {bike.name} quantity to {cart[bike_id]}')
    else:
        cart[bike_id] = quantity
        messages.success(request, f'You have added {bike.name} to your cart')

    request.session['cart'] = cart
    print(request.session['cart'])
    return redirect(redirect_url)


def update_cart(request, bike_id):
    """Adjust quantity of specified bike"""

    bike = get_object_or_404(Bike, pk=bike_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[bike_id] = quantity
        messages.success(
            request, f'Updated {bike.name} quantity to {cart[bike_id]}')
    else:
        cart.pop(bike_id)
        messages.success(request, f'Removed {bike.name} from your cart')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, bike_id):
    """Remove bike from shopping cart"""

    try:
        bike = get_object_or_404(Bike, pk=bike_id)
        cart = request.session.get('cart', {})

        cart.pop(bike_id)
        messages.success(request, f'Removed {bike.name} from your cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing bike: {e}')
        return HttpResponse(status=500)
