# Generated by Django 5.2 on 2025-04-30 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]
