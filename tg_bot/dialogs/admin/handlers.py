from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from ...db.models import BotUser
from ...load_all import dp, bot
from . import texts, keyboards
from ...modules.edit_or_send_message import edit_or_send_message
from ...modules.filters import Button, IsBotNewChatMember, AddedByAdmin, FromChat, IsAdmin


class States(StatesGroup):
    posts_count = State()


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message):
    b, _ = await BotUser.get_or_create(tg_id=message.from_user.id)
    b.is_admin = True
    await b.save()
