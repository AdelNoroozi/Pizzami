# Generated by Django 4.0.7 on 2023-12-22 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_baseuser_users_baseu_email_97cf3e_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='public_name',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='public name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='bio'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
