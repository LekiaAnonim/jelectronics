# Generated by Django 4.1.3 on 2022-11-14 13:53

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('showcase', '0007_alter_personaldetails_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaldetails',
            name='city',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field='subregion', chained_model_field='subregion', on_delete=django.db.models.deletion.CASCADE, to='cities_light.city'),
        ),
    ]
