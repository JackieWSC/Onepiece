# Generated by Django 2.1.1 on 2019-01-01 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocksapi', '0008_auto_20181230_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockdailyinfo',
            name='close',
            field=models.DecimalField(db_column='Close', decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='stockdailyinfo',
            name='date',
            field=models.DateField(db_column='Date'),
        ),
        migrations.AlterField(
            model_name='stockdailyinfo',
            name='high',
            field=models.DecimalField(db_column='High', decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='stockdailyinfo',
            name='low',
            field=models.DecimalField(db_column='Low', decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='stockdailyinfo',
            name='stock',
            field=models.CharField(db_column='Stock', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='stockkdinfo',
            name='d',
            field=models.DecimalField(db_column='D', decimal_places=4, max_digits=5),
        ),
        migrations.AlterField(
            model_name='stockkdinfo',
            name='highest',
            field=models.DecimalField(db_column='Stock', decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='stockkdinfo',
            name='k',
            field=models.DecimalField(db_column='K', decimal_places=4, max_digits=5),
        ),
        migrations.AlterField(
            model_name='stockkdinfo',
            name='lowest',
            field=models.DecimalField(db_column='Highest', decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='stockkdinfo',
            name='rsv',
            field=models.DecimalField(db_column='Lowest', decimal_places=4, max_digits=5),
        ),
        migrations.AlterField(
            model_name='stockkdinfo',
            name='stock',
            field=models.CharField(db_column='Date', max_length=10, null=True),
        ),
    ]
