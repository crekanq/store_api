from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from .models import Product, ProductCategory, CartItem
from .serializers import ProductCategorySerializer, ProductSerializer, CartItemSerializer, ProductDetailSerializer


class ProductCategoryListView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 10000


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title']
    pagination_class = ProductResultsSetPagination
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
