from django.test import TestCase

from applications.resume.views import IndexView
from project.utils.xtests import ResponseTestMixin


class Test(TestCase, ResponseTestMixin):
    def test_get(self):
        self.validate_response(
            url="/resume/",
            expected_view=IndexView,
            expected_view_name="resume:index",
            expected_template="resume/index.html",
        )
