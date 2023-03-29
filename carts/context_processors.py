from .models import Cart,CartItem
from .views import _get_cart_id

def counter(request):
    cart_count = 0
    if 'admin' in request.path:#if any of the user is admin don't want to show any item
        return {}
    else:#if user is not admin
        try:
            cart = Cart.objects.filter(cart_id = _get_cart_id(request))
            cart_items = CartItem.objects.all().filter()
            for cart_item in cart_items: 
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:#cart does not exist
            cart_count = 0
    return dict(cart_count = cart_count)
