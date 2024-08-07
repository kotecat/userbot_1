from pyrogram import types, filters, Client
from loader import bot
from simple_filters import app_admins_filter

# imports for eval
from math import *
from base64 import *
from random import *


@bot.on_message(app_admins_filter & filters.command(["e"], ["/", "!"]), group=-1)
async def cmd_eval(client: Client, message: types.Message):
    text = message.text or message.caption
    msg = message
    reply = message.reply_to_message
    me = client.me

    template = "{text}\n<b>{result_type}</b>: <code>{result_body}</code>"

    if not text:
        return
    if len(text.split(" ")) <= 1:
        return

    text = " ".join(text.split(" ")[1:])

    try:
        result_type = "result"
        await message.edit_text(template.format(text=text, result_type=result_type, result_body=str(eval(text))))
    except Exception as e:
        result_type = "error"
        await message.edit_text(template.format(text=text, result_type=result_type, result_body=str(e)))

    message.continue_propagation()


@bot.on_message(app_admins_filter, group=-2)
async def try_eval(client: Client, message: types.Message):
    text = message.text
    msg = message
    reply = message.reply_to_message
    me = client.me

    try:
        result = eval(text)
    except Exception as e:
        pass
    else:
        await message.edit_text(f"{text}\n<b>result</b>: <code>{result}</code>")

    message.continue_propagation()
