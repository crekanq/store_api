from django.urls import path

from .views import ProductListView, ProductCategoryListView

urlpatterns = [
    path('category/', ProductCategoryListView.as_view(), name='category'),
    path('products/', ProductListView.as_view(), name='products'),
]
