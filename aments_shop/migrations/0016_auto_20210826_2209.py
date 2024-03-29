# Generated by Django 3.2.5 on 2021-08-26 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aments_shop', '0015_delete_categoryanalytics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_in_category', to='aments_shop.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='productanalytics',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_views', to='aments_shop.product', unique=True),
        ),
    ]
