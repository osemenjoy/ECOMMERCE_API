from django.db import models
from cloudinary.models import  CloudinaryField
import uuid

# category model
class Category(models.Model):
    id = models.UUIDField(default= uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=250)
    slug = models.SlugField()
    description = models.TextField()

    def __str__(self):
        return self.name

# product model
class Product(models.Model):
    id = models.UUIDField(default= uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=250)
    slug = models.SlugField()
    image = CloudinaryField("image")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name