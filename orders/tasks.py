import random
import time
from datetime import timedelta

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from conf.celery import app
from orders.models import Order


@app.task
def debug_task():
    time.sleep(random.randint(5, 10))
    return 'Hello from debug_task!'


@app.task(serializer='json')
def create_order_task(user_id, amount_requested, period_requested):
    time.sleep(random.randint(5, 10))
    try:
        order = Order.objects.create(
            user_id=user_id,
            amount_requested=amount_requested,
            period_requested=period_requested,
        )
        return {
            'id': order.id,
            'user_id': order.user_id,
            'amount_requested': order.amount_requested,
            'amount_approved': order.amount_approved,
            'period_requested': order.period_requested,
            'period_approved': order.period_approved,
            'sign': order.sign,
            'contract': order.contract,
            'status': order.status,
        }
    except Exception as error:
        raise ValidationError(f'create_order_task_error: {error}')


@app.task
def check_orders_lifetime_task():
    order_lifetime_min = timedelta(minutes=1)
    qs = Order.objects.all().filter(created__gte=timezone.now() - timedelta(hours=1, minutes=5)).filter(status='NEW')
    for order in qs:
        if order.created < timezone.now() - order_lifetime_min:
            order.set_expired()
    return 'check_orders_lifetime_task_finished'
