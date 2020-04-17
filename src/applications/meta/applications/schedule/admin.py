from django import forms
from django.contrib import admin
from django.db import models

from applications.meta.applications.schedule.models import Calendar
from project.utils.xmodels import a


class CalendarModelAdminForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = "__all__"
        widgets = {
            a(Calendar.ical): forms.Textarea(
                attrs={"cols": 100, "disabled": 1, "rows": 3,}
            ),
            a(Calendar.description): forms.Textarea(attrs={"cols": 100, "rows": 3,}),
        }


@admin.register(Calendar)
class CalendarModelAdmin(admin.ModelAdmin):
    form = CalendarModelAdminForm
    formfield_overrides = {models.TextField: {"widget": forms.TextInput}}
