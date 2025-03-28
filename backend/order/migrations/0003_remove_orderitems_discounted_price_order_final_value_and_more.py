# Generated by Django 5.1.7 on 2025-03-27 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_coupon_order_status_alter_order_applied_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitems',
            name='discounted_price',
        ),
        migrations.AddField(
            model_name='order',
            name='final_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
