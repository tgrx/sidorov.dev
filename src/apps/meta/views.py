from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView

from project.utils.consts import AGE_1DAY


@method_decorator(cache_control(max_age=AGE_1DAY), name="get")
class IndexView(TemplateView):
    template_name = "meta/index.html"
