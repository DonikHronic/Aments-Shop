# Generated by Django 3.2.5 on 2021-08-20 16:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aments_shop', '0009_auto_20210820_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.today, verbose_name='Дата добавления'),
        ),
    ]
