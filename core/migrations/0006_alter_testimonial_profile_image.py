# Generated by Django 5.2 on 2025-05-07 06:16

import filebrowser.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_testimonial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonial',
            name='profile_image',
            field=filebrowser.fields.FileBrowseField(blank=True, max_length=200, null=True, verbose_name='Image'),
        ),
    ]
