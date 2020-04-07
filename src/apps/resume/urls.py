from django.urls import path

from apps.resume.apps import ResumeConfig
from apps.resume.views import view_index

app_name = ResumeConfig.name

urlpatterns = [
    path("", view_index, name="index"),
]
