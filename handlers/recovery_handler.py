from pyrogram import types, filters, Client, enums
from loader import Config, bot
from typing import List, Tuple, TypeAlias
from datetime import datetime, timedelta
import json
from time import time as time_st
import asyncio
from pony.orm import (
    Database,
    Required,
    Optional,
    PrimaryKey,
    Set,
    db_session,
    commit,
    select,
    raw_sql
)


Parsed: TypeAlias = Tuple[bool, int, int | None]
access_filter = ~filters.media & filters.private & filters.me

sm = asyncio.Semaphore(1)
db = Database()


class Users(db.Entity):
    _table_ = "users"
    id = PrimaryKey(int, auto=False, size=64)
    first_name = Required(str, 128)
    last_name = Optional(str, 128, default="")
    username = Optional(str, 64)
    messages = Set("Messages")


class Chats(db.Entity):
    _table_ = "chats"
    id = PrimaryKey(int, size=64)
    title = Required(str, 128)
    username = Optional(str, 64)
    type = Required(str, 64)
    messages = Set("Messages")


class Messages(db.Entity):
    _table_ = "messages"
    message_id = Required(int)
    reply_id = Optional(int)
    text = Optional(str, 4096)
    media_type = Optional(str, 16)
    media_id = Optional(str, 128)
    chat = Required(Chats, column="chat_id")
    is_deleted = Required(bool, default=True)
    time = Required(float)
    user = Required(Users, column="user_id")
    is_edited = Required(bool, default=False)


db.bind(provider="sqlite", filename="../messages.db", create_db=True)
db.generate_mapping(create_tables=True)


@db_session
def handler_user(message: types.Message):
    sender = message.sender_chat
    user_tg = message.from_user

    if sender:
        user_id = sender.id
        first_name = sender.title
        last_name = ""
        username = sender.username or ""
    else:
        user_id = user_tg.id
        first_name = user_tg.first_name
        last_name = user_tg.last_name or ""
        username = user_tg.username or ""

    users = list(select(u for u in Users if u.id == user_id))

    if users:
        get_user: Users = users[-1]
        # update
        get_user.first_name = first_name
        get_user.last_name = last_name
        get_user.username = username
    else:
        Users(
            id=user_id,
            first_name=first_name,
            last_name=last_name,
            username=username
        )

    return user_id


@db_session
def handler_chat(message: types.Message):
    chat = message.chat

    if not chat:
        return
    chat_id = chat.id
    if chat_id == bot.me.id:
        return
    try:
        title = chat.title or chat.first_name + (chat.last_name or "") or "None~"
        username = chat.username or ""
        type_ = str(message.chat.type).replace("ChatType.", "").upper()

        chats = list(select(c for c in Chats if c.id == chat_id))

        if chats:
            get_chat: Chats = chats[-1]
            # update
            get_chat.title = title
            get_chat.username = username
            get_chat.type = type_
        else:
            Chats(
                id=chat_id,
                title=title,
                username=username,
                type=type_
            )
    except:
        print(message.chat)


@db_session
def handler_message(message: types.Message, user_id: int, is_edit: bool = False):
    message_id = message.id
    reply_id = message.reply_to_message_id
    text = message.text or message.caption or ""
    chat_id = message.chat.id
    is_deleted = False
    time_data = round((message.edit_date if is_edit else message.date).timestamp(), 4)
    print(time_data, is_edit)

    if message.sticker:
        media_type = "sticker"
        media_id = message.sticker.file_id
    elif message.photo:
        media_type = "photo"
        media_id = message.photo.file_id
    elif message.audio:
        media_type = "audio"
        media_id = message.audio.file_id
    elif message.document:
        media_type = "document"
        media_id = message.document.file_id
    elif message.animation:
        media_type = "animation"
        media_id = message.animation.file_id
    elif message.video:
        media_type = "video"
        media_id = message.video.file_id
    elif message.voice:
        media_type = "voice"
        media_id = message.voice.file_id
    elif message.video_note:
        media_type = "video_note"
        media_id = message.video_note.file_id
    elif message.contact:
        media_type = "contact"
        media_id = ""
    elif message.location:
        media_type = "location"
        media_id = ""
    elif message.poll:
        media_type = "poll"
        media_id = message.poll.id
    elif message.dice:
        media_type = "dice"
        media_id = f"{message.dice.emoji}:{message.dice.value}"
    elif message.game:
        media_type = "game"
        media_id = message.game.id
    elif message.service:
        media_type = "service"
        media_id = f"{message.service}".split(".", maxsplit=1)[-1]
    else:
        media_id = ""
        media_type = ""

    Messages(
        message_id=message_id,
        reply_id=reply_id,
        text=text,
        media_type=media_type,
        media_id=str(media_id),
        chat=chat_id,
        is_deleted=is_deleted,
        time=time_data,
        user=user_id,
        is_edited=is_edit
    )


@db_session
def handler_delete_message(chat_id: int, message_id: int):
    messages = list(
        select(m for m in Messages if m.message_id == message_id and m.chat.id == chat_id and m.is_edited == False))
    if messages:
        get_message: Messages = messages[-1]
        print(get_message.text, get_message.chat.id)
        get_message.is_deleted = True


@bot.on_message(group=777)
async def logger_messages(client: Client, message: types.Message):
    user_id = handler_user(message)
    # if message.chat.type not in {enums.ChatType.PRIVATE, enums.ChatType.BOT}:
    handler_chat(message)

    # if message.chat.type in {
    #     enums.ChatType.GROUP,
    #     enums.ChatType.SUPERGROUP,
    #     enums.ChatType.CHANNEL
    # }:
    handler_message(message, user_id)


@bot.on_deleted_messages()
async def delete(client: Client, messages: List[types.Message]):
    for message in messages:
        if message.chat:
            message_id = message.id
            chat_id = message.chat.id
            handler_delete_message(chat_id, message_id)


# EASY API
def parse_message_ids(text: str) -> Parsed | None:
    args = text.lower().strip().split()[1:]
    deleted = False
    first_id = None
    second_id = None

    for arg in args:
        try:
            arg_int = int(arg)
        except ValueError:
            pass
        else:
            if first_id is None:
                first_id = arg_int
            elif second_id is None:
                second_id = arg_int

        if arg.replace("-", "").startswith(("d", "rem")):
            deleted = True

    if first_id is not None:
        return deleted, first_id, second_id
    return


@db_session
def get_messages_user(parsed: Parsed) -> List[Messages]:
    deleted = parsed[0]
    user_id = parsed[1]
    chat_id = parsed[2]

    if chat_id:
        messages = list(select(m for m in Messages if
                               m.is_edited == False and m.user.id == user_id and m.chat.id == chat_id and (
                                           m.is_deleted == True or m.is_deleted == deleted)))
    else:
        messages = list(select(m for m in Messages if m.is_edited == False and m.user.id == user_id and (
                    m.is_deleted == True or m.is_deleted == deleted)))

    return messages


@db_session
def get_messages_chat(parsed: Parsed) -> List[Messages]:
    deleted = parsed[0]
    chat_id = parsed[1]
    user_id = parsed[2]

    if user_id:
        messages = list(select(m for m in Messages if
                               m.is_edited == False and m.chat.id == chat_id and m.user.id == user_id and (
                                           m.is_deleted == True or m.is_deleted == deleted)))
    else:
        messages = list(select(m for m in Messages if m.is_edited == False and m.chat.id == chat_id and (
                    m.is_deleted == True or m.is_deleted == deleted)))

    return messages


@db_session
def get_messages_chat_find(chat_id: int, q: str, is_like: bool, user_id: int | None) -> List[Messages]:
    q_raw = "'%$q%'" if not is_like else "$q"

    print(is_like)

    if user_id is not None:
        messages = list(select(
            m for m in Messages if m.chat.id == chat_id and m.user.id == user_id and q.lower() in m.text.lower()))
    else:
        messages = list(select(m for m in Messages if m.chat.id == chat_id and q.lower() in m.text.lower()))

    return messages


async def str_with_file(data: str, chat_id: int):
    m = await bot.send_message(chat_id, "Ожидайте")
    async with sm:
        with open("data.txt", "w+", encoding="utf-8") as file:
            file.write(data)
        await bot.send_document(chat_id, document="data.txt")
        await m.delete()


@bot.on_message(filters.command(["user"], [".", "/", "!"]) & access_filter)
async def get_data_user(client: Client, message: types.Message):
    text = message.text
    parsed = parse_message_ids(text)

    if parsed is None:
        await message.reply(
            "<b>/user user_id chat_id del</b>\n\n> user_id - ОБЯЗАТЕЛЬНО\n> chat_id - фильтрует только по чату, "
            "по умолчанию все чаты\n> del - отобразить только удаленные сообщения")
        return

    list_messages = get_messages_user(parsed)

    await str_with_file(
        "\n".join(map(lambda msg: f"{msg.chat.id=} | {msg.is_deleted=} : {msg.text}", list_messages)),
        message.chat.id
    )


@bot.on_message(filters.command(["chat"], [".", "/", "!"]) & access_filter)
async def get_data_user(client: Client, message: types.Message):
    text = message.text
    parsed = parse_message_ids(text)

    if parsed is None:
        await message.reply(
            "<b>/chat chat_id user_id del</b>\n\n> chat_id - ОБЯЗАТЕЛЬНО\n> user_id - фильтрует только по юзеру, "
            "по умолчанию все юзеры\n> del - отобразить только удаленные сообщения")
        return

    list_messages = get_messages_chat(parsed)

    await str_with_file(
        ("\n".join(map(lambda msg: f"{msg.user.id=} | {msg.is_deleted=} : {msg.text}", list_messages))),
        message.chat.id
    )
