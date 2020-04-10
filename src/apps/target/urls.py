from django.urls import path

from apps.target.apps import TargetConfig
from apps.target.views import IndexView

app_name = TargetConfig.name

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
