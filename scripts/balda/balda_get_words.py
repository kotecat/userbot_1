import aiohttp
from aiohttp import ClientSession
from .types_balda import Field, FieldRow
import json


class BaldaApi:
    def __init__(self,
                 url: str = "https://poncy.ru/balda/server.wsgi",
                 headers=None):
        if headers is None:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.URL = url
        self.headers = headers


    async def send_query_get_words(self, field: Field):
        data = {}
        for y, row in enumerate(field.rows):
            for x, char in enumerate(row.chars):
                data[f"cell{y+1}{x+1}"] = char.upper() or ""
        data["used_words"] = "Л"
        data["boardsize"] = str(field.size)

        async with ClientSession() as session:
            async with session.post(url=self.URL, data=data, headers=self.headers) as resp:
                return await resp.text()

    async def get_words(self, field: Field):
        mono_words = await self.send_query_get_words(field)
        words = set()
        for w in json.loads(str(mono_words).replace(" ", "")):
            words.add(w[0])
        words_list = list(words)
        words_list.sort(key=lambda word: len(word), reverse=True)
        return words_list
