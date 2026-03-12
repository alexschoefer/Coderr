from django.urls import path
from .views import OrderListAPIView, SingleOrderView

urlpatterns = [
    path('api/orders/', OrderListAPIView.as_view(), name="order-list"),
    path('api/orders/<int:pk>/', SingleOrderView.as_view(), name="single-order")
]
