from django.db import models
import uuid
from users.models import User, Address
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled")
    ]
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, default="PENDING")
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    order_number = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.user.username

class OrderItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)


    def __str__(self):
        return self.product.name