from django.utils.text import slugify
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import DetailView
from store.models import Product, OrderItem, Order
from store.forms import ProductForm
from django.contrib import messages
from .forms import UserRegisterForm     # UserUpdateForm, ProfileUpdateForm

# from django.contrib.auth.forms import UserCreationForm


# Create your views here.
class VendorDetailView(DetailView):
    model = User
    template_name = 'users/vendor_detail.html'
    context_object_name = 'vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = User.objects.get(pk=self.kwargs['pk'])
        products = Product.objects.filter(status=Product.ACTIVE).filter(user=vendor)
        context['vendor'] = vendor
        context['products'] = products
        return context

class RegisterView(View):
    template_name = 'users/register.html'
    form_class = UserRegisterForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to login.')
            return redirect('frontpage')

        # else:
        #     form = UserRegisterForm()            
        return render(request, self.template_name, {'form': form})

# @login_required
# def myaccount(request):     # will be changed to class
#     return render(request, 'users/myaccount.html')

@method_decorator(login_required, name='dispatch')
class MyAccountView(View):
    template_name = 'users/myaccount.html'

    def get(self, request):
        return render(request, self.template_name)

@login_required
def my_store(request):
    products = request.user.products.exclude(status=Product.DELETED)
    order_items = OrderItem.objects.filter(product__user=request.user)

    return render(request, 'users/my_store.html', {
            'products': products, 
            'order_items': order_items,
            })

# @method_decorator(login_required, name='dispatch')
# class MyStoreView(View): # UserPassesTestMixin, 
#     template_name = 'users/my_store.html'

#     # @method_decorator(login_required, name='dispatch')
#     # def dispatch(self, *args, **kwargs):
#     #     return super().dispatch(*args, **kwargs)

#     # def test_func(self):
#     #     # Check if the user is logged in and has is_vendor=True
#     #     return self.request.user.userprofile.is_vendor

#     def get(self, request):
#         products = request.user.products.exclude(status=Product.DELETED)
#         order_items = OrderItem.objects.filter(product__user=request.user)
#         messages_list = messages.get_messages(request)
#         return render(request, self.template_name, {
#             'products': products, 
#             'messages': messages_list,
#             'order_items': order_items,
#             })

def my_store_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    return render(request, 'users/my_store_order_detail.html', {
        'order': order
    })

# @login_required
# def add_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)

#         if form.is_valid:
#             title = request.POST.get('title')
#             product = form.save(commit=False)
#             product.user = request.user
#             product.slug = slugify(title)
#             product.save()

#             messages.success(request, 'The product was added!')

#             return redirect('my-store')
#     else:
#         form = ProductForm()

#     return render(request, 'users/add_product.html', {'form': form, 'title': 'Add product'})

class AddProductView(View):
    template_name = 'users/product_form.html'
    form_class = ProductForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'title': 'Add product'})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            title = request.POST.get('title')
            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(title)
            product.save()

            messages.success(request, 'The product was added!')

            return redirect('my-store')

        return render(request, self.template_name, {'form': form, 'title': 'Add product'})

# @login_required
# def edit_product(request, pk):
#     product = Product.objects.filter(user=request.user).get(pk=pk)

#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES, instance=product)

#         if form.is_valid:
#             form.save()

#             messages.success(request, 'The changes were saved!')

#             return redirect('my-store')

#     else:
#         form = ProductForm(instance=product)

#     return render(request, 'users/add_product.html', {'form': form, 'product': product, 'title': 'Edit product'})

@method_decorator(login_required, name='dispatch')
class EditProductView(View):
    template_name = 'users/product_form.html'
    form_class = ProductForm

    def get(self, request, pk):
        product = Product.objects.filter(user=request.user).get(pk=pk)
        form = self.form_class(instance=product)
        return render(request, self.template_name, {'form': form, 'product': product, 'title': 'Edit product'})

    def post(self, request, pk):
        product = Product.objects.filter(user=request.user).get(pk=pk)
        form = self.form_class(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            messages.success(request, 'The changes were saved!')

            return redirect('my-store')

        return render(request, self.template_name, {'form': form, 'product': product, 'title': 'Edit product'})

# @login_required
# def delete_product(request, pk):
#     product = Product.objects.filter(user=request.user).get(pk=pk)
#     product.status = product.DELETED
#     product.save()

#     messages.success(request, 'The product was deleted!')

#     return redirect('my-store')

@method_decorator(login_required, name='dispatch')
class DeleteProductView(View):
    def post(self, request, pk):
        product = Product.objects.filter(user=request.user).get(pk=pk)
        product.status = product.DELETED
        product.save()

        messages.success(request, 'The product was deleted!')

        return redirect('my-store')
