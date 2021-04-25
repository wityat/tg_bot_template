import time
from datetime import datetime

from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified, TelegramAPIError

from tg_bot.db.models import Message, Chat, BotUser


async def delete_message_with_protect(bot, chat_id, msg_id):
    try:
        await bot.delete_message(chat_id, msg_id)
        return True
    except TelegramAPIError as e:
        return False


async def delete_info_message_for_user(bot: Bot, message_or_call, state: FSMContext):
    message = message_or_call if isinstance(message_or_call, types.Message) else message_or_call.message
    async with state.proxy() as data:
        prev_msg_id = data.get("prev_msg_id")
        if await delete_message_with_protect(bot, message.chat.id, prev_msg_id):
            data.update({"prev_msg_id": None})


async def edit_or_send_message(bot: Bot, message_or_call, state: FSMContext, parse_mode='HTML', kb=None, text=None,
                               video=None, photo=None, anim=None, chat_id=None, disable_web=True, chat=None, bot_user=None):
    message = message_or_call if isinstance(message_or_call, types.Message) else message_or_call.message
    msg: types.Message = None
    async with state.proxy() as data:
        prev_msg_id = data.get("prev_msg_id")

        if prev_msg_id and message.chat.id != message.from_user.id and not message.from_user.is_bot:
            msg_model, _ = await Message.get_or_create(tg_id=prev_msg_id,
                                                       chat=chat if chat else await Chat.get(tg_id=chat_id if chat_id else message.chat.id),
                                                       bot_user=bot_user if bot_user else await BotUser.get(tg_id=message.from_user.id))
        else:
            msg_model = None

        if await delete_message_with_protect(bot, message.chat.id if not chat_id else chat_id, prev_msg_id):
            data.update({"prev_msg_id": None})

        message_id = message.message_id
        # if message.from_user.id != bot.id:
        #     await delete_message_with_protect(bot, message.chat.id if not chat_id else chat_id, message.message_id)
        #     message_id = prev_msg_id
        # else:
        #     message_id = message.message_id
        if photo or anim or video:
            try:
                msg = await bot.edit_message_caption(
                    chat_id=message.chat.id if not chat_id else chat_id,
                    message_id=message_id,
                    caption=text,
                    parse_mode=parse_mode,
                    reply_markup=kb,
                )
            except Exception as e:
                await delete_message_with_protect(bot, message.chat.id, message_id)
                if type(e) == MessageNotModified:
                    pass
                elif anim:
                    msg = await bot.send_animation(
                        chat_id=message.chat.id if not chat_id else chat_id,
                        animation=anim,
                        caption=text,
                        parse_mode=parse_mode,
                        reply_markup=kb,
                    )
                elif video:
                    msg = await bot.send_video(
                        chat_id=message.chat.id if not chat_id else chat_id,
                        video=video,
                        caption=text,
                        parse_mode=parse_mode,
                        reply_markup=kb,
                    )
                else:
                    msg = await bot.send_photo(
                        chat_id=message.chat.id if not chat_id else chat_id,
                        photo=photo,
                        caption=text,
                        parse_mode=parse_mode,
                        reply_markup=kb,
                    )
        else:
            try:
                msg = await bot.edit_message_text(
                    chat_id=message.chat.id if not chat_id else chat_id,
                    message_id=message_id,
                    text=text,
                    parse_mode=parse_mode,
                    reply_markup=kb,
                    disable_web_page_preview=disable_web
                )
            except Exception as e:
                if type(e) == MessageNotModified:
                    pass
                else:
                    await delete_message_with_protect(bot, message.chat.id, message_id)
                    msg = await bot.send_message(
                        chat_id=message.chat.id if not chat_id else chat_id,
                        text=text,
                        parse_mode=parse_mode,
                        reply_markup=kb,
                        disable_web_page_preview=disable_web
                    )
        if msg:
            data.update({"prev_msg_id": msg.message_id})
            if msg_model:
                msg_model.tg_id = msg.message_id
                msg_model.created_at = datetime.now()
                msg_model.chat = chat if chat else await Chat.get(tg_id=chat_id if chat_id else message.chat.id)
                msg_model.bot_user = bot_user if bot_user else await BotUser.get(tg_id=message.from_user.id)
                await msg_model.save()
    return msg
