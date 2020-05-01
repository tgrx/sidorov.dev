from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "meta/_meta.html"
