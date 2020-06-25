# Generated by Django 3.1.1 on 2020-09-07 22:47

import storages.backends.s3boto3
from django.db import migrations
from django.db import models

import applications.meta.applications.blog.models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_auto_20200908_0033"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photo",
            name="original",
            field=models.FileField(
                max_length=2000,
                storage=storages.backends.s3boto3.S3Boto3Storage(),
                upload_to=applications.meta.applications.blog.models.upload_to,
            ),
        ),
        migrations.AlterField(
            model_name="photo",
            name="thumbnail",
            field=models.FileField(
                blank=True,
                max_length=2000,
                null=True,
                storage=storages.backends.s3boto3.S3Boto3Storage(),
                upload_to=applications.meta.applications.blog.models.upload_to,
            ),
        ),
    ]
