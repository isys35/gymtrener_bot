from django.test import TestCase

from tests.telegram_emulator.emulator import TextSimpleCommand
from webhook.models import State, View, TelegramUser


class TestSimpleView(TestCase):

    def setUp(self) -> None:
        simple_view = View.objects.create(text='Добро пожаловать')
        State.objects.create(text='старт', view_id=simple_view.id)

    def test_view(self):
        response = TextSimpleCommand('старт').execute(self.client)
        assert response.status_code == 200
        assert response.data['success'] == True
        assert response.data['response_message']['text'] == 'Добро пожаловать'

    def test_unknown_message(self):
        response = TextSimpleCommand('привет').execute(self.client)
        assert response.status_code == 200
        assert response.data['success'] == False


class TestViewWithContextInMessage(TestCase):

    def setUp(self) -> None:
        view = View.objects.create(text='Добро пожаловать {{ update.message.user.first_name }}')
        State.objects.create(text='старт', view_id=view.id)

    def test_view(self):
        response = TextSimpleCommand('старт').execute(self.client)
        assert response.status_code == 200
        assert response.data['success'] == True
        assert response.data['response_message']['text'] == 'Добро пожаловать DZMITRY'


class TestViewWithNewState(TestCase):

    def setUp(self) -> None:
        self.state = State.objects.create(text='главное меню')
        view = View.objects.create(text='Добро пожаловать', new_state_id=self.state.id)
        State.objects.create(text='restart', view_id=view.id)

    def test_view(self):
        command = TextSimpleCommand('restart')
        response = command.execute(self.client)
        assert response.status_code == 200
        assert response.data['success'] == True
        assert response.data['response_message']['text'] == 'Добро пожаловать'

        user = TelegramUser.objects.filter(id=command.json_data["message"]["from"]["id"]).first()
        assert user.state == self.state
        assert user.state.parent is None


class TestViewTranslateToState(TestCase):

    def setUp(self) -> None:
        self.state = State.objects.create(text='главное меню')
        view = View.objects.create(text='Добро пожаловать', translate_state_to_id=self.state.id)
        self.state_2 = State.objects.create(text='restart', view_id=view.id)

    def test_view(self):
        command = TextSimpleCommand('главное меню')
        command.execute(self.client)
        command = TextSimpleCommand('restart')
        response = command.execute(self.client)
        assert response.status_code == 200
        assert response.data['success'] == True
        assert response.data['response_message']['text'] == 'Добро пожаловать'

        user = TelegramUser.objects.filter(id=command.json_data["message"]["from"]["id"]).first()
        assert user.state == self.state
        assert user.state.parent == self.state_2
