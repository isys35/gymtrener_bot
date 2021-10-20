import os
import pathlib
from unittest import TestCase

from django.conf import settings

from telegram_bot.core.telegram_context import TelegramContext


class WelcomeTest(TestCase):

    def test_send_photo(self):
        context = TelegramContext(settings.TELEGRAM_TOKEN)
        BASE_DIR = pathlib.Path(__file__).parent.parent.parent
        path_file = os.path.join(BASE_DIR, r'media/images/test-image.jpg')
        photo = open(path_file, 'rb')
        context.send_photo(settings.TEST_USER_ID, photo, 'Описание')
        photo.close()