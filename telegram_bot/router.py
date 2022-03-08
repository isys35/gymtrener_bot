import re
from typing import Optional

from django.db.models import Q

from telegram_bot.bot import Bot
from telegram_bot.views_dispatcher import ViewDispatcher
from webhook.models import State


class Router:

    @staticmethod
    def dispatcher(bot: Bot) -> Optional[dict]:
        q_query = Q(text=bot.user.request) | Q(button__text=bot.user.request)
        state = State.objects.filter(q_query, parent=None).first()
        if state and state.view:
            return ViewDispatcher(bot, state.view).as_view()
        state = State.objects.filter(q_query,
                                     parent_id=bot.user.state.state_id).first()
        if state and state.view:
            return ViewDispatcher(bot, state.view).as_view()
        state = State.objects.filter(parent_id=bot.user.state.state_id).exclude(name_parameter__isnull=True).first()
        if state and state.view:
            view_dispatcher = ViewDispatcher(bot, state.view)
            view_dispatcher.save_param()
            return view_dispatcher.as_view()
        bot.error_404()
