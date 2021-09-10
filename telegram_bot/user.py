import re

from telegram_bot.handlers.handlers import UpdateHandler
from webhook.models import TelegramUser, TelegramMessage
from webhook.serializers import UpdateSerializer


def initialized(method):
    def decorator(self, *args):
        method(self, *args)
        self.initialized = True

    return decorator


class User:
    id = None
    update = None
    full_request = None
    request = None
    state = '/'
    callback = None

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
            reg = re.compile("""[^a-zA-Zа-яА-Я";#().,0-9«»-]""")
            self.request = reg.sub(' ', self.update_handler.get_text()).strip().lower()
        elif self.update_handler == "callback":
            self.request = 'callback'
            self.callback = self.update_handler.get_callback()
        if self.request == '':
            self.full_request = self.state
        elif self.state == '/':
            self.full_request = self.state + self.request
        else:
            self.full_request = f"{self.state}/{self.request}"

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
            self.state = tg_user.state
            self._init_request()
            self.save_message()
            self.initialized = True

    def save(self):
        TelegramUser.objects.update(id=self.id, state=self.state)

    def save_state(self, new_state=None):
        if new_state is None:
            if self.state == '/':
                self.state = self.state + self.request
            else:
                self.state = self.state + '/' + self.request
        else:
            self.state = new_state
        self.save()
