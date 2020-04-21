# Generated by Django 3.0.5 on 2020-04-20 23:12

import django.db.models.deletion
import django.db.models.expressions
from django.db import migrations
from django.db import models

import project.utils.xdatetime


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Framework",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                ("version", models.TextField(blank=True, null=True)),
                ("link", models.TextField(blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={"ordering": ("name",),},
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(unique=True)),
                ("link", models.TextField(blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={"ordering": ("name",),},
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                (
                    "is_hidden",
                    models.BooleanField(default=False, verbose_name="Hidden?"),
                ),
                (
                    "is_under_nda",
                    models.BooleanField(default=False, verbose_name="Under NDA?"),
                ),
                (
                    "nda_name",
                    models.TextField(
                        blank=True, null=True, verbose_name="Name under NDA"
                    ),
                ),
                (
                    "nda_organization_name",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="Organization Name under NDA",
                    ),
                ),
                ("position", models.TextField(blank=True, null=True)),
                (
                    "started_at",
                    models.DateField(default=project.utils.xdatetime.utcnow),
                ),
                ("finished_at", models.DateField(blank=True, null=True)),
                ("link", models.TextField(blank=True, null=True)),
                ("summary", models.TextField(blank=True, null=True)),
                ("responsibilities_text", models.TextField(blank=True, null=True)),
                ("achievements_text", models.TextField(blank=True, null=True)),
                (
                    "frameworks",
                    models.ManyToManyField(
                        related_name="projects", to="resume.Framework"
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projects",
                        to="resume.Organization",
                    ),
                ),
            ],
            options={
                "ordering": (
                    django.db.models.expressions.OrderBy(
                        django.db.models.expressions.F("finished_at"),
                        descending=True,
                        nulls_last=False,
                    ),
                    "-started_at",
                    "name",
                ),
            },
        ),
        migrations.AddConstraint(
            model_name="framework",
            constraint=models.UniqueConstraint(
                fields=("name", "version"), name="unique_name_version_v01"
            ),
        ),
    ]