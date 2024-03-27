from pyrogram import types, filters
from loader import bot
from simple_filters import app_admins_filter
import random
import re


reg = re.compile(r"^(-?\d+)[ .+*%]+(-?\d+)$")
reg_2 = re.compile(r"-?(\d+)")


@bot.on_message(filters.me & filters.command(["r", "ran", "run", "rand", "random"], ["!", "/", "."]), group=5)
async def random_cmd(_, message: types.Message):
    text = message.text or message.caption or ""
    args = " ".join(text.split()[1:])

    m = re.match(reg, args)
    m2 = re.match(reg_2, args)

    a = 10
    b = 1

    w = ""

    if m or m2:
        a = int((m or m2)[1])
    else:
        w = "<i>Шаблон был не верен!</i>"
    if m:
        b = int(m[2])

    minimum = min(a, b)
    maximum = max(a, b)

    if minimum == maximum:
        await message.reply("Твои числа равны!")
        return

    await message.reply(f"<b>Число <i>(от {minimum}, до {maximum})</i>: </b> <code>{random.randint(minimum, maximum)}</code>\n\n" + w)
