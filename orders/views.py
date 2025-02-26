from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMessage
import random
import string
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from django.core.cache import cache

# generate order number
def generate_order_number():
    prefix = "OR"
    digits = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}{digits}"

class OrderCreateView(GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated,]
    queryset = OrderItem.objects.all()

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            order_number = generate_order_number()
            order = serializer.save(order_number=order_number)

            # constructing email body
            email_body = f"Dear {request.user.username},\n\n"
            email_body += f"Your order with order number {order_number} has been created successfully.\n\n"
            email_body += "Order Details:\n"
            for item in order.items.all():
                email_body += f"- {item.product.name}: {item.quantity} x ${item.price}\n"
            email_body += f"\nTotal Price: ${order.total_price}\n\n"
            email_body += "Thank you for shopping with us!\n"
            email_body += "Best regards,\nFlora E-commerce Team"

            order_confirm_mail = EmailMessage(
                subject=f"Order {order_number} Created Successfully",
                body= email_body,
                to= [request.user.email]
            )
            order_confirm_mail.send()
            return Response(
                {
                    "message": "Order Created Successfully",
                    "status": status.HTTP_201_CREATED,
                    "data": serializer.data
                }, status= status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status= status.HTTP_400_BAD_REQUEST
            )

class OrderListView(GenericAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination

    def get(self, request):
        try:
            queryset = self.get_queryset()
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Order.DoesNotExist:
            return Response(
                {
                    "message": "Order Not Found",
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
        
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        user = self.request.user
        if user.is_superuser or user.roles == "ADMIN":
            return queryset
        return queryset.filter(user=user)
    
class OrderDetailsView(GenericAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        if request.user != order.user:
            return Response(
                {
                    "message": "You do not have permission to view this",
                    "status": status.HTTP_403_FORBIDDEN
                }, status = status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(order)
        return Response(
            {
                "message": "Order Retrieved Succesfully",
                "status": status.HTTP_200_OK,
                "data": serializer.data
            }, status= status.HTTP_200_OK
        )

class OrderUpdateView(GenericAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            order = self.get_object()
            if request.user != order.user:
                return Response(
                    {
                        "message": "You do not have permission to view this",
                        "status": status.HTTP_403_FORBIDDEN
                    }, status = status.HTTP_403_FORBIDDEN
                )
            serializer = self.get_serializer(order, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "Order Updated Succesfully",
                    "status": status.HTTP_200_OK,
                    "data": serializer.data
                }, status= status.HTTP_200_OK
            )
        except Order.DoesNotExist:
            return Response(
                {
                    "message": "Order Not Found",
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
    
class OrderCancelView(GenericAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        try:
            order = self.get_object()
            if request.user != order.user:
                return Response(
                    {
                        "message": "You do not have permission to view this",
                        "status": status.HTTP_403_FORBIDDEN
                    }, status = status.HTTP_403_FORBIDDEN
                )
            if order.status != "PENDING":
                return Response (
                    {
                        "message": "You do not have permission to do this",
                        "status": status.HTTP_403_FORBIDDEN
                    }, status= status.HTTP_403_FORBIDDEN
                )            
            order.status = "CANCELLED"
            order.save()
            return Response(
                {
                    "message": "Order Cancelled Succesfully",
                    "status": status.HTTP_200_OK,
                }, status= status.HTTP_200_OK
            )    
        except Order.DoesNotExist:
            return Response(
                {
                    "message": "Order Not Found",
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
        
class OrderSearchView(GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all().order_by("-created_at")

    def get(self, request):
        try:
            user = request.user
            order_number = request.query_params.get('order_number', None)
            created_date = request.query_params.get('created_date', None)
            status = request.query_params.get('status', None)
            queryset = self.get_queryset()

            if not (user.is_superuser or user.roles == "ADMIN"):
                queryset = queryset.filter(user=user)

            if order_number:
                queryset = queryset.filter(order_number__icontains=order_number)
            if created_date:
                queryset = queryset.filter(created_at__date=created_date)
            if status:
                queryset = queryset.filter(status__icontains=status)

            paginator = PageNumberPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST
            )

