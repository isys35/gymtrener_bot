import re

from django.db.models import Q

from telegram_bot.bot import Bot
from telegram_bot.views_dispatcher import ViewDispatcher
from webhook.models import State


class Router:

    @staticmethod
    def dispatcher(bot: Bot):
        state = State.objects.filter(Q(text=bot.user.request) | Q(button__text=bot.user.request), parent=None).first()
        if state and state.view:
            return ViewDispatcher(bot, state.view).as_view()
        else:
            state = State.objects.filter(Q(text=bot.user.request) | Q(button__text=bot.user.request),
                                         parent_id=bot.user.state.state_id).first()
            if state and state.view:
                return ViewDispatcher(bot, state.view).as_view()
        bot.error_404()
