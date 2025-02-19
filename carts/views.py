from django.shortcuts import render, get_object_or_404
from rest_framework.generics import GenericAPIView
from .serializers import CartSerializer, CartItemSerializer, EditCartItemSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import Cart, CartItem
from django.core.exceptions import PermissionDenied

# add to cart view
class AddCartView(GenericAPIView):
    serializer_class = CartItemSerializer

    def post(self, request):
        try:
            user = self.request.user
            if not user.is_authenticated:
                product = request.POST.get("product")
                quantity = request.POST.get("quantity")

                # get cart from session or create one
                cart = request.session.get("cart", {})

                # update cart
                if product in cart:
                    cart[product] = int(cart[product]) + int(quantity)
                else:
                    cart[product] = int(quantity)

                request.session["cart"] = cart # save cart to session
                request.session.modified = True

                return Response(
                    {
                        "message": "Product added to cart sucessfully",
                        "status": status.HTTP_201_CREATED,
                        "data": cart
                    }
                )

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "Item added to cart successfully",
                    "status": status.HTTP_201_CREATED,
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status= status.HTTP_400_BAD_REQUEST
            )
# list cart item view (view cart)       
class CartListView(GenericAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    def get(self, request):
        try:
            user = request.user
            # get session data for unauthenticated user
            if not user.is_authenticated:
                cart = request.session.get("cart", {})
                return Response(
                    {
                        "message": "cart item retrieved successfully",
                        "status": status.HTTP_200_OK,
                        "data": cart
                    }, status= status.HTTP_200_OK
                )
            cart = user.cart
            queryset = CartItem.objects.filter(cart=cart) 
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "message": "Cart retrieved successfully",
                    "status": status.HTTP_200_OK,
                    "data": serializer.data
                }, status= status.HTTP_200_OK
            )
        except Cart.DoesNotExist:
            return Response(
                {
                    "message": "Cart not found",
                    "status": status.HTTP_404_NOT_FOUND
                }, status= status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status= status.HTTP_400_BAD_REQUEST
            )
        
 # clear cart       
class CartClearView(GenericAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_object(self):
        user = self.request.user
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=user)
        return obj

    def delete(self, request, pk=None):
        try:
            cart = self.get_object()
            cart.delete()
            return Response(
                {
                    "message": "Cart cleared Successfully",
                    "status": status.HTTP_204_NO_CONTENT
                }, status= status.HTTP_204_NO_CONTENT
            )
        except Cart.DoesNotExist:
            return Response(
                {
                    "message": "Cart not found",
                    "status": status.HTTP_404_NOT_FOUND
                }, status= status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status= status.HTTP_400_BAD_REQUEST
            )

# clear cart for unauthenticated user
class ClearSessionCart(GenericAPIView):
    serializer_class = CartSerializer
    def delete(self, request, *args, **kwargs):
        try:

            request.session["cart"] = {}
            request.session.modified = True
            return Response(
                {
                    "message": "Cart cleared Successfully",
                    "status": status.HTTP_204_NO_CONTENT
                }, status= status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status= status.HTTP_400_BAD_REQUEST
            )

#remove cart item
class RemoveCartItemView(GenericAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    # override the get_object to ensure user owns the cart item to be deleted
    def get_object(self):
        obj = super().get_object()

        if obj.cart.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this item")
        return obj


    def delete(self, request, *args, **kwargs):
        try:
            queryset = self.get_object()
            queryset.delete()
            return Response(
                    {
                        "message": "Cart item deleted Successfully",
                        "status": status.HTTP_204_NO_CONTENT
                    }, status= status.HTTP_204_NO_CONTENT
                )        
        except CartItem.DoesNotExist:
            return Response(
                {
                    "message": "cart item not found",
                    "status": status.HTTP_404_NOT_FOUND,
                }, status= status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status= status.HTTP_400_BAD_REQUEST
            )

# remove cart item for unauthenticated user        
class RemoveSessionCartItem(GenericAPIView):
    serializer_class = CartItemSerializer
    
    def delete(self, request, product_id):
        try:

            cart = request.session.get("cart", {})
            if str(product_id) in cart:
                del cart[str(product_id)]
                request.session["cart"] = cart
                request.session.modified = True
                return Response(
                        {
                            "message": "Cart item deleted Successfully",
                            "status": status.HTTP_204_NO_CONTENT
                        }, status= status.HTTP_204_NO_CONTENT
                    ) 
            else:
                return Response(
                    {
                        "message": "Cart item not found",
                        "status": status.HTTP_404_NOT_FOUND
                    }, status=status.HTTP_404_NOT_FOUND
                )            
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status= status.HTTP_400_BAD_REQUEST
            )

# edit cart item, mainly the quantity
class EditCartItemView(GenericAPIView):
    serializer_class = EditCartItemSerializer
    queryset = CartItem.objects.all()

    def get_object(self):
        user = self.request.user
        obj = super().get_object()

        if user != obj.cart.user:
            raise PermissionDenied("You do not have permission to edit this")
        return obj

    def put(self, request, *args, **kwargs):
        try:
            cart_item = self.get_object()
            serializer = self.get_serializer(cart_item, data=request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(
                {
                    "message": "Cart item edited successfully",
                    "status": status.HTTP_200_OK,
                    "data": serializer.data
                }, status= status.HTTP_200_OK
            )
        except CartItem.DoesNotExist:
            return Response(
                {
                    "message": "Cart item not found",
                    "status": status.HTTP_404_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND
            )            
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status= status.HTTP_400_BAD_REQUEST
            )
        
# edit cart item, mainly the quantity for unauthenticated user        
class EditCartItemSesion(GenericAPIView):
    serializer_class = EditCartItemSerializer

    def put(self, request, product_id):
        try:
                
            quantity = request.data.get("quantity")
            cart = request.session.get("cart", {})
            product_id = str(product_id)
            if product_id in cart:
                cart[product_id] = int(quantity)
                request.session["cart"] = cart
                request.session.modified = True
                return Response(
                    {
                        "message": "Cart item edited successfully",
                        "status": status.HTTP_200_OK,
                        "data": cart
                    }, status= status.HTTP_200_OK
                )            
            else:
                return Response(
                    {
                        "message": "Cart item not found",
                        "status": status.HTTP_404_NOT_FOUND
                    }, status=status.HTTP_404_NOT_FOUND
                )            
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status= status.HTTP_400_BAD_REQUEST
            )
        