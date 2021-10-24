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

        # Check title
        self.browser.get(self.live_server_url)
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

        # Get th first user's browser's url and test it for correct url
        first_user_browser_url = self.browser.current_url
        self.assertRegex(first_user_browser_url, '/lists/only-one-list')

        self.browser.quit()

        # => Now, a second user comes and create a new todo list
        self.browser = webdriver.Firefox()

        # check if second user get his own unique URL
        second_url_browsr_url = self.browser.current_url
        self.assertRegex(second_url_browsr_url, '/lists/.+')

        # Check title
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)

        # check header text - h1
        header = self.browser.find_element(By.TAG_NAME, 'h1')
        self.assertEqual(header.text, 'To-Do List')

        # check if first user's content(todo list) is not in second user's browser
        tabel = self.browser.find_element(By.TAG_NAME, 'tabel')
        self.assertNotIn('1. Go to gye', tabel)
        self.assertNotIn('2. Prepare breakfast', tabel)

        # Ensure that first user's url and seocond user's url are not same
        self.assertNotEqual(first_user_browser_url, second_url_browsr_url)

        # add new item to todo list
        inputbox = self.browser.find_element(By.ID, 'todo-item')
        inputbox.send_keys("1. Buy books")
        inputbox.send_keys(Keys.ENTER)

        self.check_row_in_table('1. Buy books')


if __name__ == '__main__':
    unittest.main()
