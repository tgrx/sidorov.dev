from django.test import Client
from django.test import TestCase

from applications.meta.views import IndexView


class Test(TestCase):
    def setUp(self) -> None:
        self.cli = Client()

    def test_get(self):
        resp = self.cli.get("/meta/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.has_header("Cache-Control"))
        self.assertEqual(resp.get("Cache-Control"), f"max-age={60 * 60 * 24}")

        self.assertEqual(resp.resolver_match.app_name, "meta")
        self.assertEqual(resp.resolver_match.url_name, "index")
        self.assertEqual(resp.resolver_match.view_name, "meta:index")
        self.assertEqual(
            resp.resolver_match.func.__name__, IndexView.as_view().__name__
        )

        self.assertEqual(resp.template_name, ["meta/index.html"])
