from django.urls import path

from apps.target.apps import TargetConfig
from apps.target.views import view_index

app_name = TargetConfig.name

urlpatterns = [
    path("", view_index, name="index"),
]
