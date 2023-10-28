from rest_framework import generics, permissions

from .models import Product, ProductCategory, CartItem
from .serializers import ProductCategorySerializer, ProductSerializer, CartItemSerializer, ProductDetailSerializer


class ProductCategoryListView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CartItemList(generics.ListAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


class AddToCart(generics.CreateAPIView):
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RemoveFromCart(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    lookup_field = 'pk'
