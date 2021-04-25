from tortoise.models import Model
from tortoise import fields
from enum import IntEnum

from tg_bot.config import loop


class VIP(Model):
    chat = fields.ForeignKeyField("models.Chat", "vips")
    bot_user = fields.ForeignKeyField("models.BotUser", "where_vip")
    until = fields.DatetimeField()
    count_posts_per_day = fields.IntField(default=0)
    count_used_posts_today = fields.IntField(default=0)


class BotUser(Model):
    tg_id = fields.BigIntField(default=0)
    username_or_full_name = fields.CharField(max_length=200, default="")
    inst_id = fields.CharField(max_length=25, default=0)
    is_admin = fields.BooleanField(default=False)
    chats = fields.ManyToManyField("models.Chat", "bot_users")
    spam_counter = fields.IntField(default=0)

    def __str__(self):
        return str(self.username_or_full_name)

    async def is_vip(self, chat):
        await self.fetch_related("where_vip")
        for vip in self.where_vip:
            await vip.fetch_related("chat")
            if vip.chat == chat:
                return vip
        return False


class Task(Model):
    bot_user = fields.ForeignKeyField("models.BotUser", "tasks")
    post = fields.ForeignKeyField("models.InstPost", "tasks")
    is_liked = fields.BooleanField(default=False)
    is_commented = fields.BooleanField(default=False)
    is_sub = fields.BooleanField(default=False)
    is_saved = fields.BooleanField(default=False)
    started_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        x = []
        if not self.is_liked and self.post.chat.check_like:
            x.append('Лайк')
        if not self.is_commented and self.post.chat.check_comment:
            x.append('Комментарий')
        if not self.is_saved and self.post.chat.check_save:
            x.append('Сохранение')
        if not self.is_sub and self.post.chat.check_sub:
            x.append('Подписка')

        return y + f"\n{self.post.url}" if (y := ", ".join(x)) else ''


class AutopostingFunction(IntEnum):
    for_date = 0
    for_cycle = 1
    for_posts = 2


class Chat(Model):
    tg_id = fields.BigIntField(default=0)
    title = fields.CharField(max_length=200, default="")
    posts_count = fields.IntField(default=5)
    minutes_for_tasks = fields.IntField(default=15)
    count_words = fields.IntField(default=0)
    count_letters = fields.IntField(default=0)
    count_spam_posts_allowed = fields.IntField(default=3)

    individual_greeting = fields.BooleanField(default=False)
    individual_greeting_text = fields.TextField(default="")
    blocking_bots = fields.BooleanField(default=True)
    autoposting = fields.IntEnumField(AutopostingFunction, default=AutopostingFunction.for_posts)

    check_like = fields.BooleanField(default=True)
    check_comment = fields.BooleanField(default=True)
    check_save = fields.BooleanField(default=True)
    check_sub = fields.BooleanField(default=False)


class InstPost(Model):
    url = fields.TextField(default="")
    inst_id = fields.CharField(max_length=25, default=0)
    chat = fields.ForeignKeyField("models.Chat", "inst_posts")

    def __str__(self):
        return self.url


class Like(Model):
    user_inst_id = fields.CharField(max_length=25, default="")
    post = fields.ForeignKeyField("models.InstPost", "likes")


class Comment(Model):
    user_inst_id = fields.CharField(max_length=25, default="")
    text = fields.TextField(default="")
    post = fields.ForeignKeyField("models.InstPost", "comments")


class InstAcc(Model):
    username = fields.CharField(default="", max_length=255)
    password = fields.CharField(default="", max_length=255)

    def __str__(self):
        return f"{self.username} {self.password}"


class Message(Model):
    tg_id = fields.CharField(max_length=50)
    created_at = fields.DatetimeField(default=None, null=True, blank=True)
    chat = fields.ForeignKeyField("models.Chat", "messages")
    bot_user = fields.ForeignKeyField("models.BotUser", "messages")


class Autopost(Model):
    chat = fields.ForeignKeyField("models.Chat", "autoposts")
    count_cycles = fields.IntField(null=True, blank=True)
    difference_count_cycles = fields.IntField(null=True, blank=True)
    inst_post = fields.ForeignKeyField("models.InstPost", null=True, blank=True)
    datetime = fields.DatetimeField(null=True, blank=True)
    text = fields.TextField()
