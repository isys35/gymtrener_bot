from telegram_bot.core.telegram_context import TelegramContext
from telegram_bot.keyboard import BotKeyboard
from webhook.serializers import UpdateSerializer


class Bot:
    context = None
    user = None
    update = None

    def __init__(self, context: TelegramContext, update: UpdateSerializer):
        self.context = context
        self.keyboard = BotKeyboard(context)
        self.update = update
        self.user = self.context.get_user(update)

    def send_message(self, text, markup=True):
        return self.context.send_message(self.user.id,
                                         text,
                                         markup)