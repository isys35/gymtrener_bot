from typing import Optional

from django.template import Template, Context
from telebot.types import Message


from telegram_bot.bot import Bot
from webhook.models import View


class ViewDispatcher:

    def __init__(self, bot: Bot, view: View):
        self.bot = bot
        self.view = view

    def as_view(self) -> Optional[dict]:
        context = {'update': self.bot.update.data}
        text_message = Template(self.view.text).render(Context(context))
        response: Optional[Message] = None
        keyboard = self.bot.keyboard.keyboard_from_db(self.view.keyboard)
        if not self.view.function:
            response = self.bot.send_message(text_message, keyboard)
        if self.view.new_state:
            self.bot.user.state.new(self.view.new_state)
        elif self.view.translate_state_to:
            self.bot.user.state.translate_to(self.view.translate_state_to)
        if response:
            return response.json

    def save_param(self):
        self.bot.user.state.parameter.save()
