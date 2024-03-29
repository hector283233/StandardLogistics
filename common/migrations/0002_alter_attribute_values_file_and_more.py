# Generated by Django 4.2 on 2023-07-22 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute_values',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='attributes/', verbose_name='Faýl'),
        ),
        migrations.AlterField(
            model_name='attribute_values',
            name='value_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Bahasy (en)'),
        ),
        migrations.AlterField(
            model_name='attribute_values',
            name='value_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Bahasy (ru)'),
        ),
        migrations.AlterField(
            model_name='attribute_values',
            name='value_tm',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Bahasy (tm)'),
        ),
        migrations.AlterField(
            model_name='attributes',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='attributes/', verbose_name='Surat'),
        ),
        migrations.AlterField(
            model_name='attributes',
            name='title_en',
            field=models.CharField(max_length=255, verbose_name='Ady (en)'),
        ),
        migrations.AlterField(
            model_name='attributes',
            name='title_ru',
            field=models.CharField(max_length=255, verbose_name='Ady (ru)'),
        ),
        migrations.AlterField(
            model_name='attributes',
            name='title_tm',
            field=models.CharField(max_length=255, verbose_name='Ady (tm)'),
        ),
        migrations.AlterField(
            model_name='commentmodel',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Giňişleýin'),
        ),
        migrations.AlterField(
            model_name='commentmodel',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Aktiwmy?'),
        ),
        migrations.AlterField(
            model_name='commentmodel',
            name='is_notified',
            field=models.BooleanField(default=False, verbose_name='Notifikasiýa ugradylanmy?'),
        ),
        migrations.AlterField(
            model_name='commentmodel',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ady'),
        ),
        migrations.AlterField(
            model_name='commonmodel',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Giňişleýin (en)'),
        ),
        migrations.AlterField(
            model_name='commonmodel',
            name='description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Giňişleýin (ru)'),
        ),
        migrations.AlterField(
            model_name='commonmodel',
            name='description_tm',
            field=models.TextField(blank=True, null=True, verbose_name='Giňişleýin (tm)'),
        ),
        migrations.AlterField(
            model_name='commonmodel',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='services/', verbose_name='Surat 1'),
        ),
        migrations.AlterField(
            model_name='commonmodel',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='services/', verbose_name='Surat 2'),
        ),
        migrations.AlterField(
            model_name='commonmodel',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='services/', verbose_name='Surat 3'),
        ),
        migrations.AlterField(
            model_name='commonmodel',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to='services/', verbose_name='Surat 4'),
        ),
        migrations.AlterField(
            model_name='commonmodel',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Aktiwmy?'),
        ),
        migrations.AlterField(
            model_name='commonmodel',
            name='is_vip',
            field=models.BooleanField(default=False, verbose_name='Wipmy?'),
        ),
        migrations.AlterField(
            model_name='commonmodel',
            name='like_count',
            field=models.IntegerField(default=0, verbose_name='Halanan sany'),
        ),
        migrations.AlterField(
            model_name='commonmodel',
            name='rating',
            field=models.FloatField(default=0, verbose_name='Reýting'),
        ),
        migrations.AlterField(
            model_name='commonmodel',
            name='rating_count',
            field=models.IntegerField(default=0, verbose_name='Reýting sany'),
        ),
        migrations.AlterField(
            model_name='commonmodel',
            name='seen_count',
            field=models.IntegerField(default=0, verbose_name='Görülen sany'),
        ),
        migrations.AlterField(
            model_name='commonmodel',
            name='title_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ady (en)'),
        ),
        migrations.AlterField(
            model_name='commonmodel',
            name='title_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ady (ru)'),
        ),
        migrations.AlterField(
            model_name='commonmodel',
            name='title_tm',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ady (tm)'),
        ),
    ]
