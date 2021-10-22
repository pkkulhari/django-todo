import unittest
import time
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


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

        # Check title
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)

        # check header text - h1
        header = self.browser.find_element(By.TAG_NAME, 'h1')
        self.assertEqual(header.text, 'To-Do List')

        # check inputbox for new to-do
        inputbox = self.browser.find_element(By.ID, 'todo-item')
        self.assertEqual(inputbox.get_attribute(
            'placeholder'), 'Enter a to-do item')

        # add 2 new item to to-do list
        inputbox.send_keys("Go to gym")
        inputbox.send_keys(Keys.ENTER)

        time.sleep(0.01)

        inputbox = self.browser.find_element(By.ID, 'todo-item')
        inputbox.send_keys("Prepare breakfast")
        inputbox.send_keys(Keys.ENTER)

        time.sleep(0.01)

        # check for recently added items
        table = self.browser.find_element(By.ID, 'todo-items-table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(
            "1: Go to gym",
            [row.text for row in rows]
        )
        self.assertIn(
            "2: Prepare breakfast",
            [row.text for row in rows]
        )


if __name__ == '__main__':
    unittest.main()
