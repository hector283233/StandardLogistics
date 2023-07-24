# Generated by Django 4.2 on 2023-07-22 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_ba_attribute_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ba_attribute',
            name='title_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ady (en)'),
        ),
        migrations.AlterField(
            model_name='ba_attribute',
            name='title_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ady (ru)'),
        ),
        migrations.AlterField(
            model_name='ba_attribute_value',
            name='value_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Baha (en)'),
        ),
        migrations.AlterField(
            model_name='ba_attribute_value',
            name='value_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Baha (ru)'),
        ),
        migrations.AlterField(
            model_name='ba_attribute_value',
            name='value_tm',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Baha (tm)'),
        ),
    ]