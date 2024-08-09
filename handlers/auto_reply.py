from pyrogram import types, filters
from loader import bot
from utils import set_settings, get_settings, AutoReplyPrivateMode
from time import time
from datetime import datetime


COOLDOWN = {}


def check_cooldown(user_id: int, method: str = "auto", time_cd: int = 20) -> bool:
    path = f"{user_id}_{method}"
    current_time = time()
    last_time = COOLDOWN.get(path, 0)
    if current_time - last_time >= time_cd:
        COOLDOWN[path] = current_time
        return True
    return False


@bot.on_message(filters.private & ~filters.me, group=2)
async def auto_reply_handler(_, message: types.Message):
    user = message.from_user
    settings = get_settings(bot.me.id)

    if not check_cooldown(user.id, time_cd=settings.auto_reply.cooldown):
        return

    if not settings.auto_reply.is_on:
        return

    if settings.auto_reply.mode == AutoReplyPrivateMode.FOREVER:
        await message.reply_sticker(settings.auto_reply.sticker, quote=False)
        return

    try:
        time_start = datetime.strptime(settings.auto_reply.time_start, "%H:%M").time()
        time_end = datetime.strptime(settings.auto_reply.time_end, "%H:%M").time()
        current_time = datetime.now().time()
    except Exception:
        settings.auto_reply.time_start = "2:00"
        settings.auto_reply.time_end = "6:00"
        set_settings(bot.me.id, settings)
        return
    else:
        if time_start <= current_time <= time_end:
            await message.reply_sticker(settings.auto_reply.sticker, quote=False)

@bot.on_message(filters.me & filters.command(["auto"], ["/", "!"]), group=3)
async def auto_reply_setting_on_off(_, message: types.Message):
    s = get_settings(bot.me.id)
    s.auto_reply.is_on = not bool(s.auto_reply.is_on)

    text = "✔ Включил автоответчик!" if s.auto_reply.is_on else "❌ Выключил автоответчик!"
    set_settings(bot.me.id, s)

    await message.reply(text)


@bot.on_message(filters.me & filters.command(["cd", "cooldown"], ["/", "!"]) & ~filters.media, group=3)
async def auto_reply_setting_on_off(_, message: types.Message):
    text = message.text.replace("s", "").replace("с", "")
    args = text.split()[1:]

    ex = "\n<u><i>Пример:</i></u> <code>/cd 300</code>"
    err_1 = "<b>Укажи cooldown в секундах</b>" + ex
    err_2 = "<b>Слишком большое значение</b>" + ex
    success = "<b>Успешно\nТекущее значение: <u>{cd}</u> сек.</b>"

    if not args:
        await message.reply(err_1)
        return

    try:
        cd = abs(int(args[0]))
    except:
        await message.reply(err_1)
        return

    if cd > 5000:
        await message.reply(err_2)
        return

    s = get_settings(bot.me.id)
    s.auto_reply.cooldown = cd
    set_settings(bot.me.id, s)

    await message.reply(success.format(cd=cd))


@bot.on_message(filters.me & filters.command(["setsticker", "sticker"], ["/", "!"]), group=3)
async def auto_reply_setting_sticker(_, message: types.Message):
    s = get_settings(bot.me.id)
    reply = message.reply_to_message

    if reply and reply.sticker:
        s.auto_reply.sticker = reply.sticker.file_id
        text = "✔ Установил"
    else:
        text = "❌ Это не ответ на стикер"

    set_settings(bot.me.id, s)
    await message.reply(text)
