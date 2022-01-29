from django.template import Template, Context

from telegram_bot.bot import Bot
from webhook.models import View


class ViewDispatcher:

    def __init__(self, bot: Bot, view: View):
        self.bot = bot
        self.view = view

    def as_view(self):
        context = {'update': self.bot.update.data}
        text_message = Template(self.view.text).render(Context(context))
        if not self.view.function:
            self.bot.send_message(text_message)
