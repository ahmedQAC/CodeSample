from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings


# Create your views here.

class GoogleLoginURLView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Return URL used to sign in using Google account
        """
        client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
        callback_endpoint = settings.GOOGLE_CALLBACK_ENDPOINT

        google_endpoint = f'https://accounts.google.com/o/oauth2/v2/auth?redirect_uri={callback_endpoint}&prompt=consent&response_type=code&client_id={client_id}&scope=openid%20email%20profile&access_type=offline'
        return Response({'google_endpoint': google_endpoint})


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    # callback_url = "http://localhost:3000/api/auth/callback/google"
    # callback_url = "https://49d5-86-21-170-53.ngrok-free.app/googlecallback/"
    callback_url = settings.GOOGLE_CALLBACK_ENDPOINT
    client_class = OAuth2Client
    permission_classes = [AllowAny]