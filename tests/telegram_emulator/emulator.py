from abc import ABC, abstractmethod

from django.urls import reverse
from django.test.client import Client
from rest_framework.response import Response

from tests.utils import load_mock


class Command(ABC):

    @abstractmethod
    def execute(self, client: Client) -> Response:
        pass


class SimpleCommand(Command):

    def __init__(self, json_data: dict):
        self.json_data = json_data

    def execute(self, client: Client) -> Response:
        response = client.post(reverse('bot:webhook'), data=self.json_data, content_type='application/json')
        return response


class TextSimpleCommand(SimpleCommand):
    DEFAULT_FILE = 'message.json'

    def __init__(self, message: str):
        json_data = load_mock(self.DEFAULT_FILE)
        json_data["message"]["text"] = message
        super().__init__(json_data)
