# Generated by Django 2.0.4 on 2018-04-16 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='commet',
            new_name='comment',
        ),
    ]
