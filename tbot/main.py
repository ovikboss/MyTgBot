import asyncio
from aiogram import  Dispatcher, Bot, types
from core.handlers.router import router
from core.middlewares.scheduler import SchedulerCustom

from core.dispatcher.create_dp import dp
from core.DB.db import db




from config import TOKEN
bot = Bot(token=TOKEN)

async def set_commands(bot: Bot):
    """Устанавливает команды для меню бота."""
    commands = [
        types.BotCommand(command="start", description="Начать работу с ботом"),
        types.BotCommand(command="help", description="Получить справку по командам"),
        types.BotCommand(command="register", description="Зарегистрироваться"),
        types.BotCommand(command="add_food", description="Добавить запись о приеме пищи"),
        types.BotCommand(command="show_today", description="Показать записи о еде за сегодня"),
        types.BotCommand(command="show_bmr", description="Показать уровень базального метаболизма"),
        types.BotCommand(command="food_info", description="Информация про кбжу продукта"),
        types.BotCommand(command="set_breakfast_time", description="Изменить время завтрака"),
        types.BotCommand(command="set_lunch_time", description="Изменить время обеда"),
        types.BotCommand(command="set_dinner_time", description="Изменить время ужина"),
        types.BotCommand(command="subscribe", description="Оплата подписки на бота"),
        types.BotCommand(command = "cancel", description = "Остановить ввод данных" ),
        types.BotCommand(command="change_message", description="включение/выключение уведомлений")
        # Добавьте другие команды по мере необходимости
    ]
    await bot.set_my_commands(commands)



async def main(starter):

    await set_commands(bot)

    await starter.start()
    starter.start_schedule(db)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':

    starter = SchedulerCustom(db=db, bot=bot)
    asyncio.run(main(starter))
