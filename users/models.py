from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# user model
class User(AbstractUser):
    ROLE_CHOICES = [
        ("USER", "User"),
        ("ADMIN", "Admin"),
    ]
    GENDER_CHOICES = [
        ("MALE", "Male",),
        ("FEMALE", "Female",)
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    roles = models.CharField(max_length=50, choices=ROLE_CHOICES, default= "User")    
    email = models.EmailField(unique=True, max_length=100)
    phone_number = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)

    def __str__(self):
        return self.username

# address model
class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    house_number = models.CharField(max_length=50)
    street = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.street} - {self.city}' 