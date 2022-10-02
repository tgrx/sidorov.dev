from pathlib import Path

_this_file = Path(__file__).resolve()

DIR_REPO = _this_file.parent.parent.parent.parent.resolve()

DIR_SRC = (DIR_REPO / "src").resolve()
assert DIR_SRC.is_dir()

DIR_PROJECT = (DIR_SRC / "project").resolve()
assert DIR_PROJECT.is_dir()

DIR_STATIC = DIR_PROJECT / "static"
assert DIR_STATIC.is_dir()
