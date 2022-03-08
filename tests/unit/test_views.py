from django.test import TestCase

from tests.telegram_emulator.emulator import TextSimpleCommand
from webhook.models import State, View


class TestSimpleView(TestCase):

    def setUp(self) -> None:
        simple_view = View.objects.create(text='Добро пожаловать')
        State.objects.create(text='старт', view_id=simple_view.id)

    def test_simple_view(self):
        response = TextSimpleCommand('старт').execute(self.client)
        assert response.status_code == 200
        assert response.data['success'] == True


class TestViewWithUpdateParameter(TestCase):

    def setUp(self) -> None:
        view = View.objects.create(text='Добро пожаловать {{ update.message.user.first_name }}')
        State.objects.create(text='старт', view_id=view.id)

    def test_view_with_update(self):
        response = TextSimpleCommand('старт').execute(self.client)
        assert response.status_code == 200
        assert response.data['success'] == True
