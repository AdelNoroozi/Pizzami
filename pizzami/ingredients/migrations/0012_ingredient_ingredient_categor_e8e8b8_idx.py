# Generated by Django 4.0.7 on 2023-11-24 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0011_alter_ingredient_options_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='ingredient',
            index=models.Index(fields=['category', 'position'], name='ingredient_categor_e8e8b8_idx'),
        ),
    ]
