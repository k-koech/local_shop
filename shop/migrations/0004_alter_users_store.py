# Generated by Django 3.2.8 on 2021-10-09 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20211009_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='store',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
