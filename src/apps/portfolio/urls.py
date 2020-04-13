from django.urls import path
from django.views.generic import TemplateView

from apps.portfolio.apps import PortfolioConfig

app_name = PortfolioConfig.label

urlpatterns = [
    path("", TemplateView.as_view(template_name="portfolio/index.html"), name="index"),
]
