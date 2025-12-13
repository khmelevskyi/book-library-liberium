"""
Serializers for user authentication and management.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
        read_only_fields = ('id', 'is_staff', 'date_joined')


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label='Confirm Password')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': True},
        }

    def validate(self, attrs: dict) -> dict:
        """Validate that passwords match."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password fields did not match.'})
        return attrs

    def create(self, validated_data: dict) -> User:
        """Create a new user."""
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer to include user data."""

    @classmethod
    def get_token(cls, user: User):
        """Add custom claims to token."""
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token
