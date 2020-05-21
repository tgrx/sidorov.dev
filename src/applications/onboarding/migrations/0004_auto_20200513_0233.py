# Generated by Django 3.0.5 on 2020-05-12 23:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("onboarding", "0003_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="authprofile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                related_name="auth_profile",
                serialize=False,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]