import re

from telegram_bot.bot import Bot
from telegram_bot.views_dispatcher import ViewDispatcher
from webhook.models import State


class Router:

    @staticmethod
    def dispatcher(bot: Bot):
        state = State.objects.filter(text=bot.user.request, parent=None).first()
        if state and state.view:
            return ViewDispatcher(bot, state.view).as_view()
        else:
            state = State.objects.filter(text=bot.user.request, parent_id=bot.user.state_id).first()
            if state and state.view:
                return ViewDispatcher(bot, state.view).as_view()
        bot.error_404()
