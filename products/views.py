import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from store import settings

from .models import CartItem, Product, ProductCategory
from .serializers import (CartItemSerializer, CreatePaymentIntentSerializer,
                          ProductCategorySerializer, ProductDetailSerializer,
                          ProductSerializer)


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


class CreatePaymentIntent(generics.CreateAPIView):
    serializer_class = CreatePaymentIntentSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        product_metadata = ""
        for cart_item in cart_items:
            product_info = f"Product Title: {cart_item.product.title}, " \
                           f"Quantity: {cart_item.quantity}, " \
                           f"Price: {cart_item.product.price:.2f}"
            product_metadata += product_info + "\n"

        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        amount = int(total_amount * 100)
        currency = "usd"

        metadata = {
            'products': product_metadata,
            'total_sum': f"{total_amount:.2f} USD",
        }

        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                metadata=metadata,
            )
            return Response({'clientSecret': intent.client_secret})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
