# Generated by Django 2.1.1 on 2018-10-06 03:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stocksapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
