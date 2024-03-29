# Generated by Django 4.0.3 on 2022-03-17 02:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a product category (e.g TV, Fans)', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(help_text='Enter product model', max_length=250, unique=True)),
                ('price', models.FloatField(null=True)),
                ('discount_price', models.FloatField(blank=True, null=True)),
                ('decription', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(help_text='Select a category for this product', null=True, on_delete=django.db.models.deletion.SET_NULL, to='showcase.category')),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a product category (e.g LG, Samsung)', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='ProductInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular product in the shop', primary_key=True, serialize=False)),
                ('purchase_date', models.DateField(auto_now=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('a', 'Available'), ('m', 'Maintenance'), ('s', 'Sold'), ('r', 'Reserved')], default='a', help_text='Product availability', max_length=1)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='showcase.product')),
            ],
            options={
                'ordering': ['purchase_date'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(help_text='Select a vendor for this product', null=True, on_delete=django.db.models.deletion.SET_NULL, to='showcase.vendor'),
        ),
    ]
