# Generated by Django 4.2 on 2023-07-17 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute_Values',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_tm', models.CharField(max_length=255)),
                ('value_ru', models.CharField(max_length=255)),
                ('value_en', models.CharField(max_length=255)),
                ('file', models.FileField(blank=True, null=True, upload_to='attributes/')),
            ],
        ),
        migrations.CreateModel(
            name='Attributes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_tm', models.CharField(max_length=255)),
                ('title_ru', models.CharField(max_length=255)),
                ('title_en', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='attributes/')),
            ],
        ),
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_notified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CommonModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('is_vip', models.BooleanField(default=False)),
                ('title_tm', models.CharField(blank=True, max_length=255, null=True)),
                ('title_ru', models.CharField(blank=True, max_length=255, null=True)),
                ('title_en', models.CharField(blank=True, max_length=255, null=True)),
                ('description_tm', models.TextField(blank=True, null=True)),
                ('description_ru', models.TextField(blank=True, null=True)),
                ('description_en', models.TextField(blank=True, null=True)),
                ('image1', models.ImageField(blank=True, null=True, upload_to='services/')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='services/')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='services/')),
                ('image4', models.ImageField(blank=True, null=True, upload_to='services/')),
                ('rating', models.FloatField(default=0)),
                ('rating_count', models.IntegerField(default=0)),
                ('seen_count', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
