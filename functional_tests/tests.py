import unittest
from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NewUserTest(LiveServerTestCase):
    """
    Test for a new user actions
    """

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_row_in_table(self, rowItem):
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '#todo-items-table tr')))

        rows = self.browser.find_elements(
            By.CSS_SELECTOR, '#todo-items-table tr')

        self.assertIn(
            rowItem,
            [row.text for row in rows]
        )

    def test_starting_a_new_todo_list(self):
        """
        Test for when a user creates a new todo list
        """

        # get url
        self.browser.get(self.live_server_url)

        # Check title
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

        self.check_row_in_table('1. Go to gym')

        inputbox = self.browser.find_element(By.ID, 'todo-item')
        inputbox.send_keys("Prepare breakfast")
        inputbox.send_keys(Keys.ENTER)

        self.check_row_in_table('1. Go to gym')
        self.check_row_in_table('2. Prepare breakfast')


if __name__ == '__main__':
    unittest.main()
