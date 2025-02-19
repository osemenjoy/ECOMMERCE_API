from django.contrib import admin
from .models import Product, Category
from django.contrib.admin.decorators import register
from django.contrib.admin import ModelAdmin

@register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ["id", "name", "price", "quantity_available"]

@register(Category)
class Categoryadmin(ModelAdmin):
    list_display = ["id", "name", "description"]