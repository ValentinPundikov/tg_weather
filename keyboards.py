from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

keyboard_1 = ReplyKeyboardBuilder()
keyboard_1.add(types.KeyboardButton(text="Получить погоду на местности",request_location=True),
               types.KeyboardButton(text="Получить погоду в Москве"),
               types.KeyboardButton(text="Получить погоду в Тамбове"))
keyboard_1.adjust(1)


keyboard_3 = InlineKeyboardBuilder()
keyboard_3.button(text="Получить погоду на сегодня", callback_data="data_today")
keyboard_3.button(text="Получить погоду на 5 дней", callback_data="data_five_days")
keyboard_3.button(text="Назад", callback_data="back")
keyboard_3.adjust(2,1)

