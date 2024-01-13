from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from orders.utils import create_sign

User = get_user_model()


class Order(models.Model):
    NEW = 'NEW'
    LOAN_CREATED = 'LOAN_CREATED'
    DECLINED = 'DECLINED'
    EXPIRED = 'EXPIRED'
    STATUS_CHOICES = (
        (NEW, NEW),
        (LOAN_CREATED, LOAN_CREATED),
        (DECLINED, DECLINED),
        (EXPIRED, EXPIRED),
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_id = models.PositiveIntegerField()
    amount_requested = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal(1000000.00))
    amount_approved = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
    period_requested = models.SmallIntegerField(validators=(MinValueValidator(36), MaxValueValidator(84)))
    period_approved = models.SmallIntegerField(validators=(MinValueValidator(36), MaxValueValidator(84)), blank=True)
    sign = models.SmallIntegerField(default=create_sign)
    contract = models.CharField(max_length=256, blank=True, null=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=NEW)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id is None:
            self._validate_has_order()
            self._validate_open_loan()
            self._validate_credit_score()
            super().save(force_insert, force_update, using, update_fields)

    def _validate_has_order(self):
        if Order.objects.filter(user_id=self.user_id, status=self.NEW).exists():
            raise ValidationError('has_order')

    def _validate_open_loan(self):
        pass
        # raise ValidationError('has_open_loan')

    def _validate_credit_score(self):
        # raise ValidationError('low_credit_score')
        self._set_amount_approved()
        self._set_period_approved()

    def _set_amount_approved(self):
        self.amount_approved = self.amount_requested

    def _set_period_approved(self):
        self.period_approved = self.period_requested

    def set_loan_created(self):
        self.status = self.LOAN_CREATED
        super().save()
