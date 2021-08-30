from django.test import TestCase

from telegram_bot.router import ReFormat, Router
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


class RouterTests(TestCase):
    def setUp(self) -> None:
        self.urls = [
            (r'/start', 'start'),
            (r'/test', 'test'),
            (r'<wc:req>/start', 'dinamyc_start')
                     ]

    def test_reformat(self):
        reformat = ReFormat()
        re_url_1 = reformat.re_url('<str:parameter>')
        self.assertEqual(re_url_1, '(?P<parameter>[^/]+)')
        re_url_2 = reformat.re_url('<wc:parameter>')
        self.assertEqual(re_url_2, '(?P<parameter>.*)')
        re_url_3 = reformat.re_url('<int:parameter>')
        self.assertEqual(re_url_3, '(?P<parameter>[0-9]+)')
        re_url_4 = reformat.re_url('<float:parameter>')
        self.assertEqual(re_url_4, '(?P<parameter>[0-9]+[.,]?[0-9]+)')
        re_url_5 = reformat.re_url('<phone:parameter>')
        self.assertEqual(re_url_5, '(?P<parameter>\+?(375|80|0)?\(?[0]?(?<tcode>\d{2})\)?(?<tphone>\d{3}[-\s]*\d{2}[-\s]*\d{2}))')
        re_url_6 = reformat.re_url('<email:parameter>')
        self.assertEqual(re_url_6, '(?P<parameter>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+.+.[a-zA-Z]{2,4})')
        re_url_7 = reformat.re_url('<re:parameter>')
        self.assertEqual(re_url_7, '<re:parameter>')

    def test_router_init(self):
        router = Router(self.urls)
        self.assertEqual('start', router.static_urls['/start'])
        self.assertEqual('test', router.static_urls['/test'])
        self.assertEqual(('(?P<req>.*)/start', 'dinamyc_start'), router.dynamic_urls[0])