from aiogram import types


def mention(message: types.Message):
    return message.from_user.get_mention(message.new_chat_members[0].mention if message.new_chat_members else message.from_user.mention)

url_in_last_posts = lambda m, c: f"{mention(m)}, Такая ссылка уже была, дождитесь {c.posts_count} постов!"
