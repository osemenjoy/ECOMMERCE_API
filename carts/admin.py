from django.contrib import admin
from .models import Cart, CartItem
from django.contrib.admin.decorators import register
from django.contrib.admin import ModelAdmin



@register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ["id", "user",]

@register(CartItem)
class CartItem(ModelAdmin):
    list_display = ["id", "product", "quantity", "cart"]