# Generated by Django 4.0.7 on 2024-02-18 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.RESTRICT, related_name='order', to='orders.cart', verbose_name='cart'),
        ),
    ]
