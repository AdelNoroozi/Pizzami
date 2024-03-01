# Generated by Django 4.0.7 on 2024-03-01 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_address_phone_number'),
        ('feedback', '0002_comment_is_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='by_staff',
            field=models.BooleanField(default=False, verbose_name='by staff'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='users.profile', verbose_name='user'),
        ),
    ]
