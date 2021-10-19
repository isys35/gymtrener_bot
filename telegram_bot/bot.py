from telegram_bot.core.telegram_context import TelegramContext
from telegram_bot.keyboard import BotKeyboard
from webhook.serializers import UpdateSerializer
from django.core.files.base import File


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

    def send_message(self, text: str, markup=True):
        return self.context.send_message(self.user.id,
                                         text,
                                         markup)

    def send_photo(self, text: str, photo: File, markup=None):
        return self.context.send_photo(self.user.id,
                                       photo,
                                       text,
                                       markup)

    def edit_message(self, text: str, message_id: int, markup=None):
        return self.context.delete_and_create_new_message(self.user.id,
                                                          text,
                                                          message_id,
                                                          markup)

    def error_404(self):
        text_message = 'Неизвестная комманда 😧...'
        self.send_message(text_message, self.keyboard.main())
        self.user.save_state('/')
