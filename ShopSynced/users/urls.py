from django.urls import path
from .views import (
                    VendorDetailView, 
                    AddProductView, 
                    # MyStoreView, 
                    my_store,
                    EditProductView, 
                    DeleteProductView,
                    my_store_order_detail,
                    )

urlpatterns = [
    # path('my-store/', MyStoreView.as_view(), name='my-store'),
    path('my-store/', my_store, name='my-store'),
    path('my-store/order-detail/<int:pk>/', my_store_order_detail, name='my-store-order-detail'),
    path('my-store/add-product/', AddProductView.as_view(), name='add-product'),
    path('my-store/edit-product/<int:pk>/', EditProductView.as_view(), name='edit-product'),
    path('my-store/delete-product/<int:pk>/', DeleteProductView.as_view(), name='delete-product'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor-detail'),
]