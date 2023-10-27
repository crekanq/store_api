from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Product(models.Model):
    image = models.ImageField(upload_to='products_images/')
    title = models.CharField(max_length=250)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'Product: {self.title} | Category: {self.category.name}'