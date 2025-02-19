from rest_framework import serializers
from .models import Product, Category

# serializing the category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

# serializing the product model
class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    
    class Meta:
        model = Product
        fields = "__all__"    

    # validating the price to make sure it is positive
    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError("The price must be a positive value")
        
        return price