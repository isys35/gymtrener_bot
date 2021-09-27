# from django.test import TestCase
# from django.utils.safestring import SafeString
#
# from telegram_bot.core.telegram_context import TelegramContext
# from telegram_bot.handlers.handlers import UpdateHandler
# from telegram_bot.keyboard import BotKeyboard
# from telegram_bot.router import ReFormat, Router
# from telegram_bot.user import User
# from telegram_bot.views import welcome, select_category, select_exercise, next_page_exercise, previos_page_exercis, \
#     exercise_use
# from webhook.models import TelegramUser, TelegramMessage, Exersice, Category
#
#
# class ViewsTest(TestCase):
#
#     def setUp(self) -> None:
#         self.bot = BotMock()
#
#     def test_welcome(self):
#         welcome(self.bot)
#         text_message = self.bot.text_message
#         self.assertEqual(SafeString, type(text_message))
#         self.assertEqual('/', self.bot.user.state)
#
#     def test_select_categories(self):
#         select_category(self.bot)
#         text_message = self.bot.text_message
#         self.assertEqual("В базе нету упражнений 😔", text_message)
#         self.assertEqual("/выбрать упражнение", self.bot.user.state)
#
#     def test_select_exercises(self):
#         select_exercise(self.bot, 'грудь')
#         text_message = self.bot.text_message
#         self.assertEqual("В базе нету упражнений 😔", text_message)
#         self.assertEqual("/выбрать упражнение", self.bot.user.state)
#         Category.objects.create(title='грудь')
#         Exersice.objects.create(title='Жим', category_id=1, description='Описание')
#         select_exercise(self.bot, 'грудь')
#         text_message = self.bot.text_message
#         self.assertEqual(SafeString, type(text_message))
#         self.assertEqual("/выбрать упражнение/грудь/1", self.bot.user.state)
#
#     def test_next_page_exercise(self):
#         self.bot.user.request = 'следующая страница'
#         next_page_exercise(self.bot, category='грудь', page_number=1)
#         self.assertEqual("/", self.bot.user.state)
#         self.assertEqual("В базе нету упражнений 😔", self.bot.text_message)
#         Category.objects.create(title='грудь')
#         exercises = [Exersice(title=f'Жим {i}', category_id=1, description='Описание') for i in range(30)]
#         Exersice.objects.bulk_create(exercises)
#         next_page_exercise(self.bot, category='грудь', page_number=1)
#         self.assertIn('Жим 7', str(self.bot.text_message))
#         self.assertIn('Жим 8', str(self.bot.text_message))
#         self.assertIn('Жим 9', str(self.bot.text_message))
#
#     def test_previos_page_exercis(self):
#         self.bot.user.request = 'следующая страница'
#         previos_page_exercis(self.bot, category='грудь', page_number=2)
#         self.assertEqual("/", self.bot.user.state)
#         self.assertEqual("В базе нету упражнений 😔", self.bot.text_message)
#         Category.objects.create(title='грудь')
#         exercises = [Exersice(title=f'Жим {i}', category_id=1, description='Описание') for i in range(30)]
#         Exersice.objects.bulk_create(exercises)
#         previos_page_exercis(self.bot, category='грудь', page_number=3)
#         self.assertIn('Жим 7', str(self.bot.text_message))
#         self.assertIn('Жим 8', str(self.bot.text_message))
#         self.assertIn('Жим 9', str(self.bot.text_message))
#
#     def test_exercise_info(self):
#         Category.objects.create(title='грудь')
#         Category.objects.create(title='грудь 2')
#         category = Category.objects.create(title='грудь 3')
#         exercise = Exersice.objects.create(title='Жим 1', category=category, description='Описание')
#         exercise = Exersice.objects.create(title='Жим 2', category=category, description='Описание')
#         exercise = Exersice.objects.create(title='Жим 3', category=category, description='Описание')
#         TelegramUser.objects.create(first_name='first_name', last_name='last_name', username='username')
#         self.bot.user.id = 1
#         exercise_use(self.bot, exercise_id='3')
#         self.assertEqual(f"/exercise_use/3/1", self.bot.user.state)
#         self.assertEqual(SafeString, type(self.bot.text_message))
#
#
# class UserModelTest(TestCase):
#     def setUp(self) -> None:
#         self.update = UpdateMockMessage()
#
#     def test_init_from_update(self):
#         user = User(self.update)
#         user.init_from_update()
#         self.assertEqual(0, user.id)
#         self.assertEqual('test', user.request)
#         self.assertEqual(self.update, user.update)
#         self.assertEqual('/', user.state)
#         self.assertEqual(True, user.initialized)
#         tg_message = TelegramMessage.objects.get(id=1)
#         self.assertEqual('TEST', tg_message.text)
#         tg_user = TelegramUser.objects.get(id=0)
#         self.assertEqual('test_first_name', tg_user.first_name)
#         self.assertEqual('test_last_name', tg_user.last_name)
#         self.assertEqual('test_username', tg_user.username)
#
#     def test_update_from_db(self):
#         user = User(self.update)
#         user.init_from_update()
#         user.initialized = False
#         user.init_from_db()
#         self.assertEqual(0, user.id)
#         self.assertEqual('test', user.request)
#         self.assertEqual(self.update, user.update)
#         self.assertEqual('/', user.state)
#         self.assertEqual(True, user.initialized)
#
#     def test_save_state(self):
#         user = User(self.update)
#         user.init_from_update()
#         user.save_state('/тестовое состояние')
#         tg_user = TelegramUser.objects.get(id=0)
#         self.assertEqual('/тестовое состояние', tg_user.state)
#
#
# class RouterTest(TestCase):
#     def setUp(self) -> None:
#         self.urls = [
#             (r'/start', 'start'),
#             (r'/test', 'test'),
#             (r'<wc:req>/start', 'dinamyc_start')
#         ]
#
#     def test_reformat(self):
#         reformat = ReFormat()
#         re_url_1 = reformat.re_url('<str:parameter>')
#         self.assertEqual(re_url_1, '(?P<parameter>[^/]+)')
#         re_url_2 = reformat.re_url('<wc:parameter>')
#         self.assertEqual(re_url_2, '(?P<parameter>.*)')
#         re_url_3 = reformat.re_url('<int:parameter>')
#         self.assertEqual(re_url_3, '(?P<parameter>[0-9]+)')
#         re_url_4 = reformat.re_url('<float:parameter>')
#         self.assertEqual(re_url_4, '(?P<parameter>[0-9]+[.,]?[0-9]+)')
#         re_url_5 = reformat.re_url('<phone:parameter>')
#         self.assertEqual(re_url_5,
#                          '(?P<parameter>\+?(375|80|0)?\(?[0]?(?<tcode>\d{2})\)?(?<tphone>\d{3}[-\s]*\d{2}[-\s]*\d{2}))')
#         re_url_6 = reformat.re_url('<email:parameter>')
#         self.assertEqual(re_url_6, '(?P<parameter>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+.+.[a-zA-Z]{2,4})')
#         re_url_7 = reformat.re_url('<re:parameter>')
#         self.assertEqual(re_url_7, '<re:parameter>')
#
#     def test_router_init(self):
#         router = Router(self.urls)
#         self.assertEqual('start', router.static_urls['/start'])
#         self.assertEqual('test', router.static_urls['/test'])
#         self.assertEqual(('(?P<req>.*)/start', 'dinamyc_start'), router.dynamic_urls[0])
#
#
# class HandlersrsTest(TestCase):
#     def setUp(self) -> None:
#         self.update_message = UpdateMockMessage()
#         self.update_callback = UpdateMockCallback()
#
#     def test_update_handler_message(self):
#         update_handler = UpdateHandler(self.update_message)
#         self.assertEqual(0, update_handler.get_user_id())
#         self.assertEqual('test_first_name', update_handler.get_first_name())
#         self.assertEqual('test_last_name', update_handler.get_last_name())
#         self.assertEqual('test_username', update_handler.get_username())
#         self.assertEqual('TEST', update_handler.get_text())
#         self.assertEqual(0, update_handler.get_message_id())
#
#     def test_update_handler_callback(self):
#         update_handler = UpdateHandler(self.update_callback)
#         self.assertEqual(1040023542, update_handler.get_user_id())
#         self.assertEqual('Dzmitry', update_handler.get_first_name())
#         self.assertEqual(None, update_handler.get_last_name())
#         self.assertEqual('dzmitrydrazdou', update_handler.get_username())
#         self.assertEqual(None, update_handler.get_text())
#         self.assertEqual(412, update_handler.get_message_id())
