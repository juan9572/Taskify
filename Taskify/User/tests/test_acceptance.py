import os
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from playwright.sync_api import sync_playwright, expect


class UserAuthenticationTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super(UserAuthenticationTest, cls).setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        super(UserAuthenticationTest, cls).tearDownClass()
        cls.browser.close()
        cls.playwright.stop()


    def test_user_registration(self):
        page = self.browser.new_page()
        page.goto(self.live_server_url)
        # Navigate to Registration Page
        page.get_by_role("link", name="Registrate").click()

        # Register
        page.locator("#id_username").fill("newuser")
        page.locator("#id_password1").fill("newpasswordHiperSecret123")
        page.locator("#id_password2").fill("newpasswordHiperSecret123")
        page.get_by_role("button", name="Registrarse").click()

        # Verify Successful Registration
        expect(page.locator("h1")).to_contain_text("Hola Newuser")
        expect(page.get_by_role("button", name="Cerrar sesión")).to_be_visible()
        user_exists = User.objects.filter(username="newuser").exists()
        self.assertTrue(user_exists)

    def test_user_login(self):
        page = self.browser.new_page()
        page.goto(self.live_server_url)
        User.objects.create_user(
            username="newuser", password="newpasswordHiperSecret123"
        )

        # Login
        page.locator("#id_username").fill("newuser")
        page.locator("#id_password").fill("newpasswordHiperSecret123")
        page.get_by_role("button", name="Logueate").click()

        # Verify Successful Login
        expect(page.locator("h1")).to_contain_text("Hola Newuser")
        expect(page.get_by_role("button", name="Cerrar sesión")).to_be_visible()
