# Generated by Django 4.0.7 on 2024-02-24 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_confirmed',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='is confirmed'),
        ),
    ]