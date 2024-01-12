from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from orders.models import Order
from orders.serializers import ReadOrderSerializer, CreateOrderSerializer


class OrderViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            serializer_class = ReadOrderSerializer
        else:
            serializer_class = CreateOrderSerializer
        return serializer_class
