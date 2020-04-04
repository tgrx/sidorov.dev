from django.test import Client
from django.test import TestCase

from project.urls import view_thoughts


class Test(TestCase):
    def setUp(self) -> None:
        self.cli = Client()

    def test_get(self):
        resp = self.cli.get("/thoughts/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.templates), 2)
        self.assertEqual(
            [_t.name for _t in resp.templates], ["thoughts.html", "base.html"]
        )
        self.assertEqual(resp.resolver_match.func, view_thoughts)
