# Generated by Django 4.1.3 on 2022-11-18 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models
import smart_selects.db_fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/category_pics')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PersonalDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_in_cart', models.IntegerField(blank=True, help_text='Leave this field blank', null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/product_pics')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='media/product_pics')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='media/product_pics')),
                ('category', models.ForeignKey(help_text='Select a category for this product', null=True, on_delete=django.db.models.deletion.SET_NULL, to='showcase.category')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProductInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('a', 'Available'), ('m', 'Maintenance'), ('s', 'Sold'), ('r', 'Reserved')], default='a', help_text='Product availability', max_length=1)),
                ('purchase_date', models.DateField(auto_now=True, null=True)),
                ('buyer', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='showcase.product')),
            ],
            options={
                'ordering': ['purchase_date'],
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(help_text='Select a vendor for this product', null=True, on_delete=django.db.models.deletion.SET_NULL, to='showcase.vendor'),
        ),
        migrations.CreateModel(
            name='VendorTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(help_text='Enter a product category (e.g LG, Samsung)', max_length=250, verbose_name='name')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='showcase.vendor')),
            ],
            options={
                'verbose_name': 'vendor Translation',
                'db_table': 'showcase_vendor_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProductTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('model', models.CharField(help_text='Enter product model', max_length=250, unique=True, verbose_name='model')),
                ('price', models.FloatField(null=True, verbose_name='price')),
                ('discount_price', models.FloatField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='showcase.product')),
            ],
            options={
                'verbose_name': 'product Translation',
                'db_table': 'showcase_product_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProductInstanceTranslation',
            fields=[
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular product in the shop', primary_key=True, serialize=False)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='showcase.productinstance')),
            ],
            options={
                'verbose_name': 'product instance Translation',
                'db_table': 'showcase_productinstance_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PersonalDetailsTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('first_name', models.CharField(max_length=255, null=True, verbose_name='first_name')),
                ('last_name', models.CharField(max_length=255, null=True, verbose_name='last_name')),
                ('phone_number', models.CharField(max_length=255, null=True, verbose_name='phone_number')),
                ('address_line_1', models.CharField(max_length=255, null=True, verbose_name='address_line_1')),
                ('address_line_2', models.CharField(blank=True, max_length=255, null=True, verbose_name='address_line_2')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='city')),
                ('zip_code', models.CharField(max_length=255, null=True, verbose_name='zip_code')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.country')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='showcase.personaldetails')),
                ('state', smart_selects.db_fields.ChainedForeignKey(chained_field='country', chained_model_field='country', on_delete=django.db.models.deletion.CASCADE, to='cities_light.region')),
            ],
            options={
                'verbose_name': 'personal details Translation',
                'db_table': 'showcase_personaldetails_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(help_text='Enter a product category (e.g TV, Fans)', max_length=250, verbose_name='name')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='showcase.category')),
            ],
            options={
                'verbose_name': 'category Translation',
                'db_table': 'showcase_category_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
