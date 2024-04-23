from ..models import Task
from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='12345')
        Task.objects.create(user=test_user, title='Test Task', description='Test Description')

    def test_title_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_complete_default(self):
        task = Task.objects.get(id=1)
        self.assertFalse(task.complete)

    def test_str_method(self):
        task = Task.objects.get(id=1)
        self.assertEqual(str(task), task.title)

class TaskModelDeleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='12345')
        Task.objects.create(user=test_user, title='Test Task', description='Test Description')
        test_user.delete()

    def test_cascade_delete(self):
        self.assertFalse(User.objects.filter(id=1).exists())
        self.assertFalse(Task.objects.filter(id=1).exists())

class TaskUniqueModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='testuser', password='12345')
        Task.objects.create(user=cls.test_user, title='Unique Title')

    def test_unique_title(self):
        try:
            with self.assertRaises(IntegrityError):
                Task.objects.create(user=self.test_user, title='Unique Title', description='New Description')
        except IntegrityError as e:
            print(f"Caught IntegrityError: {e}")