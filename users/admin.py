from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register
from .models import User, Address

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("phone_number", "roles", "gender")}),
    )



@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ('id', 'city', 'state', 'street')
