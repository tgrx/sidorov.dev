from datetime import timedelta

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView

from applications.meta.applications.schedule.models import Event
from applications.meta.applications.schedule.utils import get_days


@method_decorator(cache_page(settings.CELERY_BEAT_CALSYNC), name="get")
class IndexView(ListView):
    template_name = "schedule/index.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__days = get_days()

    def get_queryset(self):
        start = self.__days[0].date
        end = self.__days[-1].date + timedelta(days=1)
        return Event.objects.filter(start__gte=start, end__lte=end)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx["days"] = self.__days
        ctx["actual_window"] = int(round(settings.CELERY_BEAT_CALSYNC / 60, 0))

        return ctx
