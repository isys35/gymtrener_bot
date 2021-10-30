from django.test import TestCase
from django.utils.safestring import SafeString

from telegram_bot.views import welcome, select_category, select_exercise
from tests.conftest import BotMock
from webhook.models import Category, Exersice


class WelcomeTest(TestCase):

    def setUp(self) -> None:
        self.bot = BotMock()

    def test_welcome(self):
        welcome(self.bot)
        text_message = self.bot.text_message
        self.assertEqual(SafeString, type(text_message))
        self.assertEqual('/', self.bot.user.state)


class SelectCategoryTest(TestCase):

    def setUp(self) -> None:
        self.bot = BotMock()

    def test_select_category(self):
        select_category(self.bot)
        text_message = self.bot.text_message
        self.assertEqual(str, type(text_message))
        self.assertEqual('/', self.bot.user.state)
        category = Category(title='Грудь')
        category.save()
        select_category(self.bot)
        self.assertEqual(str, type(text_message))
        self.assertEqual('/выбрать упражнение', self.bot.user.state)


class SelectExerciseTest(TestCase):

    def setUp(self):
        self.bot = BotMock()
        self.category = Category(title='Грудь')
        self.category.save()

    def test_select_exercise(self):
        select_exercise(self.bot, category='грудь')
        self.assertEqual('/выбрать упражнение', self.bot.user.state)

        exercise = Exersice(title='Упражнение', category=self.category)
        exercise.save()
        select_exercise(self.bot, category='грудь')
        self.assertEqual('/выбрать упражнение/грудь/1', self.bot.user.state)