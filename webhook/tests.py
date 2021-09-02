from django.test import TestCase

from telegram_bot.core.telegram_context import TelegramContext
from telegram_bot.keyboard import BotKeyboard
from telegram_bot.router import ReFormat, Router
from telegram_bot.user import User
from telegram_bot.views import welcome, select_category
from webhook.models import TelegramUser, TelegramMessage


class KeyboardMock:
    def main(self):
        return

    def categories(self, categories_list):
        return


class UserMock:
    def save_state(self, new_state=None):
        pass


class BotMock:
    keyboard = BotKeyboard(TelegramContext('token'))
    text_message = None
    user = UserMock()

    def send_message(self, text, keyboard):
        self.text_message = text


class UpdateMock:
    data = {
        'message':
            {
                'message_id': 0,
                'user':
                    {
                        'id': 0,
                        'first_name': 'test_first_name',
                        'last_name': 'test_last_name',
                        'username': 'test_username'
                    },
                'text': 'TEST'
            }
    }


class ViewsTest(TestCase):

    def setUp(self) -> None:
        self.bot = BotMock()

    def test_welcome(self):
        welcome(self.bot)
        text_message = self.bot.text_message
        self.assertEqual("%ПРИВЕТСТВИЕ%", text_message)

    def test_select_categories(self):
        select_category(self.bot)
        text_message = self.bot.text_message
        self.assertEqual("Выберите категорию упражнений", text_message)


class UserModelTest(TestCase):
    def setUp(self) -> None:
        self.update = UpdateMock()

    def test_init_from_update(self):
        user = User(self.update)
        user.init_from_update()
        self.assertEqual(0, user.id)
        self.assertEqual('test', user.request)
        self.assertEqual(self.update, user.update)
        self.assertEqual('/', user.state)
        self.assertEqual(True, user.initialized)
        tg_message = TelegramMessage.objects.get(id=1)
        self.assertEqual('TEST', tg_message.text)
        tg_user = TelegramUser.objects.get(id=0)
        self.assertEqual('test_first_name', tg_user.first_name)
        self.assertEqual('test_last_name', tg_user.last_name)
        self.assertEqual('test_username', tg_user.username)

    def test_update_from_db(self):
        user = User(self.update)
        user.init_from_update()
        user.initialized = False
        user.init_from_db()
        self.assertEqual(0, user.id)
        self.assertEqual('test', user.request)
        self.assertEqual(self.update, user.update)
        self.assertEqual('/', user.state)
        self.assertEqual(True, user.initialized)

    def test_save_state(self):
        user = User(self.update)
        user.init_from_update()
        user.save_state('/тестовое состояние')
        tg_user = TelegramUser.objects.get(id=0)
        self.assertEqual('/тестовое состояние', tg_user.state)


class RouterTest(TestCase):
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
        self.assertEqual(re_url_5,
                         '(?P<parameter>\+?(375|80|0)?\(?[0]?(?<tcode>\d{2})\)?(?<tphone>\d{3}[-\s]*\d{2}[-\s]*\d{2}))')
        re_url_6 = reformat.re_url('<email:parameter>')
        self.assertEqual(re_url_6, '(?P<parameter>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+.+.[a-zA-Z]{2,4})')
        re_url_7 = reformat.re_url('<re:parameter>')
        self.assertEqual(re_url_7, '<re:parameter>')

    def test_router_init(self):
        router = Router(self.urls)
        self.assertEqual('start', router.static_urls['/start'])
        self.assertEqual('test', router.static_urls['/test'])
        self.assertEqual(('(?P<req>.*)/start', 'dinamyc_start'), router.dynamic_urls[0])
