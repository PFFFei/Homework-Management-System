# Generated by Django 2.0.5 on 2019-04-22 01:52

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='excerpt',
        ),
        migrations.AlterField(
            model_name='notice',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]