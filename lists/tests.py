from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page, new_list
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
        response = new_list(request)

        # Test for redirection
        self.assertEqual(response.status_code, 302)
        _list = TodoList.objects.first()
        self.assertEqual(response['Location'], f'/lists/{_list.id}/')

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


class NewListViewTest(TestCase):
    """
    Tests for create a new todo list
    """

    def test_save_data_into_database(self):
        """
        Test that new list data save in database
        """

        self.client.post('/lists/new/', {'todo-item': 'A new todo item'})
        newly_added_item = Item.objects.all()[0]
        self.assertEqual(newly_added_item.body, 'A new todo item')

    def test_post_request_redirection(self):
        """
        Test the redirection of post request for create a new todo item
        """

        response = self.client.post(
            '/lists/new/', {'todo-item': 'A new todo item'})
        self.assertEqual(response.status_code, 302)
        _list = TodoList.objects.first()
        self.assertRedirects(response, f'/lists/{_list.id}/')


class AddItemToExistingListTest(TestCase):
    """
    Tests for adding a new item to existing list
    """

    def test_add_item_to_existig_list(self):
        """
        Tests for adding a item to existing list
        """
        _list = TodoList.objects.create()
        self.client.post(
            f'/lists/{_list.id}/add/',
            {'todo-item': 'A one more item'}
        )
        newly_added_item = Item.objects.first()

        self.assertEqual(newly_added_item.list, _list)
        self.assertEqual(newly_added_item.body, 'A one more item')

    def test_post_request_redirect(self):
        """
        Test that post request redirecting user to right list page
        """
        _list = TodoList.objects.create()
        response = self.client.post(
            f'/lists/{_list.id}/add/', {'todo-item': 'A one more item'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/lists/{_list.id}/')


class ListViewTest(TestCase):
    """
    Tests for the ListView
    """

    def test_lists_page_uses_list_template(self):
        """
        Test that lists page uses list.html template
        """
        _list = TodoList.objects.create()
        response = self.client.get(f'/lists/{_list.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_items_in_todo_list(self):
        """
        Ensure that the items are displayed in todo list
        """

        # create a list and add 2 new items in list
        _list = TodoList.objects.create()
        Item.objects.create(body='Test item 1', list=_list)
        Item.objects.create(body='Test item 2', list=_list)

        # create seocnd list and add a item in it
        _list2 = TodoList.objects.create()
        Item.objects.create(body='Test item 3', list=_list2)

        # check if the item are display or not
        response = self.client.get(f'/lists/{_list.id}/')

        self.assertContains(response, 'Test item 1')
        self.assertContains(response, 'Test item 2')
        self.assertNotContains(response, 'Test item 3')

    def test_list_page_check_list_in_context(self):
        """
        Test that list page has a object of list in it's context
        """
        todoList = TodoList.objects.create()
        response = self.client.get(f'/lists/{todoList.id}/')

        self.assertEqual(response.context['list'], todoList)
