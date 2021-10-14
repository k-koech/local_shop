# Generated by Django 3.2.8 on 2021-10-09 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20211009_0822'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveries',
            name='store',
            field=models.CharField(default='A', max_length=50),
        ),
        migrations.AddField(
            model_name='item',
            name='store',
            field=models.CharField(default='A', max_length=50),
        ),
        migrations.AddField(
            model_name='request',
            name='store',
            field=models.CharField(default='A', max_length=50),
        ),
        migrations.AddField(
            model_name='users',
            name='store',
            field=models.CharField(default='A', max_length=50),
        ),
    ]