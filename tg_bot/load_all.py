import logging

from tortoise import Tortoise
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from .modules.middlewares import GetUserMiddleware
from .config import *


storage = RedisStorage2(host=REDIS_HOST,
                        port=REDIS_PORT,
                        password=REDIS_PASS if REDIS_PASS else None)
bot = Bot(token=TG_TOKEN, parse_mode="HTML", loop=loop)
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.DEBUG)

dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(GetUserMiddleware())

loop.run_until_complete(Tortoise.init(config=TORTOISE_ORM))

loop.run_until_complete(Tortoise.generate_schemas())


