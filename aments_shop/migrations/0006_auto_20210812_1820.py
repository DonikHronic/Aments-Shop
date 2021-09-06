# Generated by Django 3.2.5 on 2021-08-12 18:20

import aments_shop.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aments_shop', '0005_auto_20210812_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 18, 20, 47, 345323), verbose_name='Дата заказа'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 18, 20, 47, 346253), verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='product',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='media/products/', verbose_name='Превью'),
        ),
        migrations.AlterField(
            model_name='productimages',
            name='image',
            field=models.ImageField(upload_to=aments_shop.models.image_path, verbose_name='Изображение продукта'),
        ),
    ]
