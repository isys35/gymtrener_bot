import json
import os
from pathlib import Path

MOCKS_DIR = os.path.join(Path(__file__).resolve().parent, 'mocks')


def load_mock(file_name: str):
    with open(os.path.join(MOCKS_DIR, file_name), encoding='utf-8') as json_file:
        return json.load(json_file)
    