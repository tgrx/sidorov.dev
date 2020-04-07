from django.urls import path

from apps.thoughts.apps import ThoughtsConfig
from apps.thoughts.views import view_index

app_name = ThoughtsConfig.name

urlpatterns = [
    path("", view_index, name="index"),
]
