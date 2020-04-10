from pathlib import Path
from unittest import TestCase

from project.utils.xstatic import get_favicon


class Test(TestCase):
    def test_get_favicon(self):
        ret = get_favicon()
        self.assertIsInstance(ret, Path)
        self.assertTrue(ret.is_file())
        self.assertEqual(ret.name, "favicon.png")
