import telebot

from telegram_bot.user import User
from webhook.serializers import UpdateSerializer


class TelegramContext:
    bot = None

    def __init__(self, token: str):
        """
        Инициализирует telebot.TeleBot(token)
        :param token: токен бота в Telegram
        """
        self.bot = telebot.TeleBot(token, threaded=False)

    @staticmethod
    def get_keyboard(buttons: list) -> telebot.types.ReplyKeyboardMarkup:
        """
        Создает и возвращает клавиатуру
        для показа пользователю в Telegram
        :param buttons: список с кнопками
        :return: telebot.types.ReplyKeyboardMarkup
        """
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1,
                                                   resize_keyboard=True)
        for row in buttons:
            markup.row(*row)
        return markup

    def send_message(self,
                     receiver: int,
                     text: str,
                     markup: telebot.types.ReplyKeyboardMarkup = None) -> None:
        """
        Отправляет сообщение пользователю в Telegram.
        :param receiver: id пользователя в Telegram
        :param text: строка с сообщением
        :param markup: клавиатура для показа пользователю
        :return: None
        """
        kwargs = {
            'chat_id': receiver,
            'text': text,
            'disable_web_page_preview': True,
            'disable_notification': True,
            'parse_mode': 'HTML',
            'reply_markup': markup,
            'timeout': 1
        }
        self.bot.send_message(**kwargs)

    def edit_message(self, receiver: int, text: str, message_id: int):
        kwargs = {
            'chat_id': receiver,
            'text': text,
            'message_id': message_id
        }
        self.bot.edit_message_text(**kwargs)

    @staticmethod
    def get_user(update: UpdateSerializer):
        user = User(update)
        user.init_from_db()
        if not user.initialized:
            user.init_from_update()
        return user
