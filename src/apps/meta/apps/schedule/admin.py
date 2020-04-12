from django.contrib import admin

from apps.meta.apps.schedule.models import GoogleCredentials


@admin.register(GoogleCredentials)
class GoogleCredentialsModelAdmin(admin.ModelAdmin):
    pass
