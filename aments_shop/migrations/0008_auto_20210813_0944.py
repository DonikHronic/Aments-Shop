# Generated by Django 3.2.5 on 2021-08-13 09:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aments_shop', '0007_auto_20210813_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.today, verbose_name='Дата заказа'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime.today, verbose_name='Дата публикации'),
        ),
    ]
