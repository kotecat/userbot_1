from pydantic import BaseModel
from enum import Enum
import json
from typing import Optional, Union

PATH_TO_SETTINGS = "{me_id}_params.json"
UTF_8 = "utf-8"


class AutoReplyPrivateMode(str, Enum):
    TIME = "time"
    FOREVER = "forever"

class SettingsAutoReplyPrivate(BaseModel):
    mode: Optional[AutoReplyPrivateMode] = AutoReplyPrivateMode.FOREVER
    time_start: Optional[str] = "2:00"
    time_end: Optional[str] = "6:00"
    sticker: Optional[str] = "CAACAgIAAxkDAAEBNqplsoJC2i0MSNp82FNH5AVjZzBJawACtzYAAgzM6UmWTdUpDDIL8x4E"
    cooldown: Optional[int] = 300
    is_on: Optional[bool] = True

class Settings(BaseModel):
    auto_reply: Optional[SettingsAutoReplyPrivate] = SettingsAutoReplyPrivate()


def get_settings(user_id: int) -> Settings:
    path = PATH_TO_SETTINGS.format(me_id=user_id)
    try:
        with open(path, encoding=UTF_8) as file:
            return Settings(**json.load(file))
    except FileNotFoundError:
        with open(path, "w", encoding=UTF_8) as file:
            json.dump(json.loads(Settings().json()), file, ensure_ascii=False, indent=4)
            return Settings()


def set_settings(user_id: int, new: Settings) -> bool:
    path = PATH_TO_SETTINGS.format(me_id=user_id)
    old = get_settings(user_id)

    try:
        with open(path, "w", encoding=UTF_8) as file:
            json.dump(json.loads(new.json()), file, ensure_ascii=False, indent=4)
            return True
    except:
        with open(path, "w", encoding=UTF_8) as file:
            json.dump(json.loads(old.json()), file, ensure_ascii=False, indent=4)
            return False