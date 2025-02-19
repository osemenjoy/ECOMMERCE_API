# Generated by Django 5.1.6 on 2025-02-14 17:11

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_category_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=cloudinary.models.CloudinaryField(default='none', max_length=255, verbose_name='image'),
            preserve_default=False,
        ),
    ]
