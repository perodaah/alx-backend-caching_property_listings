from django.db import models
from decimal import Decimal
from django.utils import timezone

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)  # changed from 255 to 100
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=32, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # remove default to avoid E160

    def __str__(self):
        return f"{self.name} <{self.email}>"

class Product(models.Model):
    name = models.CharField(max_length=100)  # changed from 255 to 100
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} (${self.price})"

class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name="orders", on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name="orders", blank=True)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    def __str__(self):
        return f"Order #{self.pk} for {self.customer}"
