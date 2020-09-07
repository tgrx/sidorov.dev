# Generated by Django 3.0.6 on 2020-05-31 21:52

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("resume", "0002_auto_20200421_1418"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="framework",
            options={"ordering": ("name", "version")},
        ),
        migrations.AddField(
            model_name="organization",
            name="is_hidden",
            field=models.BooleanField(default=False, verbose_name="Hide everywhere?"),
        ),
        migrations.AddField(
            model_name="project",
            name="is_frameworks_hidden",
            field=models.BooleanField(default=False, verbose_name="Hide frameworks?"),
        ),
        migrations.AddField(
            model_name="project",
            name="is_organization_hidden",
            field=models.BooleanField(default=False, verbose_name="Hide organization?"),
        ),
        migrations.AlterField(
            model_name="project",
            name="is_hidden",
            field=models.BooleanField(
                default=False, verbose_name="Hide whole project?"
            ),
        ),
    ]
