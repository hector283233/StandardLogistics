# Generated by Django 4.2 on 2023-07-29 19:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_alter_attribute_values_file_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0002_alter_cargo_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='warehouseattributevalue',
            options={'verbose_name': 'Ammar Attribýut Baha', 'verbose_name_plural': 'Ammarlar Attribýut Bahalar'},
        ),
        migrations.CreateModel(
            name='WarehouseComment',
            fields=[
                ('commentmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='common.commentmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_warehouse_comment', to=settings.AUTH_USER_MODEL, verbose_name='Ulanyjy')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_warehouse_comment', to='service.warehouse', verbose_name='Ammar')),
            ],
            options={
                'verbose_name': 'Ammar Teswir',
                'verbose_name_plural': 'Ammar Teswirler',
                'ordering': ['-created_at'],
            },
            bases=('common.commentmodel',),
        ),
    ]