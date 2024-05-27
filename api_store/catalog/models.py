from django.db import models
from django.utils import timezone
from cart.models import Cart

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class LlistaProductes(models.Model):
    Cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    producte = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantitat = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)