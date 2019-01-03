# Generated by Django 2.1.1 on 2019-01-01 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocksapi', '0009_auto_20190101_1903'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockKDInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_column='Date')),
                ('stock', models.CharField(db_column='Stock', max_length=10, null=True)),
                ('highest', models.DecimalField(db_column='Highest', decimal_places=2, max_digits=5)),
                ('lowest', models.DecimalField(db_column='Lowest', decimal_places=2, max_digits=5)),
                ('rsv', models.DecimalField(db_column='RSV', decimal_places=4, max_digits=5)),
                ('k', models.DecimalField(db_column='K', decimal_places=4, max_digits=5)),
                ('d', models.DecimalField(db_column='D', decimal_places=4, max_digits=5)),
            ],
        ),
    ]
