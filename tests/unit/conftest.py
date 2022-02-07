from telegram_bot.core.telegram_context import TelegramContext
from telegram_bot.keyboard import BotKeyboard
from telegram_bot.user import User


class KeyboardMock:
    def main(self):
        return

    def categories(self, categories_list):
        return


class UpdateMockMessage:
    data = {
        'message':
            {
                'message_id': 0,
                'user':
                    {
                        'id': 0,
                        'first_name': 'test_first_name',
                        'last_name': 'test_last_name',
                        'username': 'test_username'
                    },
                'text': 'TEST'
            },
    }


class BotMock:
    keyboard = BotKeyboard(TelegramContext('token'))
    text_message = None
    user = User(UpdateMockMessage())  # type: ignore
    user.state = "/"  # type: ignore

    def send_message(self, text, keyboard):
        self.text_message = text


class UpdateMockCallback:
    data = {
        "update_id": 416435499,
        "callback_query": {
            "id": "4466867100678531890",
            "user": {
                "id": 1040023542,
                "is_bot": False,
                "first_name": "Dzmitry",
                "username": "dzmitrydrazdou",
                "language_code": "ru"
            },
            "message": {
                "message_id": 412,
                "user": {
                    "id": 1462806763,
                    "is_bot": False,
                    "first_name": "trener_bot",
                    "username": "personal_trener_bot"
                },
                "chat": {
                    "id": 1040023542,
                    "first_name": "Dzmitry",
                    "username": "dzmitrydrazdou",
                    "type": "private"
                },
                "date": 1630847814,
                "text": "TEST",
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {
                                "text": "1",
                                "callback_data": "1"
                            }
                        ]
                    ]
                }
            },
            "chat_instance": "1054847050213324649",
            "data": "1"
        }
    }