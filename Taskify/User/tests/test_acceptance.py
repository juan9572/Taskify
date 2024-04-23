from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from selenium.webdriver.chrome.webdriver import WebDriver


class UserAuthenticationTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(UserAuthenticationTest, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(UserAuthenticationTest, cls).tearDownClass()

    def setUp(self):
        self.selenium.get(self.live_server_url)

    def test_user_registration(self):
        selenium = self.selenium

        # Navigate to Registration Page
        selenium.find_element(By.LINK_TEXT, "Registrate").click()

        # Register
        username_field = selenium.find_element(By.NAME, "username")
        password1_field = selenium.find_element(By.NAME, "password1")
        password2_field = selenium.find_element(By.NAME, "password2")
        username_field.send_keys("newuser")
        password1_field.send_keys("newpasswordHiperSecret123")
        password2_field.send_keys("newpasswordHiperSecret123")
        password2_field.send_keys(Keys.RETURN)

        # Verify Successful Registration
        self.assertTrue(
            WebDriverWait(selenium, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Hola Newuser')]")
                )
            )
        )
        self.assertTrue(
            WebDriverWait(selenium, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "logout-link")
                )
            )
        )
        user_exists = User.objects.filter(username="newuser").exists()
        self.assertTrue(user_exists)

    def test_user_login(self):
        selenium = self.selenium
        User.objects.create_user(
            username="newuser", password="newpasswordHiperSecret123"
        )

        # Login
        username_field = selenium.find_element(By.NAME, "username")
        password_field = selenium.find_element(By.NAME, "password")
        username_field.send_keys("newuser")
        password_field.send_keys("newpasswordHiperSecret123")
        password_field.send_keys(Keys.RETURN)

        # Verify Successful Login
        self.assertTrue(
            WebDriverWait(selenium, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Hola Newuser')]")
                )
            )
        )
        self.assertTrue(
            WebDriverWait(selenium, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "logout-link")
                )
            )
        )
