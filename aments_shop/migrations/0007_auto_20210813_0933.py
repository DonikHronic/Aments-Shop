# Generated by Django 3.2.5 on 2021-08-13 09:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aments_shop', '0006_auto_20210812_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 13, 9, 33, 49, 484267), verbose_name='Дата заказа'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 13, 9, 33, 49, 485228), verbose_name='Дата публикации'),
        ),
    ]
