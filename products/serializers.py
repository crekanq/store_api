from rest_framework import serializers

from .models import ProductCategory, Product, CartItem


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    description = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'image', 'title', 'description', 'quantity', 'price', 'category']

    def get_description(self, obj):
        max_length = 100
        return obj.description[:max_length]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'image', 'title', 'description', 'quantity', 'price', 'category']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'user', 'quantity']


class CreatePaymentIntentSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")
        return product
