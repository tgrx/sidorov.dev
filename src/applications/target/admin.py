from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from applications.target.models import UserInfo


class UserInfoAdminForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = "__all__"
        widgets = {"name": forms.TextInput()}


@admin.register(UserInfo)
class UserInfoAdminModel(ModelAdmin):
    form = UserInfoAdminForm
