from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage, send_mail
from django.db import transaction
from .models import User

# * Registration View
class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                validated_data = serializer.data
                welcome_email = EmailMessage(
                    subject= "Registration Successful",
                    body = f'Welcome {validated_data["username"]} to Flora Store',
                    to = [validated_data['email'] ]  
                )
                welcome_email.send(fail_silently=False)
                return Response(
                    {
                    "message": "User Created Successfully",
                    "status": status.HTTP_201_CREATED,
                    "data": validated_data
                    }, status = status.HTTP_201_CREATED
                )
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST,
                }, status= status.HTTP_400_BAD_REQUEST
            )

# * login view        
class LoginView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        try:
                
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]
            print(user)
            tokens = serializer.get_token(user)
            return Response(
                {
                    "message": "User Logged In successfully",
                    "status": status.HTTP_200_OK,
                    "tokens": tokens
                }, status= status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST,
                }, status= status.HTTP_400_BAD_REQUEST
            )

# view to list out user        
class UserListView(GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:

            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "message": "User List Retrieved successfully",
                    "status": status.HTTP_200_OK,
                    "data": serializer.data
                }, status= status.HTTP_200_OK
            )    
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST,
                }, status= status.HTTP_400_BAD_REQUEST
            )

    # overriding the get queryset to allow admin see the entire list and user see only theirs    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser or user.roles == "ADMIN":
            return queryset
        return queryset.none()

 # the detail view for a particular user   
class UserDetailView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            if request.user.id != user.id:
                return Response(
                    {
                        "message": "You do not have permissions to perform this action",
                        "status": status.HTTP_403_FORBIDDEN,
                    }, status= status.HTTP_403_FORBIDDEN
                )
            serializer = self.get_serializer(user)
            return Response(
                {
                    "message": "User List Retrieved successfully",
                    "status": status.HTTP_200_OK,
                    "data": serializer.data
                }, status= status.HTTP_200_OK
            )  
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST,
                }, status= status.HTTP_400_BAD_REQUEST
            )
