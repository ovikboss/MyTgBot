import functools
import logging
import asyncio
from datetime import datetime
from core.DB.db import db

from aiogram import types


def is_subscribed(user_id: int, bot) -> bool:
    """Проверяет, подписан ли пользователь на все необходимые каналы/группы."""
    try:
        check = db.get_user_subscribe(str(user_id))
        if datetime.now() < check[0]:
            print(check)
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Ошибка при проверке подписки: {e}")
        return False # Считаем, что не подписан, если произошла ошибка

def subscription_required(func):
    """Декоратор для проверки подписки пользователя."""
    @functools.wraps(func)  # Сохраняет метаданные исходной функции
    async def wrapper(message: types.Message, *args, **kwargs):
        bot = kwargs['bot'] if 'bot' in kwargs else message.bot # Передача bot

        user_id = message.from_user.id
        is_member = is_subscribed(user_id, bot)
        if is_member:
            return  await func(message, *args, **kwargs)  # Вызываем функцию, если пользователь подписан
        else:
            await message.reply("Для использования этой команды необходимо оплатить платную подписку.  /subscribe")
            # или предложите другой способ получения подписки
    return wrapper