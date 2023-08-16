import json
import stripe

from django.shortcuts import render, get_object_or_404, redirect

from django.http import JsonResponse

from django.views.generic import DetailView, ListView, View

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Product, Category, Order, OrderItem
from .forms import OrderForm
from .cart import Cart

from django.db.models import Q



# Create your views here.

                                                        

class ProductDetailView(View):
    template_name = 'store/product_detail.html'     # <app>/<model>_<viewtype>.html

    def get(self, request, category_slug, slug):
        product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE)
        return render(request, self.template_name, {'product': product})


def CategoryListView(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=Product.ACTIVE)
    
    return render(request, 'store/category_list.html', {
        'category': category,
        'products': products,
    })

######################### converted to class-based ##################
# def search(request):
#     query = request.GET.get('query', '')
#     products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
#     return render(request, 'store/search.html', {'query': query, 'products': products})

@login_required
def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            total_price = 0
            items = []

            for item in cart:
                print('My item: ', item)
                product = item['product']
                total_price += product.price * int(item['quantity'])

                items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product.title,
                        },
                        'unit_amount': product.price,
                    },
                    'quantity': item['quantity']
                })
            
            print('these are all items: ', items)
            stripe.api_key = settings.STRIPE_SECRET_KEY



########################################################### Have to check Stripe API ###########################
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=items,
                mode='payment',
                success_url='http://127.0.0.1:8000/cart/success/',
                cancel_url='http://127.0.0.1:8000/cart/',
            )
            payment_intent = stripe.PaymentIntent.create(
                amount=total_price,
                currency='usd',
                payment_method_types=['card'],
            )
################################################################################################################


            # payment_intent = session.payment_intent
            print('payment intent: ', payment_intent)

            order = form.save(commit=False)
            order.created_by = request.user
            order.paid_amount = total_price
            order.is_paid = True
            order.payment_intent = payment_intent.payment_intent
            order.save()

            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
            
            cart.clear()
            return JsonResponse({'session': session, 'order': payment_intent.payment_intent})
    else:
        form = OrderForm()

    return render(request, 'store/checkout.html', {
        'cart': cart, 
        'form': form,
        'pub_key': settings.STRIPE_PUB_KEY,
        })

class SearchView(ListView):
    model = Product
    template_name = 'store/search.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Product.objects.filter(status=Product.ACTIVE).filter(Q(title__icontains=query) | Q(description__icontains=query))

# def add_to_cart(request, product_id):
#     cart = Cart(request)
#     cart.add(product_id)

#     return redirect('frontpage')

class AddToCartView(View):

    def post(self, request, product_id):
        cart = Cart(request)
        cart.add(product_id)
        product = get_object_or_404(Product, id=product_id)
        return redirect('cart-view')

class RemoveFromCartView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        cart.remove(product_id)
        return redirect('cart-view')

class ChangeQuantityView(View):

    def get(self, request, product_id):
        action = request.GET.get('action', '')

        if action:
            quantity = 1

            if action == 'decrease':
                quantity = -1

            cart = Cart(request)
            cart.add(product_id, quantity, True)
        
        return redirect('cart-view')


class CartView(View):

    def get(self, request):
        cart = Cart(request)
        return render(request, 'store/cart_view.html', {'cart': cart})