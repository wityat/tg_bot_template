import asyncio
from aiogram import executor
from tortoise import Tortoise
import aioschedule

from tg_bot.load_all import bot


async def on_shutdown(dp):
    await bot.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    await Tortoise.close_connections()
    # inst_bot.logout()


async def on_startup(dp):
    print("!!!!!!!!!!!!!1STARTING!!!!!!!!!!!!!!!!!!")
    asyncio.create_task(scheduler())


async def scheduler():
    # aioschedule.every(1).minutes.do(delete_old_tasks)
    # aioschedule.every(1).minutes.do(delete_old_messages)
    # aioschedule.every(1).minutes.do(send_autoposts_by_datetime)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

from tg_bot.dialogs.chats.handlers import dp
from tg_bot.dialogs.admin.handlers import dp
executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup, skip_updates=True)
