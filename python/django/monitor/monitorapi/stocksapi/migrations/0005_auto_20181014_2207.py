# Generated by Django 2.1.1 on 2018-10-14 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocksapi', '0004_stockpricestatistics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockpricestatistics',
            name='remark',
            field=models.CharField(max_length=50, null=True),
        ),
    ]