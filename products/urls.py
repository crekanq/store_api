from django.urls import path

from .views import (ProductListView,
                    ProductCategoryListView,
                    ProductDetailView,
                    RemoveFromCart,
                    AddToCart,
                    CartItemList,
                    CreatePaymentIntent,
                    )

urlpatterns = [
    path('category/', ProductCategoryListView.as_view(), name='category'),
    path('products/', ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', CartItemList.as_view(), name='get_cart'),
    path('cart/add/', AddToCart.as_view(), name='add_to_cart'),
    path('cart/remove/<int:pk>/', RemoveFromCart.as_view(), name='remove_from_cart'),
    path('create-payment-intent/', CreatePaymentIntent.as_view(), name='create-payment-intent'),
]
