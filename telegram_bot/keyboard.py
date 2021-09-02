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
            self.row(str(category))