from pathlib import Path

from django.conf import settings
from django.http import Http404
from django.http import HttpResponse

from project.utils import consts

STATIC_DIR = settings.PROJECT_DIR / "static"


def render_static(file_path: Path, content_type: str) -> HttpResponse:
    if not file_path.is_file():
        full_path = file_path.as_posix()
        raise Http404(f"file '{full_path}' not found")

    with file_path.open("rb") as fp:
        content = fp.read()

    response = HttpResponse(content, content_type=content_type)
    return response


def get_theme_css(hour: int) -> Path:
    css = "theme_light.css" if (hour in consts.DAYLIGHT) else "theme_dark.css"
    css_path = STATIC_DIR / "css" / css
    return css_path


def get_favicon() -> Path:
    return STATIC_DIR / "favicon.png"
