from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import  types

from .router import router
from core.DB.db import  db
from core.checksubscribe.checker import subscription_required


@router.message(Command("change_message"))
async def change_command(message: types.Message):
    user_id  = message.from_user.id
    mess = db.change_message_on(user_id)
    await message.reply(mess)
