from django.test import TestCase

from telegram_bot.user import User
from telegram_bot.views import welcome


class KeyboardMock:
    def main(self):
        return


class BotMock:
    keyboard = KeyboardMock()
    text_message = None

    def send_message(self, text, keyboard):
        self.text_message = text


class UpdateMock:
    data = {'message': {'user': {'id': 0}, 'text': 'TEST'}}


class WelcomeViewTest(TestCase):

    def setUp(self) -> None:
        self.bot = BotMock()

    def test_welcome(self):
        welcome(self.bot)
        text_message = self.bot.text_message
        self.assertEqual("Привет мир", text_message)


class UserModelTest(TestCase):
    def setUp(self) -> None:
        self.update = UpdateMock()

    def test_init_from_update(self):
        user = User(self.update)
        user.init_from_update()
        self.assertEqual(0, user.id)
        self.assertEqual('TEST', user.full_request)
        self.assertEqual(self.update, user.update)
        self.assertEqual('/', user.state)
