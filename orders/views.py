from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from orders.models import Order
from orders.serializers import ReadOrderSerializer, CreateOrderSerializer
from orders.tasks import create_order_task


class OrderViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Order.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            serializer_class = ReadOrderSerializer
        else:
            serializer_class = CreateOrderSerializer
        return serializer_class


class OrderTaskAPIView(CreateAPIView, ListAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        task = create_order_task.delay(
            user_id=request.user.id,
            amount_requested=request.data.get('amount_requested'),
            period_requested=request.data.get('period_requested')
        )
        return Response({'task_uuid': task.id})
