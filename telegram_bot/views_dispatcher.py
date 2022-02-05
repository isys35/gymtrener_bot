from django.template import Template, Context
from . import views

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
        if not self.function:
            self.bot.send_message(text_message, self.keyboard)
        else:
            if self.function in dir(views):
                func = eval('views.' + self.function)
                func(self)
        if self.new_state:
            self.bot.user.state.new(self.new_state)
