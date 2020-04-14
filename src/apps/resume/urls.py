from django.urls import path
from django.views.generic import TemplateView

from apps.resume.apps import ResumeConfig

app_name = ResumeConfig.label

urlpatterns = [
    path("", TemplateView.as_view(template_name="resume/index.html"), name="index"),
]
