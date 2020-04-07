from django.urls import path

from apps.portfolio.apps import PortfolioConfig
from apps.portfolio.views import view_index

app_name = PortfolioConfig.name

urlpatterns = [
    path("", view_index, name="index"),
]
