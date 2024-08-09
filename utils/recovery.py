import json
from typing import Optional, Union, List, Dict, TypeAlias
from pyrogram.types import Message


Messages: TypeAlias = "List[Dict[str, List[Union[str, int, bool]]]]"
PATH_TO_MESSAGES = "messages.json"
UTF_8 = "utf-8"


# def add_message()


def set_messages(messages: Messages) -> bool:
    path = PATH_TO_MESSAGES
    old = get_all_messages()

    try:
        with open(path, "w", encoding=UTF_8) as file:
            json.dump(messages, file, ensure_ascii=False, indent=4)
            return True
    except:
        with open(path, "w", encoding=UTF_8) as file:
            json.dump(old, file, ensure_ascii=False, indent=4)
            return False


def get_all_messages() -> Messages:
    path = PATH_TO_MESSAGES
    try:
        with open(path, encoding=UTF_8) as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        set_messages([])
        return []
