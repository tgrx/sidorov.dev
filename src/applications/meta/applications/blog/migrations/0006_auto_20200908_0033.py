# Generated by Django 3.1.1 on 2020-09-07 21:33

import storages.backends.s3boto3
from django.db import migrations
from django.db import models

import applications.meta.applications.blog.models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0005_photo_thumbnail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photo",
            name="original",
            field=models.FileField(
                storage=storages.backends.s3boto3.S3Boto3Storage(),
                upload_to=applications.meta.applications.blog.models.upload_to,
            ),
        ),
        migrations.AlterField(
            model_name="photo",
            name="thumbnail",
            field=models.FileField(
                blank=True,
                null=True,
                storage=storages.backends.s3boto3.S3Boto3Storage(),
                upload_to=applications.meta.applications.blog.models.upload_to,
            ),
        ),
    ]