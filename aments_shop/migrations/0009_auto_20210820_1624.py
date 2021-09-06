# Generated by Django 3.2.5 on 2021-08-20 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aments_shop', '0008_auto_20210813_0944'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'db_table': 'category',
            },
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_photo',
            field=models.ImageField(blank=True, null=True, upload_to='users_photos/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='preview',
            field=models.ImageField(upload_to='post_previews/', verbose_name='Превью'),
        ),
        migrations.AlterField(
            model_name='product',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Превью'),
        ),
        migrations.CreateModel(
            name='ProjectAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views', models.IntegerField(default=0, verbose_name='Просмотры')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aments_shop.product')),
            ],
            options={
                'db_table': 'analytic',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aments_shop.category', verbose_name='Категория'),
        ),
    ]