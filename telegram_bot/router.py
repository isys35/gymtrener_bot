import re

from telegram_bot.bot import Bot
from telegram_bot.views_dispatcher import ViewDispatcher
from webhook.models import State


class Router:

    @staticmethod
    def dispatcher(bot: Bot):
        if not bot.user.state:
            states = State.objects.filter(text=bot.user.request, parent=None)
            state = None
            if states:
                state = states.first()
            if state and state.view:
                view_dispatcher = ViewDispatcher(state.view).as_view()
        bot.error_404()