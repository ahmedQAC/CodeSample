from rest_framework.permissions import AllowAny
from rest_framework import generics
from users.models import CustomUser
from users.serializers import (RegisterUserSerializer,
                               UpdateUserSerializer,
                               ViewUserSerializer)


# Create your views here.
class UserCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        instance = queryset.get(pk=self.request.user.pk)
        return instance


class UserViewAPIView(generics.RetrieveAPIView):
    """View other user profiles"""
    queryset = CustomUser.objects.all()
    serializer_class = ViewUserSerializer
    lookup_field = 'username'