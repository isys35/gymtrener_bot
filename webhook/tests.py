from django.test import TestCase

from telegram_bot.views import welcome


class KeyboardMock:
    def main(self):
        return


class BotMock:
    keyboard = KeyboardMock()
    text_message = None

    def send_message(self, text, keyboard):
        self.text_message = text


class WelcomeViewTest(TestCase):

    def setUp(self) -> None:
        self.bot = BotMock()

    def test_welcome(self):
        welcome(self.bot)
        text_message = self.bot.text_message
        self.assertEqual("Привет мир", text_message)
