# Generated by Django 4.0.7 on 2023-12-22 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_profile_public_name_alter_profile_bio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='public_name',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='public name'),
        ),
    ]