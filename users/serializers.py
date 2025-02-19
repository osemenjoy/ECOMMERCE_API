from .models import User, Address
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


# registration serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:            
        model = User
        fields = ("username","first_name", "last_name", "password", "email","phone_number", "gender")
        extra_kwargs = {"password": {"write_only": True}}

    # validate password length and content
    def validate_password(self, password):

        if len(password) < 8:
            raise serializers.ValidationError("Password must be greater than 8 characters")
        if not any(char in "!@#$%^&*()_+-=[]{}|;':,.<>?/~`" for char in password):
            raise serializers.ValidationError("Password must contain at least one special character")
        return password
    
    # create new user
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)   
        return user

# login serializer    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only= True)

    #  validate the email and the password
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise serializers.ValidationError("Invalid Credentials")
            except User.DoesNotExist:
                raise serializers.ValidationError("Email not found")
        else:
            raise serializers.ValidationError("Email and Password are required")
        
        data["user"] = user
        return data
    
    # create jwt token for a user
    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        print(refresh)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }

# user serializer    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "phone_number", "gender", )
        extra_kwargs = {"password": {"write_only": True}}   

# address serializer
class AddressSerializer(serializers.ModelSerializer):
    state = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    house_number = serializers.CharField(required=False, allow_blank=True)
    street = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Address
        fields = ["id", "state", "city", "house_number", "street"]

                