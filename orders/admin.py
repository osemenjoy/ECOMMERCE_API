from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register
from .models import Order, OrderItem

@register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ("id", "order_number", "user", "status", "total_price")

@register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price")
