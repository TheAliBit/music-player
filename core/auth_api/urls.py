from django.urls import path

from .api_views import SignupAPIView, LoginAPIView, RefreshAPIView, LogoutAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('refresh/', RefreshAPIView.as_view()),

    path('logout/', LogoutAPIView.as_view()),
]
