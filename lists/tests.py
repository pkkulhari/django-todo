from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page


class TestHomePage(TestCase):
    """
    Tests for Home Page
    """

    def test_home_page_is_loading_right_template(self):
        """
        Test, it is loading right page
        """
        request = HttpRequest()
        response = home_page(request)

        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do Lists</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))
