from django.contrib.postgres.fields import JSONField
from django.db import models as m


class GoogleCredentials(m.Model):
    client_secrets = JSONField(null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "Google Credentials"
