from webhook.serializers import UpdateSerializer


class User:
    id = None
    update = None

    def __init__(self, update: UpdateSerializer):
        self.update = update

    def from_update(self):
        self.id = int(self.update.message.user.id)
        return True
