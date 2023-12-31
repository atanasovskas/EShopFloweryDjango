# Generated by Django 4.2.3 on 2023-08-17 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eShopFlowery', '0005_remove_payment_order_payment_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=3)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eShopFlowery.product')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eShopFlowery.order')),
            ],
        ),
    ]
