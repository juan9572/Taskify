from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from selenium.webdriver.firefox.webdriver import WebDriver


class TaskAcceptanceTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(TaskAcceptanceTest, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(TaskAcceptanceTest, cls).tearDownClass()

    def setUp(self):
        # Login
        self.user = User.objects.create_user(
            username="testuser", password="12345"
        )
        self.selenium.get(self.live_server_url)
        username_field = self.selenium.find_element(By.NAME, "username")
        password_field = self.selenium.find_element(By.NAME, "password")
        username_field.send_keys("testuser")
        password_field.send_keys("12345")
        password_field.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, 10)\
            .until(EC.url_to_be(self.live_server_url + "/"))

    def test_task_crud(self):
        selenium = self.selenium

        # Navigate to Task List
        selenium.get(self.live_server_url)

        # Create Task
        selenium.find_element(By.ID, "add-link").click()
        title_field = selenium.find_element(By.NAME, "title")
        description_field = selenium.find_element(By.NAME, "description")
        title_field.send_keys("New Task")
        description_field.send_keys("New Description")
        selenium.find_element(By.CLASS_NAME, "button").click()

        # Verify Task Created
        self.assertTrue(
            WebDriverWait(selenium, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'New Task')]")
                )
            )
        )

        # Update Task
        selenium.find_element(By.LINK_TEXT, "New Task").click()
        title_field = selenium.find_element(By.NAME, "title")
        description_field = selenium.find_element(By.NAME, "description")
        title_field.clear()
        title_field.send_keys("Updated Task")
        description_field.clear()
        description_field.send_keys("Updated Description")
        selenium.find_element(By.NAME, "complete").click()
        selenium.find_element(By.CLASS_NAME, "button").click()

        # Verify Task Updated
        self.assertTrue(
            WebDriverWait(selenium, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Updated Task')]")
                )
            )
        )

        # Delete Task
        selenium.find_element(By.LINK_TEXT, "×").click()
        selenium.find_element(By.CLASS_NAME, "button").click()

        # Verify Task Deleted
        no_tasks_message = "No hay tareas nuevas."
        add_task_link_text = "Crea una nueva "
        add_task_link_element = selenium.find_element(
            By.XPATH, f"//*[contains(text(), '{add_task_link_text}')]"
        )
        no_tasks_element = WebDriverWait(selenium, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//*[contains(text(), '{no_tasks_message}')]")
            )
        )
        self.assertTrue(no_tasks_element.is_displayed())
        self.assertTrue(add_task_link_element.is_displayed())

        # Logout
        selenium.find_element(By.CLASS_NAME, "logout-link").click()
        self.assertTrue(
            WebDriverWait(selenium, 10)\
                .until(EC.url_contains("/user/login/"))
        )
