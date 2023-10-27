from rest_framework import generics, permissions

from .models import Product, ProductCategory
from .serializers import ProductCategorySerializer, ProductSerializers


class ProductCategoryListView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
