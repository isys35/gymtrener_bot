from typing import Optional

from . import ViewDispatcher
from webhook.models import Category


def select_category(dispatcher: ViewDispatcher) -> Optional[dict]:
    categories = Category.objects.all()
    message = dispatcher.bot.send_message(dispatcher.view.text, dispatcher.bot.keyboard.categories(categories))
    return message.json