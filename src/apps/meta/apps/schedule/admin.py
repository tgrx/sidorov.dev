from django import forms
from django.contrib import admin
from django.db import models

from apps.meta.apps.schedule.models import Calendar
from project.utils.xmodels import a


class CalendarModelAdminForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = "__all__"
        widgets = {
            a(Calendar.ical): forms.Textarea(attrs={"rows": 3, "cols": 100}),
            a(Calendar.description): forms.Textarea(attrs={"rows": 3, "cols": 100}),
        }


@admin.register(Calendar)
class CalendarModelAdmin(admin.ModelAdmin):
    form = CalendarModelAdminForm
    formfield_overrides = {models.TextField: {"widget": forms.TextInput}}
    readonly_fields = [a(f) for f in (Calendar.ical,)]
