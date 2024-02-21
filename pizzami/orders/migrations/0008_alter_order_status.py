# Generated by Django 4.0.7 on 2024-02-21 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_order_has_delivery_alter_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('CRT', 'created'), ('RTP', 'ready to pay'), ('PD', 'paid'), ('RJC', 'rejected'), ('IPR', 'in progress'), ('DLV', 'delivered')], default='CRT', max_length=20, verbose_name='status'),
        ),
    ]