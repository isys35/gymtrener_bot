from django.test import TestCase
from django.utils.safestring import SafeString

from telegram_bot.views import welcome
from tests.conftest import BotMock


class WelcomeTest(TestCase):

    def setUp(self) -> None:
        self.bot = BotMock()

    def test_welcome(self):
        welcome(self.bot)
        text_message = self.bot.text_message
        self.assertEqual(SafeString, type(text_message))
        self.assertEqual('/', self.bot.user.state)