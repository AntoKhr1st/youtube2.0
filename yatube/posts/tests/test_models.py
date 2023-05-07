from django.test import TestCase

from ..models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def setUp(self):
        self.post = PostModelTest.post
        self.group = PostModelTest.group

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        vals = (
            (str(self.post), self.post.text[:15]),
            (str(self.group), self.group.title),
        )
        for value, expected in vals:
            with self.subTest(value=value):
                self.assertEqual(value, expected)

    def test_verbose_name(self):
        """Проверяем, что у моделей корректно работает verbose_name."""
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.post._meta.get_field(value).verbose_name, expected
                )

    def test_help_text(self):
        """Проверяем, что у моделей корректно работает help_text."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(post._meta.get_field(value).help_text,
                                 expected)
