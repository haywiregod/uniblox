# Generated by Django 5.1.7 on 2025-03-27 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_coupon_order_status_alter_order_applied_coupon'),
        ('product', '0003_rename_quantity_product_available_quantity'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Coupon',
        ),
    ]
