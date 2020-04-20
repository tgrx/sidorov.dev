from django.contrib import admin
from django.contrib.admin import ModelAdmin

from applications.resume.models import Project
from applications.resume.models import Technology


# class UserInfoAdminForm(forms.ModelForm):
#     class Meta:
#         model = UserInfo
#         fields = "__all__"
#         widgets = {"name": forms.TextInput()}


@admin.register(Technology)
class TechnologyAdminModel(ModelAdmin):
    # form = UserInfoAdminForm
    pass


@admin.register(Project)
class ProjectAdminModel(ModelAdmin):
    pass
