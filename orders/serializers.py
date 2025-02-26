from rest_framework import serializers
from .models import Order, OrderItem
from carts.models import Cart, CartItem
from users.models import Address
from users.serializers import AddressSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price",  "created_at", "updated_at"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.none(), required=False)
    address_data = AddressSerializer(write_only=True, required=False)
    total_price = serializers.DecimalField(max_digits=15, decimal_places=2, read_only = True)
    status = serializers.CharField(max_length= 100, read_only = True)
    order_number = serializers.CharField(max_length= 6, read_only = True)
    user = serializers.PrimaryKeyRelatedField(read_only = True)

    class Meta:
        model = Order
        fields = ["id", "user", "address","address_data","order_number",  "created_at", "updated_at", "total_price", "status", "items",]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context["request"]
        if request and hasattr(request, "user"):
            self.fields["address"].queryset = Address.objects.filter(user=request.user)
   

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        # get address or create one
        address_id = validated_data.pop("address", None)
        address_data = validated_data.pop("address_data", None)
        address = None

        if address_data and any(address_data.values()):
            address_serializer = AddressSerializer(data=address_data)
            address_serializer.is_valid(raise_exception=True)
            address = address_serializer.save(user=user)

        elif address_id:
            try:
                address = Address.objects.get(id=address_id.id, user=user)
            except Address.DoesNotExist:
                raise serializers.ValidationError("Address does not exist")
            
        else:
            raise serializers.ValidationError("An address is required")
        
        order = Order.objects.create(
            user=user,
            address = address,
            total_price = 0,
            order_number = validated_data.get("order_number")
        )
        total_price = 0
        order_items = []
        for cart_item in cart_items:
            order_item = OrderItem(
                order = order,
                quantity = cart_item.quantity,
                product = cart_item.product,
                price = cart_item.quantity * cart_item.product.price
            )
            total_price += order_item.price
            order_items.append(order_item)

        order_items = OrderItem.objects.bulk_create(order_items) 

        order.total_price = total_price
        order.save()

        cart.delete()

        return order     
      
    def update(self, instance, validated_data):
        request = self.context.get("request")
        user = request.user

        # Extract address information
        address_id = validated_data.pop("address", None)
        address_data = validated_data.pop("address_data", None)

        # Allow updating address with new one
        if address_data and any(address_data.values()):
            address_serializer = AddressSerializer(data=address_data)
            address_serializer.is_valid(raise_exception=True)
            address = address_serializer.save(user=user)  # Create new address

        elif address_id:
            try:
                address = Address.objects.get(id=address_id.id, user=user)
            except Address.DoesNotExist:
                raise serializers.ValidationError("Address does not exist")
        else:
            address = instance.address
        instance.address = address
        instance.save()
        return instance
