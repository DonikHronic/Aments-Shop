# Generated by Django 3.2.5 on 2021-09-17 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aments_shop', '0020_auto_20210917_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='postreview',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aments_shop.postreview', verbose_name='Родительский отзыв'),
        ),
    ]
