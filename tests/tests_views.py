from django.test import TestCase
from django.utils.safestring import SafeString

from telegram_bot.views import welcome, select_category, select_exercise, favorite_exercises
from tests.conftest import BotMock
from webhook.models import Category, Exersice, FavoritedExercises, TelegramUser


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


class SelectFavoriteExerciseTest(TestCase):

    def setUp(self):
        self.tg_user = TelegramUser(id=123,
                                    first_name='dasdasdas',
                                    last_name='dasdasdasd',
                                    username='dasdasd')
        self.tg_user.save()
        self.bot = BotMock()
        self.bot.user.id = self.tg_user.id
        self.category = Category(title='Грудь')
        self.category.save()
        self.exercise = Exersice(title='Упражнение', category=self.category)
        self.exercise.save()

    def test_select_exercise(self):
        favorite_exercises(self.bot)
        self.assertEqual('/', self.bot.user.state)

        favorite_exercise = FavoritedExercises(user_id=self.tg_user.id, exercise_id=self.exercise.id)
        favorite_exercise.save()

        favorite_exercises(self.bot)
        self.assertEqual('/избранные упражнения/1', self.bot.user.state)
