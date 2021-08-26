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

    @staticmethod
    def get_user(update: UpdateSerializer):
        user = User(update)
        user.from_update()
