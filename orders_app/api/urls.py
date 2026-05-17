from django.urls import path
from .views import OrderListAPIView, SingleOrderView, InProgressOrderListView, CompletedOrderCountListView

urlpatterns = [
    path('orders/', OrderListAPIView.as_view(), name="order-list"),
    path('orders/<int:pk>/', SingleOrderView.as_view(), name="single-order"),
    path('order-count/<int:pk>/', InProgressOrderListView.as_view(), name="in-progress-order-count"),
    path('completed-order-count/<int:pk>/', CompletedOrderCountListView.as_view(), name="completed-order-count"),
]
