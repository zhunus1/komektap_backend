# Generated by Django 5.0 on 2024-03-11 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='first_name',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appuser',
            name='last_name',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]
