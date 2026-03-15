# Django imports
from django.urls import path
from .views import ReviewListCreateAPIView, ReviewRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('api/reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('api/reviews/<int:pk>/', ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review-detail'),
]
