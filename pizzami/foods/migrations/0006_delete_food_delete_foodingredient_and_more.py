# Generated by Django 4.0.7 on 2024-01-21 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0005_foodcategorycompound_food_catego_food_ca_238771_idx'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Food',
        ),
        migrations.DeleteModel(
            name='FoodIngredient',
        ),
        migrations.AlterModelOptions(
            name='foodcategorycompound',
            options={'ordering': ('position',), 'verbose_name': 'Food Category Compound', 'verbose_name_plural': 'Food Category Compounds'},
        ),
    ]
