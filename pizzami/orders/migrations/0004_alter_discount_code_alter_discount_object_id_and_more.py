# Generated by Django 4.0.7 on 2024-02-18 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_discount_specified_object_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='code',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='object_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='type',
            field=models.CharField(choices=[('ABS', 'absolute'), ('RAT', 'ratio')], max_length=20, verbose_name='type'),
        ),
    ]