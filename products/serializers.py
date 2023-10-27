from rest_framework import serializers

from .models import ProductCategory, Product


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name']


class ProductSerializers(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'image', 'title', 'description', 'quantity', 'price', 'category']
