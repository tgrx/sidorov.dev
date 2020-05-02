from django.test import TestCase

from applications.meta.applications.blog.views import AllBlogPostsView
from project.utils.xtests import TemplateResponseTestMixin


class Test(TestCase, TemplateResponseTestMixin):
    def test_get(self):
        self.validate_response(
            url="/meta/blog/posts/",
            expected_view=AllBlogPostsView,
            expected_template="blog/all_posts.html",
            expected_view_name="meta:blog:all_posts",
            content_filters=(lambda _c: b"Blog" in _c,),
        )

    def test_post(self):
        self.validate_response(
            method="post",
            url="/meta/blog/posts/",
            expected_status_code=405,
            expected_view=AllBlogPostsView,
            expected_template="blog/all_posts.html",
            expected_view_name="meta:blog:all_posts",
            content_filters=(lambda _c: _c == b"",),
        )
