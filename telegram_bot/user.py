import re

from webhook.models import TelegramUser, TelegramMessage
from webhook.serializers import UpdateSerializer


def initialized(method):
    def decorator(self, *args):
        method(self, *args)
        self.initialized = True

    return decorator


class MessageHandler:

    def __init__(self, update: UpdateSerializer):
        self.update = update

    def get_user_id(self):
        return self.update.data['message']['user'].get('id')

    def get_first_name(self):
        return self.update.data['message']['user'].get('first_name')

    def get_last_name(self):
        return self.update.data['message']['user'].get('last_name')

    def get_username(self):
        return self.update.data['message']['user'].get('username')

    def get_text(self):
        return self.update.data['message'].get('text')

    def get_message_id(self):
        return self.update.data['message'].get('message_id')


class CallBackHandler:

    def __init__(self, update: UpdateSerializer):
        self.update = update

    def get_user_id(self):
        return self.update.data['callback_query']['user'].get('id')

    def get_first_name(self):
        return self.update.data['callback_query']['user'].get('first_name')

    def get_last_name(self):
        return self.update.data['callback_query']['user'].get('last_name')

    def get_username(self):
        return self.update.data['callback_query']['user'].get('username')

    def get_text(self):
        return None

    def get_message_id(self):
        return self.update.data['callback_query']['message'].get('message_id')


class UpdateHandler:

    def __init__(self, update: UpdateSerializer):
        self.update = update
        if self.update.data.get('message'):
            self.type = "message"
            self.handler = MessageHandler(update)
        elif self.update.data.get('callback_query'):
            self.type = "callback"
            self.handler = CallBackHandler(update)

    def get_user_id(self):
        return self.handler.get_user_id()

    def get_first_name(self):
        return self.handler.get_first_name()

    def get_last_name(self):
        return self.handler.get_last_name()

    def get_username(self):
        return self.handler.get_username()

    def get_text(self):
        return self.handler.get_text()

    def get_message_id(self):
        return self.handler.get_message_id()


class User:
    id = None
    update = None
    full_request = None
    request = None
    state = '/'

    def __init__(self, update: UpdateSerializer):
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
