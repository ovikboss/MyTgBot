import asyncio
import time
import logging
from importlib.metadata import always_iterable

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.middlewares.breakfast_daily_message import send_meal_reminder

from core.DB.models import User



class SchedulerCustom:
    _scheduler_started = False
    scheduler = AsyncIOScheduler()
    bot = None
    def __init__(self,db, bot):
        self.db = db
        SchedulerCustom.bot = bot
        SchedulerCustom._scheduler_started = True
        print("create", __name__, id(self.scheduler))


    def start_schedule(self, db):
        """Создает или обновляет расписание напоминаний для каждого пользователя."""
        users = db.get_show_daily()
        for user in users:
            if user.subscription:
                self.update_user_reminders(  user,"завтрак", 0.3)
                self.update_user_reminders(  user, "обед", 0.4)
                self.update_user_reminders(  user, "ужин", 0.3)

    async def start(self):
        await asyncio.sleep(0)
        if SchedulerCustom._scheduler_started:
            self.scheduler.start()
            print("started", id(self.scheduler))
        else:
            print("no start",id(self.scheduler))



    @classmethod
    def update_user_reminders(cls, user: User, meal_type: str, percent: float):
            """Обновляет расписание напоминаний для конкретного приема пищи пользователя."""
            job_id = f"{meal_type}_{user.id}"
            # Удаляем старую задачу, если она есть
            if cls.scheduler.get_job(job_id):
                print(f"Задача {job_id} успешно удалена в APScheduler.{id(cls.scheduler)}")
                cls.scheduler.remove_job(job_id)
            # Добавляем новую задачу
            
            if meal_type == "завтрак":
                reminder_time = user.breakfast_time
            elif meal_type == "обед":
                reminder_time = user.lunch_time
            elif meal_type == "ужин":
                reminder_time = user.dinner_time
            else:
                return  # Неизвестный тип приема пищи
            cls.scheduler.add_job(
                send_meal_reminder,
                trigger="cron",
                hour=reminder_time.hour,
                minute=reminder_time.minute,
                args=(cls.bot, meal_type, percent, user.id),
                id=job_id
            )
            print(cls.scheduler.get_job(job_id))







