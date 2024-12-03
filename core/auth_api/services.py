from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from core.models import User


def get_jwt_tokens(user):
    access_token = AccessToken.for_user(user)
    refresh_token = RefreshToken.for_user(user)

    return (access_token, refresh_token)


def black_list_refresh_token(refresh_token):
    refresh_token = RefreshToken(refresh_token)
    refresh_token.blacklist()


def get_access_from_refresh(refresh_token):
    refresh = RefreshToken(refresh_token)
    access = str(refresh.access_token)
    return access


def signup(validated_data):
    username = validated_data.get('username')
    password = validated_data.get('password')

    User.objects.create_user(username=username, password=password)

    return {"message": "User created successfully"}


def login(validated_data):
    username = validated_data.get('username')
    password = validated_data.get('password')

    user = authenticate(username=username, password=password)

    access_token, refresh_token = get_jwt_tokens(user)
    return str(access_token), str(refresh_token)
