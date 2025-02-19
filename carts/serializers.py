from .models import CartItem, Cart
from rest_framework import serializers


class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only = True)
    cart = serializers.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = CartItem
        fields = ["id", "quantity", "product", "cart"]


    def create(self, validated_data):
        product = validated_data.get("product")
        quantity = validated_data.get("quantity")
        request = self.context.get("request")
        user = request.user

        # get or create cart 
        cart, created = Cart.objects.get_or_create(user=user)

        # get or create cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, quantity=quantity)

        # update quantity if the cart item exists
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        return cart_item

# cart serializer    
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"

class EditCartItemSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only = True)
    cart = serializers.PrimaryKeyRelatedField(read_only = True)
    product = serializers.CharField(read_only= True)
    class Meta:
        model = CartItem
        fields = ["id", "quantity", "product", "cart"]