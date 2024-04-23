import os
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from playwright.sync_api import sync_playwright, expect


class TaskAcceptanceTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super(TaskAcceptanceTest, cls).setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()


    @classmethod
    def tearDownClass(cls):
        super(TaskAcceptanceTest, cls).tearDownClass()
        cls.browser.close()
        cls.playwright.stop()


    def test_task_crud(self):
        self.user = User.objects.create_user(
            username="testuser", password="12345passwordHiper"
        )
        page = self.browser.new_page()
        page.goto(self.live_server_url)

        page.locator("#id_username").fill("testuser")
        page.locator("#id_password").fill("12345passwordHiper")
        page.get_by_role("button", name="Logueate").click()
        expect(page.get_by_role("heading", name="Hola Testuser")).to_be_visible()
        page.get_by_role("link", name="tarea").click()

        # Create Task
        page.locator("#id_title").fill("New Task")
        page.locator("#id_description").fill("New Description")
        page.get_by_role("button", name="Guardar").click()

        # Verify Task Created
        expect(page.locator("#tasklist")).to_contain_text("New Task")
        expect(page.locator("h3")).to_contain_text("Tienes 1 tarea incompleta")

        # Update Task
        page.get_by_role("link", name="New Task").click()
        page.locator("#id_title").fill("Updated Task")
        page.locator("#id_description").fill("Updated Description")
        page.locator("#id_complete").check()
        page.get_by_role("button", name="Guardar").click()

        # Verify Task Updated
        expect(page.locator("h3")).to_contain_text("Tienes 0 tareas incompletas")
        expect(page.locator("#tasklist")).to_contain_text("Updated Task")

        # Delete Task
        page.get_by_role("link", name="×").click()
        page.get_by_role("button", name="Eliminar").click()

        # Verify Task Deleted
        expect(page.locator("#tasklist")).to_contain_text("No hay tareas nuevas.")
        expect(page.locator("#tasklist")).to_contain_text("Crea una nueva tarea !")

        # Logout
        page.get_by_role("button", name="Cerrar sesión").click()
        page.close()
