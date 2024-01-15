import random
import time
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError

from orders.utils import create_sign

User = get_user_model()


class StatusChoices(models.TextChoices):
    NEW = 'NEW', 'новый'
    LOAN_CREATED = 'LOAN_CREATED', 'кредит создан'
    DECLINED = 'DECLINED', 'отменён'
    EXPIRED = 'EXPIRED', 'истёк'


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_id = models.PositiveIntegerField()
    amount_requested = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal(1000000.00))
    amount_approved = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
    period_requested = models.SmallIntegerField(validators=(MinValueValidator(36), MaxValueValidator(84)))
    period_approved = models.SmallIntegerField(validators=(MinValueValidator(36), MaxValueValidator(84)), blank=True)
    sign = models.SmallIntegerField(default=create_sign)
    contract = models.CharField(max_length=256, blank=True, null=True)
    status = models.CharField(max_length=32, choices=StatusChoices.choices, default=StatusChoices.NEW)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id is None:
            self._validate_has_order()
            self._validate_has_open_loan()
            self._validate_credit_score()
            self._set_amount_approved()
            self._set_period_approved()
            super().save(force_insert, force_update, using, update_fields)

    def _validate_has_order(self):
        if Order.objects.filter(user_id=self.user_id, status=StatusChoices.NEW).exists():
            raise ValidationError('has_order')

    def _validate_has_open_loan(self):
        # if Loan.objects.filter(order__user_id=self.user.id, status_in=['OPEN', 'FROZEN']).exists():
        #     raise ValidationError('has_open_loan')
        pass

    def _validate_credit_score(self):
        # checking client credit score
        # if low: raise ValidationError('low_credit_score')
        time.sleep(random.randint(1, 5))

    def _set_amount_approved(self):
        self.amount_approved = self.amount_requested

    def _set_period_approved(self):
        self.period_approved = self.period_requested

    def set_loan_created(self):
        self.status = StatusChoices.LOAN_CREATED
        super().save()

    def set_expired(self):
        self.status = StatusChoices.EXPIRED
        super().save()

    def set_declined(self):
        self.status = StatusChoices.DECLINED
        super().save()
