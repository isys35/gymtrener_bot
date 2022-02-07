from typing import List

from django.core.paginator import Page
from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup  # type: ignore
from webhook.models import Keyboard


class State:
    __state = None

    @property
    def state(self):
        return self.__state

    def __init__(self, state):
        self.__state = state
        self.__state.context = self

    def transition_to(self, state):
        self.__state = state
        self.__state.context = self


def keyboard(method):
    def decorator(self, *args):
        self.kb_data = []
        method(self, *args)
        return self.get_keyboard(self.kb_data)

    return decorator


class BotKeyboard(State):
    kb_data = None

    def __init__(self, context):
        State.__init__(self, context)

    def row(self, *args):
        button_row = [*args]
        self.kb_data.append(button_row)

    def get_keyboard(self, buttons):
        """
        Вызывает одноименную функцию из созданного state
        :param buttons:
        :return:
        """
        return self.state.get_keyboard(buttons)

    @keyboard
    def keyboard_from_db(self, keyboard: Keyboard):
        if not keyboard:
            return
        for button in keyboard.buttons.all():  # type: ignore
            self.row(button.text)


    @keyboard
    def categories(self, categories_list):
        self.row('🏠 Главное меню')
        for category in categories_list:
            self.row(str(category).capitalize())

    @keyboard
    def exercises(self, exercise_page: Page):
        exersices_keys = [str(exercise.id) for exercise in exercise_page.object_list]
        self.row(*exersices_keys)
        if exercise_page.has_next() and exercise_page.has_previous():
            self.row('Предыдущая страница', 'Следующая страница')
        elif exercise_page.has_next():
            self.row('Следующая страница ▶️')
        elif exercise_page.has_previous():
            self.row('⬅️ Предыдущая страница')
        self.row('🔙 Назад', '🏠 Главное меню')

    @keyboard
    def favorite_exercises(self, exercise_page: Page):
        exersices_keys = [str(exercise.exercise.id) for exercise in exercise_page.object_list]
        self.row(*exersices_keys)
        if exercise_page.has_next() and exercise_page.has_previous():
            self.row('Предыдущая страница', 'Следующая страница')
        elif exercise_page.has_next():
            self.row('Следующая страница ▶️')
        elif exercise_page.has_previous():
            self.row('⬅️ Предыдущая страница')
        self.row('🏠 Главное меню')

    @keyboard
    def last_exercises(self, exercises: List[dict]):
        exersices_keys = [str(exercise['id']) for exercise in exercises]
        self.row(*exersices_keys)
        self.row('🏠 Главное меню')

    @keyboard
    def exercise(self, favorited=False):
        self.row('💪🏻 Выполнить упражнение 💪🏻')
        if not favorited:
            self.row('Добавить в избранное ⭐️')
        else:
            self.row('Удалить из избранного 🌟️')
        self.row('🔙 Назад', '🏠 Главное меню')

    @keyboard
    def exercise_use(self):
        self.row('Продолжить ➡')
        self.row('❌ Закончить упражнение')

    def clear_keyboard(self):
        return ReplyKeyboardRemove()
