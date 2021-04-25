import os
import asyncio

from dotenv import load_dotenv

load_dotenv()
envs = os.environ

loop = asyncio.get_event_loop()

TG_TOKEN = envs.get("TG_TOKEN")
REDIS_HOST = envs.get("REDIS_HOST")
REDIS_PORT = int(envs.get("REDIS_PORT"))
REDIS_PASS = envs.get("REDIS_PASS")

DATABASE = envs.get("DATABASE")
PG_DB = envs.get("POSTGRES_DB")
PG_USER = envs.get("POSTGRES_USER")
PG_PASS = envs.get("POSTGRES_PASSWORD")
PG_HOST = envs.get("POSTGRES_HOST")
PG_PORT = envs.get("POSTGRES_PORT")

TORTOISE_ORM = {
    "connections": {"default": f'{DATABASE}://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}'},
    "apps": {
        "models": {
            "models": ["aerich.models", "tg_bot.db.models"],
            "default_connection": "default",
        },
    },
}
