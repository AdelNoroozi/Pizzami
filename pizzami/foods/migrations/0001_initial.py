# Generated by Django 4.0.7 on 2023-11-04 07:05

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ingredients', '0009_alter_ingredient_options_alter_ingredient_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('image_url', models.CharField(max_length=512, verbose_name='image url')),
                ('image_alt_text', models.CharField(max_length=50, verbose_name='image alt text')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('image_url', models.CharField(max_length=512, verbose_name='image url')),
                ('image_alt_text', models.CharField(max_length=50, verbose_name='image alt text')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('icon_url', models.CharField(max_length=512, verbose_name='icon url')),
                ('icon_alt_text', models.CharField(max_length=50, verbose_name='icon alt text')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='position')),
                ('is_customizable', models.BooleanField(verbose_name='is customizable')),
            ],
            options={
                'verbose_name': 'Food Category',
                'verbose_name_plural': 'Food Categories',
                'db_table': 'food_category',
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='FoodIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FoodCategoryCompound',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('min', models.PositiveIntegerField(default=1, verbose_name='min')),
                ('max', models.PositiveIntegerField(verbose_name='max')),
                ('food_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compounds', to='foods.foodcategory', verbose_name='category')),
                ('ingredient_category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='food_categories', to='ingredients.ingredientcategory', verbose_name='ingredient_category')),
            ],
            options={
                'verbose_name': 'Food Category Compound',
                'verbose_name_plural': 'Food Category Compound',
                'db_table': 'food_category_compound',
            },
        ),
    ]
