from rest_framework import status
from rest_framework.response import Response

from typing import Optional

from django.db.models import Q

from telegram_bot import ViewDispatcher, Bot
from webhook.models import State


class StateDispatcher:

    def __init__(self, bot: Bot):
        self.bot = bot

    def _execute_state_view(self, state: State, save_param: bool = False) -> Optional[Response]:
        if state and state.view:
            view_dispatcher = ViewDispatcher(self.bot, state.view)
            if save_param:
                view_dispatcher.save_param()
            message_data = view_dispatcher.as_view()
            return Response({"success": True, "response_message": message_data}, status=status.HTTP_200_OK)

    def as_state(self) -> Response:
        q_query = Q(text=self.bot.user.request) | Q(button__text=self.bot.user.request)

        states = [
            # the command is a state without parent. Example: in telegram it is '/start'
            State.objects.filter(q_query, parent=None),
            # state with parent
            State.objects.filter(q_query, parent_id=self.bot.user.state.state_id),
        ]
        for state in states:
            response = self._execute_state_view(state.first())
            if response:
                return response

        # the state that saves the entered data
        state = State.objects.filter(parent_id=self.bot.user.state.state_id).exclude(name_parameter__isnull=True).first()
        response = self._execute_state_view(state, save_param=True)
        if response:
            return response

        message_data = self.bot.error_404()
        return Response({"success": False, "error": "state not found", "response_message": message_data})