from unittest import TestCase
import unittest
from selenium import webdriver


class NewUserTest(TestCase):
    """
    Test for a new user actions 
    """

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_starting_a_new_todo_list(self):
        """
        Test for when a user creates a new todo list
        """
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)


if __name__ == '__main__':
    unittest.main()
