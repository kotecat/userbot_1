from pyrogram import types, filters
from loader import bot
from simple_filters import app_admins_filter
import random
import re


reg = re.compile(r"(\d+)\D+(\d+)")


@bot.on_message(filters.me & filters.command(["r", "rand", "random"], ["!", "/", "."]), group=5)
async def random_cmd(_, message: types.Message):
    text = message.text or message.caption or ""
    args = " ".join(text.split()[1:])

    m = re.match(reg, args)

    if not m:
        return

    a = int(m[1])
    b = int(m[2])

    minimum = min(a, b)
    maximum = max(a, b)

    if minimum == maximum:
        return

    await message.reply(f"<b>Число: </b> <code>{random.randint(minimum, maximum)}</code>")
