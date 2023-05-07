from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import CreationForm

User = get_user_model()


class CreationFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create()
        cls.form = CreationForm()

    def setUp(self):
        self.guest_client = Client()

    def test_signup(self):
        """Валидная форма создает нового пользователя."""
        users_count = User.objects.count()
        form_data = {
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': 'test_username',
            'email': 'test_email@yandex.ru',
            'password1': 'test_password_23',
            'password2': 'test_password_23',
        }
        response = self.guest_client.post(
            reverse('users:signup'), data=form_data, follow=True
        )
        self.assertRedirects(response, reverse('posts:index'))
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertTrue(User.objects.filter(username='test_username').exists())
        self.assertEqual(response.status_code, HTTPStatus.OK)
