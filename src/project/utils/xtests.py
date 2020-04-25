from typing import Callable
from typing import Collection
from typing import Dict
from typing import List
from typing import Optional

from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


class ResponseTestMixin:
    def validate_response(
        self,
        *,
        url: str,
        expected_view_name: str,
        expected_view: type,
        expected_template: str,
        method: Optional[str] = "get",
        form_data: Optional[Dict] = None,
        expected_status_code: Optional[int] = 200,
        content_filters: Optional[Collection[Callable[[bytes], bool]]] = None,
        expected_redirect_chain: Optional[List] = None,
        client: Optional = None,
    ):
        cli = client or Client()
        meth = getattr(cli, method)

        meth_args = []
        if form_data:
            meth_args.append(form_data)

        resp = meth(url, *meth_args, follow=True)
        self.assertEqual(resp.status_code, expected_status_code)

        if expected_redirect_chain is not None:
            self.assertEqual(resp.redirect_chain, expected_redirect_chain)

        self.assertEqual(resp.resolver_match.view_name, expected_view_name)
        self.assertEqual(
            resp.resolver_match.func.__name__, expected_view.as_view().__name__
        )

        self.assertIn(expected_template, resp.template_name)

        for content_filter in content_filters or []:
            self.assertTrue(content_filter(resp.content))
