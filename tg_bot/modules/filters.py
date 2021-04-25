import typing
from aiogram.dispatcher.filters import BoundFilter, Regexp
from aiogram import types
from aiogram.dispatcher.handler import ctx_data

from ..db.models import BotUser
from ..load_all import bot


class Button(BoundFilter):
    def __init__(self, key, contains=False, work_in_group=False):
        self.key = key
        self.contains = contains
        self.work_in_group = work_in_group

    async def check(self, message: types.Message) -> bool:
        if isinstance(message, types.Message):
            if self.contains:
                return self.key in message.text
            else:
                return message.text == self.key
        elif isinstance(message, types.CallbackQuery):
            if self.contains:
                return self.key in message.data
            else:
                return self.key == message.data


class AddedByAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        data = ctx_data.get()
        print(data["bot_user"])
        return data["bot_user"].is_admin


class IsBotNewChatMember(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        flag = False
        if members := message.__getattribute__("new_chat_members"):
            me = await bot.get_me()
            for member in members:
                flag = True if member.id == me.id else flag
        return flag


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message) -> typing.Union[typing.Dict[str, BotUser], bool]:
        data = ctx_data.get()
        print(data["bot_user"])
        return data if data["bot_user"].is_admin else False


class FromChat(BoundFilter):
    async def check(self, message_or_call: [types.Message, types.CallbackQuery]) -> bool:
        if isinstance(message_or_call, types.Message):
            return not message_or_call.chat.id == message_or_call.from_user.id
        elif isinstance(message_or_call, types.CallbackQuery):
            return not message_or_call.message.chat.id == message_or_call.message.from_user.id

