from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.target.models import UserInfo


@admin.register(UserInfo)
class UserInfoAdminModel(ModelAdmin):
    pass
