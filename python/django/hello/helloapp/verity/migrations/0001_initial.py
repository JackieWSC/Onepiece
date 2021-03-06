# Generated by Django 2.0.4 on 2018-05-02 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CaseStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='RefereesDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name', models.CharField(max_length=20)),
                ('relationship', models.CharField(max_length=20)),
                ('contact', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RefereesMain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.CharField(max_length=50)),
                ('actions', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='refereesdetails',
            name='main',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='verity.RefereesMain'),
        ),
        migrations.AddField(
            model_name='casestatus',
            name='details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='verity.RefereesDetails'),
        ),
    ]
