from telegram_bot.handlers.handler_interface import HandlerInterface
from webhook.serializers import UpdateSerializer


class MessageHandler(HandlerInterface):

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


class CallBackHandler(HandlerInterface):

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


class UpdateHandler(HandlerInterface):

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
