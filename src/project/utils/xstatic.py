from pathlib import Path

from django.http import Http404
from django.http import HttpResponse

from project.utils import dirs


def render_static(file_path: Path, content_type: str) -> HttpResponse:
    if not file_path.is_file():
        full_path = file_path.as_posix()
        raise Http404(f"file '{full_path}' not found")

    with file_path.open("rb") as fp:
        content = fp.read()

    response = HttpResponse(content, content_type=content_type)
    return response


def get_favicon() -> Path:
    return dirs.DIR_STATIC / "favicon2.png"
