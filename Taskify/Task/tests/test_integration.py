from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Task

class TaskIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.task = Task.objects.create(user=self.user, title='Test Task', description='Test Description')

    def test_task_list_view(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_create_view(self):
        response = self.client.post(reverse('task-create'), {'title': 'New Task', 'description': 'New Description', 'complete': False})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_task_update_view(self):
        response = self.client.post(reverse('task-update', args=[self.task.id]), {'title': 'Updated Task', 'description': 'Updated Description', 'complete': True})
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_task_delete_view(self):
        response = self.client.post(reverse('task-delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_task_create_invalid_data(self):
        self.client.post(reverse('task-create'), {'title': '', 'description': 'New Description', 'complete': False})
        self.assertFalse(Task.objects.filter(title='').exists())

        long_description = 'Lorem Ipsum es simplemente el texto de relleno de las imprentas y archivos de texto. Lorem Ipsum ha sido el texto de relleno estándar de las industrias desde el año 1500, cuando un impresor (N. del T. persona que se dedica a la imprenta) desconocido usó una galería de textos y los mezcló de tal manera que logró hacer un libro de textos especimen. No sólo sobrevivió 500 años, sino que tambien ingresó como texto de relleno en documentos electrónicos, quedando esencialmente igual al original. Fue popularizado en los 60s con la creación de las hojas "Letraset", las cuales contenian pasajes de Lorem Ipsum, y más recientemente con software de autoedición, como por ejemplo Aldus PageMaker, el cual incluye versiones de Lorem Ipsum.'
        self.client.post(reverse('task-create'), {'title': 'Valid Title', 'description': long_description, 'complete': False})
        self.assertFalse(Task.objects.filter(title='Valid Title').exists())

class TaskIntegrationExtremeCasesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(username='owner', password='12345')
        self.non_owner = User.objects.create_user(username='non_owner', password='12345')
        self.task = Task.objects.create(user=self.owner, title='Test Task', description='Test Description')
        self.client.login(username='non_owner', password='12345')

    def test_task_update_by_non_owner(self):
        self.client.post(reverse('task-update', args=[self.task.id]), {'title': 'Updated Task', 'description': 'Updated Description', 'complete': True})
        self.task.refresh_from_db()
        self.assertNotEqual(self.task.title, 'Updated Task')
        self.assertNotEqual(self.task.description, 'Updated Description')
        self.assertFalse(self.task.complete)