# Generated by Django 4.0.3 on 2022-03-17 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
