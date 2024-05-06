from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import GoogleLogin, GoogleLoginURLView

app_name = 'authentication'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('oauth2/google/login/url/', GoogleLoginURLView.as_view(), name='google_login_url'),
    path("oauth2/google/login/", GoogleLogin.as_view(), name="google_login"),
]