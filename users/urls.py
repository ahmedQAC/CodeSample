from django.urls import path
from users.views import (UserCreateAPIView,
                         UserUpdateAPIView,
                         UserViewAPIView)

app_name = 'users'

urlpatterns = [
    path('', UserCreateAPIView.as_view(), name='create'),
    path('update/', UserUpdateAPIView.as_view(), name='update'),
    path('<str:username>/', UserViewAPIView.as_view(), name='view')
]