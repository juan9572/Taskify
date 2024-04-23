from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User


class CustomLoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="12345"
        )

    def test_login_view(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "12345"}
        )
        self.assertRedirects(response, reverse("tasks"))

    def test_login_incorrect_credentials(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "wrongpassword"}
        )
        path = response.request["PATH_INFO"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(path, "/user/login/")
        self.assertNotEqual(path, "")


class RegisterPageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "password1": "newpassword123",
                "password2": "newpassword123",
            },
        )
        self.assertRedirects(response, reverse("tasks"))
