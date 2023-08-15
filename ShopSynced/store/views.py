from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import DetailView, ListView, View

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Product, Category, Order, OrderItem

from .forms import OrderForm

from django.db.models import Q

from .cart import Cart


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

        if form.is_valid:
            total_price = 0

            for item in cart:
                product = item['product']
                total_price += product.price * int(item['quantity'])
            order = form.save(commit=False)
            order.created_by = request.user
            order.paid_amount = total_price
            order.save()

            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
            
            cart.clear()
            return redirect('myaccount')
    else:
        form = OrderForm()

    return render(request, 'store/checkout.html', {'cart': cart, 'form': form,})

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