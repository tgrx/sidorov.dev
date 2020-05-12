from unittest import TestCase
from unittest.mock import patch

from project.utils import xmail


class Test(TestCase):
    @patch.object(xmail, xmail.send_mail.__name__)
    def test_send_email(self, mock_send_mail):
        xmail.send_email(
            email_to="test@example.com", subject="x", mail_template_name="invitation",
        )

        mock_send_mail.assert_called_once()
