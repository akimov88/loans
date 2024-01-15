from rest_framework.routers import SimpleRouter
from orders.views import OrderViewSet, OrderTaskAPIView
from django.urls import path


router = SimpleRouter(trailing_slash=False)

urlpatterns = [
    path('order', OrderViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('order_task', OrderTaskAPIView.as_view()),
]
