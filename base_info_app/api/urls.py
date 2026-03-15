from django.urls import path
from .views import BaseInfoAPIView


urlpatterns = [
    path('api/base-info/', BaseInfoAPIView.as_view(), name='base-info'),
]
