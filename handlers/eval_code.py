from pyrogram import types, filters, Client, raw
from loader import bot
from simple_filters import app_admins_filter
from typing import List, Dict

# imports for eval
from math import *
from base64 import *
from random import *
import asyncio
import datetime
import typing


api = bot
template = "> <code>{text}</code>\n- - - - - - = (<b>{result_type}</b>) = - - - - - -\n<pre>{result_body}</pre>"
template_search = "> <code>{text}</code>\n- - - - - - = (<b>{result_type}</b>) = - - - - - -\n{result_body}"
CORO_WARN = """a coroutine was expected, got"""


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
        try:  # try eval
            result_type = "result"
            obj = eval(text_for_eval, globals(), locals())
            if asyncio.iscoroutine(obj):
                eval_result = asyncio.create_task(obj)
                await eval_result
                result = eval_result.result()
            else:
                result = obj

        except SyntaxError as e:  # try exec
            result_type = "result"
            obj = exec(text_for_eval, globals(), locals())
            if asyncio.iscoroutine(obj):
                t = asyncio.create_task(obj)
                await t
                result = t.result()
            else:
                result = obj

        # success
        result = str(result) if is_input else "OK"
        if result.startswith(CORO_WARN):
            result = result.replace(CORO_WARN, "", 1)
        await message.edit_text(template.format(text=text, result_type=result_type, result_body=result))

    except Exception as e:
        result_type = "error2"
        await message.edit_text(template.format(text=text, result_type=result_type, result_body=str(e)[:1024]))

    message.continue_propagation()


@bot.on_message(app_admins_filter & filters.command(["s"], ["/", "!"]), group=-1)
async def obj_parser(client: Client, message: types.Message):
    text = message.text or message.caption or ""

    text = message.text or message.caption
    m = msg = message
    r = reply = message.reply_to_message
    me = client.me

    try:
        try:
            if len(message.command) == 2:
                obj = message.command[-1]
                query = ""
            elif len(message.command) >= 3:
                obj = message.command[-2]
                query = message.command[-1]
            else:
                raise ValueError("try /s obj query")

            attrs: List[str] = eval(f"dir({obj})", globals(), locals())
        except Exception as e:
            await message.edit_text(template.format(text=text, result_type="error", result_body=str(e)))
            return

        result = []
        for attr in attrs:
            if attr.startswith("__"):
                continue
            if query in attr:
                result.append("• " + attr.replace(
                    query,
                    f"<b>{query}</b>",
                    1
                ))

        await message.edit_text(template_search.format(text=text, result_type="result", result_body="\n" + "\n".join(result)))

    except Exception as e:
        await message.edit_text(template.format(text=text, result_type="error", result_body=str(e)))


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
