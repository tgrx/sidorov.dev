from django.db import IntegrityError
from django.db import transaction
from django.test import Client
from django.test import TestCase

from applications.target.models import UserInfo
from applications.target.views import IndexView


class Test(TestCase):
    def setUp(self) -> None:
        self.cli = Client()

    def test_get(self):
        resp = self.cli.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.has_header("Cache-Control"))
        self.assertEqual(resp.get("Cache-Control"), f"max-age={60 * 60 * 24}")

        self.assertEqual(resp.resolver_match.app_name, "target")
        self.assertEqual(resp.resolver_match.url_name, "index")
        self.assertEqual(resp.resolver_match.view_name, "target:index")
        self.assertEqual(
            resp.resolver_match.func.__name__, IndexView.as_view().__name__
        )

        self.assertEqual(resp.template_name, ["target/index.html"])

    def test_user_info_model(self):
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                obj = UserInfo(name=None, greeting=None, age=None)
                obj.save()

        with transaction.atomic():
            obj1 = UserInfo(name="")
            obj1.save()
            self.assertTrue(obj1.pk)
            self.assertEqual(obj1.name, "")
            self.assertEqual(str(obj1), f"{UserInfo.__name__}(id={obj1.pk}, name='')")

        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                obj2 = UserInfo(name="")
                obj2.save()
