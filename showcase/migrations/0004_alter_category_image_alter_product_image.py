# Generated by Django 4.0.3 on 2022-03-17 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0003_rename_decription_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/category_pics'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/product_pics'),
        ),
    ]
