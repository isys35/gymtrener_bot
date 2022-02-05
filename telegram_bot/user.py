import re
from typing import Optional

from telegram_bot.handlers.handlers import UpdateHandler
from webhook.models import TelegramUser, TelegramMessage, State, StateParameter
from webhook.serializers import UpdateSerializer


def initialize(method):
    def decorator(self, *args):
        method(self, *args)
        self.initialized = True

    return decorator


class UserStateParameter:
    value: Optional[str] = None

    def __init__(self, state: 'UserState'):
        self.state = state

    def save(self):
        state_parameter = StateParameter.objects.filter(state_id=self.state.state_id,
                                                        user_id=self.state.user.id).first()
        if state_parameter:
            state_parameter.value = self.value
            state_parameter.save()
            return
        StateParameter.objects.create(state_id=self.state.state_id,
                                      user_id=self.state.user.id,
                                      value=self.value)


class UserState:
    state_id: Optional[int] = None

    def __init__(self, user: 'User'):
        self.user = user

    def new(self, state: State):
        self.state_id = state.id
        self.user.save()

    def clear(self):
        self.state_id = None
        self.user.save()

    def translate_to(self, text_state: Optional[str] = None):
        if not text_state:
            text_state = self.user.request
        state = State.objects.filter(parent_id=self.state_id, text=text_state).first()
        if state:
            self.state_id = state.id
        else:
            state = State.objects.create(parent_id=self.state_id, text=text_state)
            state.save()
        self.user.save()


class User:
    id = None
    update = None
    type_request: str = None
    request: Optional[str] = None
    initialized: bool = False
    callback: Optional[str] = None

    def __init__(self, update: UpdateSerializer):
        self.update = update
        self.update_handler = UpdateHandler(update)
        self.state = UserState(self)

    def save_message(self):
        if self.update_handler.type == "message":
            message = TelegramMessage(message_id=self.update_handler.get_message_id(),
                                      text=self.update_handler.get_text(),
                                      user_id=self.id)
            message.save()

    def create_user(self):
        tg_user = TelegramUser(id=self.id,
                               first_name=self.update_handler.get_first_name(),
                               last_name=self.update_handler.get_last_name(),
                               username=self.update_handler.get_username())
        tg_user.save()

    def _init_request(self):
        if self.update_handler.type == "message":
            # reg = re.compile("""[^a-zA-Zа-яА-Я";#().,0-9«»-]""")
            # self.request = reg.sub(' ', self.update_handler.get_text()).strip().lower()
            self.request = self.update_handler.get_text()
            self.type_request = 'message'
        elif self.update_handler.type == "callback":
            self.type_request = 'callback'
            self.callback = self.update_handler.get_callback()

    @initialize
    def init_from_update(self):
        self.id = self.update_handler.get_user_id()
        self._init_request()
        self.create_user()
        self.save_message()

    def init_from_db(self):
        tg_user = TelegramUser.objects.filter(id=self.update_handler.get_user_id())
        if tg_user:
            tg_user = tg_user.first()
            self.id = tg_user.id
            if tg_user.state:
                self.state.state_id = tg_user.state_id
            self._init_request()
            self.save_message()
            self.initialized = True

    def save(self):
        TelegramUser.objects.update(id=self.id, state_id=self.state.state_id)
