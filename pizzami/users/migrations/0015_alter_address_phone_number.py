# Generated by Django 4.0.7 on 2024-02-23 15:50

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='phone number'),
        ),
    ]
