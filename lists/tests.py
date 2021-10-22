from django.test import TestCase
from django.http import HttpRequest, request, response

from lists.views import home_page
from lists.models import Item


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



class ItemModelTest(TestCase):
    """
    Tests for Item model
    """

    def test_insert_and_fetch_item_from_database(self):
        """
        Tests -
        1. Insert two items into database
        2. Fetch both items from database
        """

        fist_item = Item()
        fist_item.body = 'First Item'
        fist_item.save()

        second_item = Item()
        second_item.body = 'Second Item'
        second_item.save()

        fetched_items = Item.objects.values_list('body')

        self.assertEqual('First Item', fetched_items[0][0])
        self.assertEqual('Second Item', fetched_items[1][0])
