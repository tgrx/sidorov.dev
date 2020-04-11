from django.urls import path

from apps.meta.apps import MetaConfig
from apps.meta.views import IndexView

app_name = MetaConfig.name

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
