# Generated by Django 4.0.7 on 2024-02-18 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('orders', '0002_alter_order_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discount',
            name='specified_object',
        ),
        migrations.AddField(
            model_name='discount',
            name='specified_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='contenttypes.contenttype', verbose_name='specified type'),
        ),
    ]
