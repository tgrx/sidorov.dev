from django.urls import include
from django.urls import path
from django.views.generic import TemplateView

from apps.meta.apps import MetaConfig

app_name = MetaConfig.label

urlpatterns = [
    path("", TemplateView.as_view(template_name="meta/index.html"), name="index"),
    path("schedule/", include("apps.meta.apps.schedule.urls")),
]
