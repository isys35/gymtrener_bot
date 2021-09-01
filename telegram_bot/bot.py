from telegram_bot.core.telegram_context import TelegramContext
from telegram_bot.keyboard import BotKeyboard
from webhook.serializers import UpdateSerializer


def save_state(state: str = '/'):
    """
    Декоратор для сохранения состояния пользователя после
    выполнения запроса.
    Если state не передается, то сохраняет корневое состояние.
    :param state: str
    :return: _save_state (wrapper)
    """

    def _save_state(function):
        """
        Выполняет запрос, после сохраняет стейт
        :param function:
        :return: wrapper
        """
        def wrapper(bot, **kwargs):
            function(bot, **kwargs)
            bot.user.save_state(state)
        return wrapper

    return _save_state


class Bot:
    context = None
    user = None
    update = None

    def __init__(self, context: TelegramContext, update: UpdateSerializer):
        self.context = context
        self.keyboard = BotKeyboard(context)
        self.update = update
        self.user = self.context.get_user(update)

    def send_message(self, text, markup=True):
        return self.context.send_message(self.user.id,
                                         text,
                                         markup)