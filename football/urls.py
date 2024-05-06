from django.urls import path
from .views import (SessionCreateAPIView,
                    SessionUpdateAPIView,
                    SessionCancelAPIView,
                    SessionHostedAPIView,
                    SessionAllAPIView,
                    SessionAPIView)

app_name = 'football'

urlpatterns = [
    path('create/', SessionCreateAPIView.as_view(), name='create'),
    path('update/<int:pk>/', SessionUpdateAPIView.as_view(), name='update'),
    path('cancel/<int:pk>/', SessionCancelAPIView.as_view(), name='cancel'),
    path('hosted/', SessionHostedAPIView.as_view(), name='hosted'),
    path('all/', SessionAllAPIView.as_view(), name='all'),
    path('view/<int:pk>/', SessionAPIView.as_view(), name='view')
]