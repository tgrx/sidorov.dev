import functools

from django.conf import settings
from sentry_sdk import capture_exception


def safe(func):
    if settings.DEBUG:
        return func

    @functools.wraps(func)
    def _safe_func(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as err:
            capture_exception(err)

        return result

    return _safe_func
