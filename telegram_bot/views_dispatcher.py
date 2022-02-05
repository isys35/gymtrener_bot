from django.template import Template, Context

from telegram_bot.bot import Bot
from webhook.models import View


class ViewDispatcher:

    def __init__(self, bot: Bot, view: View):
        self.bot = bot
        self.view = view
        self.text = self.view.text
        self.new_state = self.view.new_state
        self.function = self.view.function
        self.keyboard = self.bot.keyboard.keyboard_from_db(self.view.keyboard)

    def as_view(self):
        context = {'update': self.bot.update.data}
        text_message = Template(self.text).render(Context(context))
        if not self.view.function:
            self.bot.send_message(text_message, self.keyboard)
        if self.new_state:
            self.bot.user.save_state(new_state=self.new_state)
