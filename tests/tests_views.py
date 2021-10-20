from django.test import TestCase
from django.utils.safestring import SafeString

from telegram_bot.views import welcome, select_category
from tests.conftest import BotMock
from webhook.models import Category


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