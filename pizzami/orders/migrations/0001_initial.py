# Generated by Django 4.0.7 on 2024-02-18 08:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('foods', '0012_alter_foodingredient_ingredient'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0013_alter_profile_public_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('position', models.PositiveIntegerField(default=0, editable=False, verbose_name='position')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_alive', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='carts', to='users.profile', verbose_name='user')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
                'db_table': 'cart',
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('position', models.PositiveIntegerField(default=0, editable=False, verbose_name='position')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('is_public', models.BooleanField(default=True, verbose_name='is public')),
                ('code', models.CharField(max_length=10, null=True, unique=True, verbose_name='code')),
                ('has_time_limit', models.BooleanField(default=False, verbose_name='has time limit')),
                ('type', models.CharField(choices=[('ABS', 'absolute'), ('RAT', 'ration')], max_length=20, verbose_name='type')),
                ('start_date', models.DateTimeField(blank=True, null=True, verbose_name='start date')),
                ('expiration_date', models.DateTimeField(blank=True, null=True, verbose_name='expiration date')),
                ('specified_to_type', models.CharField(blank=True, choices=[('USR', 'user'), ('FOD', 'food'), ('CAT', 'category')], max_length=20, null=True, verbose_name='specified to type')),
                ('object_id', models.CharField(max_length=50)),
                ('percentage_value', models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)], verbose_name='percentage value')),
                ('absolute_value', models.FloatField(blank=True, null=True, verbose_name='absolute value')),
                ('specified_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='contenttypes.contenttype', verbose_name='specified object')),
            ],
            options={
                'verbose_name': 'Discount',
                'verbose_name_plural': 'Discounts',
                'db_table': 'discount',
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('position', models.PositiveIntegerField(default=0, editable=False, verbose_name='position')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=256, verbose_name='address')),
                ('status', models.CharField(choices=[('RTP', 'ready to pay'), ('PD', 'paid'), ('RJC', 'rejected'), ('IPR', 'in progress'), ('DLV', 'delivered')], default='RTP', max_length=20, verbose_name='status')),
                ('total_value', models.FloatField(verbose_name='total value')),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='order', to='orders.cart', verbose_name='cart')),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='orders', to='orders.discount', verbose_name='discount')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'db_table': 'order',
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('position', models.PositiveIntegerField(default=0, editable=False, verbose_name='position')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('is_income', models.BooleanField(default=True, verbose_name='is income')),
                ('tracking_code', models.CharField(max_length=256, verbose_name='tracking code')),
                ('payment_data', models.TextField(blank=True, null=True, verbose_name='payment data')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='payments', to='orders.order', verbose_name='order')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
                'db_table': 'payment',
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('position', models.PositiveIntegerField(default=0, editable=False, verbose_name='position')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('count', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='count')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.cart', verbose_name='cart')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='cart_items', to='foods.food', verbose_name='food')),
            ],
            options={
                'verbose_name': 'Cart Item',
                'verbose_name_plural': 'Cart Items',
                'db_table': 'cart item',
                'ordering': ('position',),
            },
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['position'], name='order_positio_ec7ff6_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['created_at'], name='order_created_6dbd10_idx'),
        ),
    ]