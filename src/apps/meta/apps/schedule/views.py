from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView


@method_decorator(never_cache, name="get")
class IndexView(TemplateView):
    template_name = "schedule/index.html"


class OAuth2CallbackView(View):
    pass
