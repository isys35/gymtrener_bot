from django.core.paginator import Paginator, Page
from telebot import types


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
    def main(self) -> None:
        """
        Функция генерации клавиатуры главного меню.
        :return: None
        """
        self.row('💪🏻 Выбрать упражнение')

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
        else:
            self.row('⬅️ Предыдущая страница')
        self.row('🔙 Назад', '🏠 Главное меню')

    @keyboard
    def exercise(self):
        self.row('Выполнить упражнение')
        self.row('🔙 Назад', '🏠 Главное меню')

    # def exercises(self, exersices) -> types.InlineKeyboardMarkup:
    #     markup = types.InlineKeyboardMarkup()
    #     btn_list = []
    #     for exersice in exersices:
    #         btn = types.InlineKeyboardButton(text=exersice.id, callback_data=exersice.id)
    #         btn_list.append(btn)
    #     markup.add(*btn_list)
    #     return markup
