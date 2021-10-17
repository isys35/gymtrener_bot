from unittest import TestCase

from django.conf import settings

from telegram_bot.core.telegram_context import TelegramContext


class WelcomeTest(TestCase):

    def test_send_photo(self):
        context = TelegramContext(settings.TELEGRAM_TOKEN)
        photo = open(r'media\images\test-image.jpg', 'rb')
        context.send_photo(settings.TEST_USER_ID, photo, 'Описание')
        photo.close()