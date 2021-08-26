from webhook.serializers import UpdateSerializer


class User:
    id = None
    update = None
    full_request = None
    state = '/'

    def __init__(self, update: UpdateSerializer):
        self.update = update

    def init_from_update(self):
        self.id = self.update.data['message']['user']['id']
        self.full_request = self.update.data['message']['text']
        return True
