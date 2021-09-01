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
    state = '/'

    def __init__(self, update: UpdateSerializer):
        self.update = update
        self.initialized = False

    def save_message(self):
        message = TelegramMessage(message_id=self.update.data['message']['message_id'],
                                  text=self.full_request,
                                  user_id=self.id)
        message.save()

    def create_user(self):
        tg_user = TelegramUser(id=self.id,
                               first_name=self.update.data['message']['user'].get('first_name'),
                               last_name=self.update.data['message']['user'].get('last_name'),
                               username=self.update.data['message']['user'].get('username'))
        tg_user.save()

    @initialized
    def init_from_update(self):
        self.id = self.update.data['message']['user']['id']
        self.full_request = self.update.data['message']['text']
        self.create_user()
        self.save_message()

    def init_from_db(self):
        tg_user = TelegramUser.objects.filter(id=self.update.data['message']['user']['id'])
        if tg_user:
            self.id = tg_user[0].id
            self.full_request = self.update.data['message']['text']
            self.save_message()
            self.initialized = True
