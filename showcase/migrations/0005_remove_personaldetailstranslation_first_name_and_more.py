# Generated by Django 4.1.3 on 2022-11-23 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0004_remove_personaldetailstranslation_address_line_1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personaldetailstranslation',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='personaldetailstranslation',
            name='last_name',
        ),
        migrations.AddField(
            model_name='personaldetails',
            name='first_name',
            field=models.CharField(max_length=255, null=True, verbose_name='first_name'),
        ),
        migrations.AddField(
            model_name='personaldetails',
            name='last_name',
            field=models.CharField(max_length=255, null=True, verbose_name='last_name'),
        ),
        migrations.AddField(
            model_name='personaldetailstranslation',
            name='add_to_email_list',
            field=models.BooleanField(null=True),
        ),
    ]