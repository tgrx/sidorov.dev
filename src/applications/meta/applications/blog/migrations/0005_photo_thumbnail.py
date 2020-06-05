# Generated by Django 3.0.7 on 2020-06-05 14:25

from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200524_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='thumbnail',
            field=models.FileField(blank=True, editable=False, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(), upload_to=''),
        ),
    ]