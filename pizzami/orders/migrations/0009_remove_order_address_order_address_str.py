# Generated by Django 4.0.7 on 2024-02-24 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.AddField(
            model_name='order',
            name='address_str',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='address'),
        ),
    ]
