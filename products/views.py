from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, ProductCategory, CartItem
from .serializers import ProductCategorySerializer, ProductSerializer, CartItemSerializer


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
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticatedOrReadOnly]


class CartItemList(generics.ListAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        # Assuming you have a user object for the authenticated user
        user = self.request.user
        return CartItem.objects.filter(user=user)


class AddToCart(generics.CreateAPIView):
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        # Assuming you have a user object for the authenticated user
        serializer.save(user=self.request.user)


class RemoveFromCart(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()  # Set queryset to include all cart items
    lookup_field = 'pk'
