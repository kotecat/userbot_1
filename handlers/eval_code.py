from pyrogram import types, filters, Client
from loader import bot
from simple_filters import app_admins_filter

# imports for eval
from math import *
from base64 import *
from random import *
import asyncio
import datetime


api = bot
template = "> <code>{text}</code>\n- - - - - - = (<b>{result_type}</b>) = - - - - - -\n<pre>{result_body}</pre>"


@bot.on_message(app_admins_filter & filters.command(["e", "ne"], ["/", "!"]), group=-1)
async def cmd_eval(client: Client, message: types.Message):
    text = message.text or message.caption
    m = msg = message
    r = reply = message.reply_to_message
    me = client.me

    if not text:
        return
    if len(text.split(" ")) <= 1:
        return

    text_for_eval = " ".join(text.split(" ")[1:])

    is_input = message.command[0].lower().strip() != "ne"

    try:
        try:
            result_type = "result"
            eval_result = asyncio.create_task(eval(text_for_eval, globals(), locals()))
            await eval_result
            result = eval_result.result()
            result = str(result) if is_input else "OK"
            await message.edit_text(template.format(text=text, result_type=result_type, result_body=result))

        except SyntaxError as e:
            result_type = "result"
            t = asyncio.create_task(exec(text_for_eval, globals(), locals()))
            await t
            result = t.result()
            result = str(result) if is_input else "OK"
            await message.edit_text(template.format(text=text, result_type=result_type, result_body=result))

    except Exception as e:
        result_type = "error"
        await message.edit_text(template.format(text=text, result_type=result_type, result_body=str(e)))

    message.continue_propagation()


@bot.on_message(app_admins_filter, group=-2)
async def try_eval(client: Client, message: types.Message):
    text = message.text
    m = msg = message
    r = reply = message.reply_to_message
    me = client.me

    text_for_eval = text

    try:
        try:
            eval_result = eval(text_for_eval, globals(), locals())
        except Exception as e:
            pass
        else:
            result_type = "result"
            await message.edit_text(template.format(text=text, result_type=result_type, result_body=str(eval_result)))

    except Exception as e:
        result_type = "error"
        await message.edit_text(template.format(text=text, result_type=result_type, result_body=str(e)))

    message.continue_propagation()
