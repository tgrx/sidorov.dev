from django.test import Client
from django.test import TestCase

from apps.thoughts.views import IndexView


class Test(TestCase):
    def setUp(self) -> None:
        self.cli = Client()

    def test_get(self):
        resp = self.cli.get("/thoughts/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.templates), 2)
        self.assertEqual(
            [_t.name for _t in resp.templates], ["thoughts/index.html", "base.html"]
        )
        self.assertEqual(
            resp.resolver_match.func.__name__, IndexView.as_view().__name__
        )
        self.assertTrue(resp.has_header("Cache-Control"))
        self.assertIn("max-age=0", resp.get("Cache-Control"))
