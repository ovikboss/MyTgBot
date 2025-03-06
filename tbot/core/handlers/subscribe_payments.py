import asyncio

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import  types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .router import router
from core.states.registration import Registration
from core.DB.db import  db
from  core.DB.models import User
from pay import create_payment, check_payment_status


@router.message(Command("subscribe"))
async def subscribe_user(message: types.Message, state: FSMContext):

    payment = await create_payment("100.00", "Оплата подписки на премиум-функции", message.from_user.id)
    print(payment)
    if payment:
        confirmation_url = payment.confirmation.confirmation_url  # Get payment link
        builder = InlineKeyboardBuilder()
        builder.button(text="Оплатить", url=confirmation_url)  # Create button with link
        await message.reply("Для оформления подписки, перейдите по ссылке, стоимость подписки 100 рублей:",
                                          reply_markup=builder.as_markup())
        await asyncio.sleep(60)
        text = check_payment_status(payment.id)
        if text == "succeeded":
            user_sub_change(message.from_user.id)
            await message.reply("Платеж совершен.")
    else:
        await message.reply("Произошла ошибка при создании платежа.")

def user_sub_change(user_id):
    db.change_user_subscribe(user_id)