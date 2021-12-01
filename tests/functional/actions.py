import json
import os
from pathlib import Path

import requests

MOCKS_DIR = os.path.join(Path(__file__).resolve().parent.parent, 'mocks')
WEBHOOK_URL = 'http://127.0.0.1:8000/webhook/'


def load_mock(file_name: str):
    with open(os.path.join(MOCKS_DIR, file_name), encoding='utf-8') as json_file:
        return json.load(json_file)


def action(file_mock: str):
    data = load_mock(file_mock)
    response = requests.post(WEBHOOK_URL, json=data)
    return response.ok


def start():
    """Комманда /start"""
    return action('start.json')


def select_exercise():
    """Кнопка - выбор упражнения"""
    return action('select_exercise.json')


def category_back():
    """Кнопка - Спина"""
    return action('category_back.json')


if __name__ == '__main__':
    start()
    select_exercise()
    category_back()
