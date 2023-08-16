from .cart import Cart

def cart(request):
    # if not hasattr(request, '_cart'):
    #     request._cart = Cart(request)
    # return {'cart': request._cart}
    return {'cart': Cart(request)}
    