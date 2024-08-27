from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    stock = models.IntegerField(default=0)
    reserved = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()


class Order(models.Model):
    STATUS_CHOICES = [
        ('reserved', 'Reserved'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
