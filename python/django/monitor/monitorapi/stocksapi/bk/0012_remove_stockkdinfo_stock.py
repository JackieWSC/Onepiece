# Generated by Django 2.1.1 on 2019-01-01 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocksapi', '0011_remove_stockkdinfo_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockkdinfo',
            name='stock',
        ),
    ]
