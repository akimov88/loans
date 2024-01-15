import random
import time
from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from conf.celery import app
from orders.models import Order
from orders.models import StatusChoices


@app.task
def debug_task():
    time.sleep(random.randint(5, 10))
    return 'Hello from debug_task!'


@shared_task
def debug_shared_task():
    time.sleep(random.randint(5, 10))
    return 'Hello from debug_shared_task!'


@app.task(serializer='json')
def create_order_task(user_id, amount_requested, period_requested):
    try:
        order = Order.objects.create(
            user_id=user_id,
            amount_requested=amount_requested,
            period_requested=period_requested,
        )
        return {
            'id': order.id,
            'user_id': order.user_id,
            'amount_approved': order.amount_approved,
            'period_approved': order.period_approved,
            'contract': order.contract,
            'status': order.status,
        }
    except Exception as error:
        raise ValidationError(f'create_order_task_error: {error}')


@app.task
def check_order_lifetime_task():
    order_lifetime_min = timedelta(minutes=1)
    last_hour_orders = Order.objects.all().filter(
        created__gte=timezone.now() - timedelta(hours=1, minutes=5),
        status=StatusChoices.NEW
    )
    for order in last_hour_orders:
        if timezone.now() - order.created > order_lifetime_min:
            order.set_expired()
    return 'check_order_lifetime_task finished!'
