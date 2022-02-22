from datetime import datetime

from django.test import TestCase

from tests.telegram_emulator.emulator import TextSimpleCommand
from webhook.models import State, View


class StateAndViewStartMessage(TestCase):

    def setUp(self) -> None:
        view = View.objects.create(text='Добро пожаловать')
        State.objects.create(text='старт', view_id=view.id)

    def test_view(self):
        TextSimpleCommand('старт').execute(self.client)


