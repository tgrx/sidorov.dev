from django.test import TestCase

from applications.target.views import IndexView
from project.utils.xtests import ResponseTestMixin


class Test(TestCase, ResponseTestMixin):
    def test_get(self):
        self.validate_response(
            url="/",
            expected_view_name="target:index",
            expected_view=IndexView,
            expected_template="target/index.html",
        )
