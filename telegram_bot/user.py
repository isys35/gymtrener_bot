import re

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

    def __init__(self, update: UpdateSerializer):
        self.update = update
        self.initialized = False

    def save_message(self):
        message = TelegramMessage(message_id=self.update.data['message']['message_id'],
                                  text=self.update.data['message']['text'],
                                  user_id=self.id)
        message.save()

    def create_user(self):
        tg_user = TelegramUser(id=self.id,
                               first_name=self.update.data['message']['user'].get('first_name'),
                               last_name=self.update.data['message']['user'].get('last_name'),
                               username=self.update.data['message']['user'].get('username'))
        tg_user.save()

    def _init_request(self):
        reg = re.compile("""[^a-zA-Zа-яА-Я";#().,0-9«»-]""")
        self.request = reg.sub(' ', self.update.data['message']['text']).strip().lower()
        if self.request == '':
            self.full_request = self.state
        elif self.state == '/':
            self.full_request = self.state + self.request
        else:
            self.full_request = f"{self.state}/{self.request}"

    @initialized
    def init_from_update(self):
        self.id = self.update.data['message']['user']['id']
        self._init_request()
        self.create_user()
        self.save_message()

    def init_from_db(self):
        tg_user = TelegramUser.objects.filter(id=self.update.data['message']['user']['id'])
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
