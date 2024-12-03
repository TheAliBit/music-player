from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.auth_api.serializers import SignupSerializer, LoginSerializer, RefreshSerializer
from core.auth_api.services import signup, login, get_access_from_refresh, black_list_refresh_token


class SignupAPIView(APIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            response = signup(serializer.validated_data)

        return Response(response, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            access_token, refresh_token = login(serializer.validated_data)
            return Response({'access_token': access_token, 'refresh_token': refresh_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RefreshAPIView(APIView):
    serializer_class = RefreshSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = get_access_from_refresh(serializer.validated_data['refresh_token'])
        return Response({'access_token': access_token}, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    serializer_class = RefreshSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        black_list_refresh_token(serializer.validated_data['refresh_token'])

        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
