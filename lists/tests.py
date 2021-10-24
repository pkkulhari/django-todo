from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item, TodoList


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

    def test_home_page_persist_todos(self):
        "Test that To-Dos are persisted after form submission"

        request = HttpRequest()
        request.method = 'POST'
        request.POST['todo-item'] = 'A new item'
        response = home_page(request)

        # Test for redirection
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')

        # check the item in database
        item = Item.objects.first()
        self.assertEqual(item.body, 'A new item')


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
        _list = TodoList()
        _list.save()

        first_item = Item()
        first_item.body = 'First Item'
        first_item.list = _list
        first_item.save()

        second_item = Item()
        second_item.body = 'Second Item'
        second_item.list = _list
        second_item.save()

        fetched_items = Item.objects.values_list('body')

        self.assertEqual('First Item', fetched_items[0][0])
        self.assertEqual('Second Item', fetched_items[1][0])
        self.assertEqual(first_item.list, _list)
        self.assertEqual(second_item.list, _list)
