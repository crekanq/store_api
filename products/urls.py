from django.urls import path

from .views import ProductListView, ProductCategoryListView, ProductDetailView

urlpatterns = [
    path('category/', ProductCategoryListView.as_view(), name='category'),
    path('products/', ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
