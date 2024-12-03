import re

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import User


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'password'
        ]

    def validate_username(self, value):
        if not value.strip():
            raise serializers.ValidationError('Username cannot be empty')
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        if not re.match(r'^[\w]+$', value):
            raise serializers.ValidationError('Username can only contain letters, numbers, and underscores')
        if len(value) < 3:
            raise serializers.ValidationError('Username must be at least 3 characters long')
        if len(value) > 64:
            raise serializers.ValidationError('Username must be at most 64 characters long')
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError('Password cannot be empty')

        validate_password(value)
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username).first()

        if not all([username, password]):
            raise serializers.ValidationError('Username and password are required')

        if not user:
            raise serializers.ValidationError('Username or password is invalid')

        if not user.check_password(password):
            raise serializers.ValidationError('Username or password is invalid')

        return data


class RefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=2500, required=True)

    def validate_refresh_token(self, value):
        try:
            RefreshToken(value)
        except Exception:
            raise serializers.ValidationError("Invalid refresh token")
        return value
