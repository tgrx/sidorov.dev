from unittest import TestCase
from unittest.mock import patch

from project.utils import safeguards
from project.utils.safeguards import safe


class Test(TestCase):
    @patch.object(safeguards, safeguards.capture_exception.__name__)
    def test_safe(self, mock_capture_exception):
        exc = AssertionError("xxx")

        def _error():
            raise exc

        _safe = safe(_error)

        ret = _safe()
        self.assertIsNone(ret)
        mock_capture_exception.assert_called_once_with(exc)
