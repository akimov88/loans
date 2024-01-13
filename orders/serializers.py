from rest_framework import serializers
from orders.models import Order


class CurrentUserIdDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user.id


class ReadOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=CurrentUserIdDefault())

    class Meta:
        model = Order
        fields = ('user_id', 'amount_requested', 'period_requested')
