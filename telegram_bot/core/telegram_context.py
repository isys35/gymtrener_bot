from io import BufferedReader
from typing import Union
from django.core.files.base import File
import telebot
from telebot.types import Message

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
                     markup: telebot.types.ReplyKeyboardMarkup = None) -> Message:
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
        return self.bot.send_message(**kwargs)

    def send_photo(self, receiver: int,
                   photo: Union[File, BufferedReader],
                   caption: str,
                   markup: telebot.types.ReplyKeyboardMarkup = None) -> Message:
        kwargs = {
            'chat_id': receiver,
            'photo': photo,
            'disable_notification': True,
            'caption': caption,
            'reply_markup': markup,
            'timeout': 1
        }
        return self.bot.send_photo(**kwargs)

    def edit_message(self, receiver: int, text: str, message_id: int):
        kwargs = {
            'chat_id': receiver,
            'text': text,
            'message_id': message_id
        }
        self.bot.edit_message_text(**kwargs)

    def delete_and_create_new_message(self, receiver: int,
                                      text: str, message_id: int,
                                      markup: telebot.types.ReplyKeyboardMarkup = None):
        self.bot.delete_message(chat_id=receiver, message_id=message_id)
        return self.send_message(receiver, text, markup)

    @staticmethod
    def get_user(update: UpdateSerializer):
        user = User(update)
        user.init_from_db()
        if not user.initialized:
            user.init_from_update()
        return user
