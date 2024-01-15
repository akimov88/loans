# Generated by Django 4.2.8 on 2024-01-15 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_amount_requested_alter_order_sign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NEW', 'новый'), ('LOAN_CREATED', 'кредит создан'), ('DECLINED', 'отменён'), ('EXPIRED', 'истёк')], default='NEW', max_length=32),
        ),
    ]
