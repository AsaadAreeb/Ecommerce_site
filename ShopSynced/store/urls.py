from django.urls import path
from .views import (
                    ProductDetailView,
                    CategoryListView,
                    SearchView,
                    AddToCartView,
                    CartView,
                    RemoveFromCartView,
                    ChangeQuantityView,
                    checkout,
                    )

from core.views import AboutPageView

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/<str:product_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('change-quantity/<str:product_id>/', ChangeQuantityView.as_view(), name='change-quantity'),
    path('cart/', CartView.as_view(), name='cart-view'),
    path('cart/checkout/', checkout, name='checkout'),
    path('<slug:slug>/', CategoryListView, name='category-list'),
    path('<slug:category_slug>/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),

]