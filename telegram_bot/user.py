import re
from typing import Optional

from telegram_bot.handlers.handlers import UpdateHandler
from webhook.models import TelegramUser, TelegramMessage, State
from webhook.serializers import UpdateSerializer


def initialized(method):
    def decorator(self, *args):
        method(self, *args)
        self.initialized = True

    return decorator


class User:
    id = None
    update = None
    type_request: str = None
    request: Optional[str] = None
    state_id: Optional[int] = None
    callback: Optional[str] = None

    def __init__(self, update: UpdateSerializer):
        self.update = update
        self.update_handler = UpdateHandler(update)
        self.initialized = False

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

    @initialized
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
                self.state_id = tg_user.state_id
            self._init_request()
            self.save_message()
            self.initialized = True

    def save(self):
        TelegramUser.objects.update(id=self.id, state_id=self.state_id)

    def save_state(self, text_state: Optional[str] = None, blank=False):
        if blank:
            self.state_id = None
            self.save()
            return
        if not text_state:
            text_state = self.request
        state = State.objects.filter(parent_id=self.state_id, text=text_state).first()
        if state:
            self.state_id = state.id
        else:
            state = State.objects.create(parent_id=self.state_id, text=text_state)
            state.save()
        self.save()
