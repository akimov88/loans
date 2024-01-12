from rest_framework.serializers import ModelSerializer
from orders.models import Order


class ReadOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('user_id', 'amount_requested', 'amount_approved',
                  'period_requested', 'period_approved', 'sign',
                  'contract', 'status')
        read_only_fields = fields


class CreateOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user_id', 'amount_requested', 'period_requested',
                  'amount_approved', 'period_approved', 'sign',
                  'contract', 'status')
        read_only_fields = ('id', 'amount_approved', 'period_approved',
                            'sign', 'contract', 'status')
