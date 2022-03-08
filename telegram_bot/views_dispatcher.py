from typing import Optional

from django.template import Template, Context
from telebot.types import ReplyKeyboardMarkup, Message


from telegram_bot.bot import Bot
from webhook.models import View, State


class ViewDispatcher:

    def __init__(self, bot: Bot, view: View):
        self.bot = bot
        self.view = view
        self.text: str = self.view.text
        self.new_state: State = self.view.new_state
        self.translate_state_to: State = self.view.translate_state_to
        self.function: str = self.view.function
        self.keyboard: Optional[ReplyKeyboardMarkup] = self.bot.keyboard.keyboard_from_db(self.view.keyboard)

    def as_view(self) -> Optional[dict]:
        context = {'update': self.bot.update.data}
        text_message = Template(self.text).render(Context(context))
        response: Optional[Message] = None
        if not self.function:
            response = self.bot.send_message(text_message, self.keyboard)
        if self.new_state:
            self.bot.user.state.new(self.new_state)
        elif self.translate_state_to:
            self.bot.user.state.translate_to(self.translate_state_to)
        if response:
            return response.json

    def save_param(self):
        self.bot.user.state.parameter.save()
