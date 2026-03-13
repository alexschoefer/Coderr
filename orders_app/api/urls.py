from django.urls import path
from .views import OrderListAPIView, SingleOrderView, InProgressOrderListView, CompletedOrderCountListView

urlpatterns = [
    path('api/orders/', OrderListAPIView.as_view(), name="order-list"),
    path('api/orders/<int:pk>/', SingleOrderView.as_view(), name="single-order"),
    path('api/order-count/<int:pk>/', InProgressOrderListView.as_view(), name="in-progress-order-count"),
    path('api/completed-order-count/<int:pk>/', CompletedOrderCountListView.as_view(), name="completed-order-count"),
]
