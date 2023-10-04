from aiogram.filters.command import Command
import logging
from aiogram import F
from aiogram.fsm.storage.memory import MemoryStorage
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

ADMIN_ID = ['']
OPENWEATHERMAP_API_KEY = "3cccaf8c64a1057516f02c3cc59a9cad"

storage = MemoryStorage()
lon = ""
lat = ""

dp = Dispatcher()
bot = Bot(token='',parse_mode='HTML')


@dp.message(Command("start"))
async def cmd_name(message: types.Message) -> None:

    if str(message.from_user.id) in str(ADMIN_ID):
        builder = ReplyKeyboardBuilder()
        builder.row(
            types.KeyboardButton(text="Информация", request_location=True)
        )
        await message.answer(f"Привет, <b>{str(message.from_user.first_name)}</b>", reply_markup=builder.as_markup())
    else:
        await message.answer("ERROR")

@dp.message(F.location)
async def Data(message: Message):
    global lon, lat
    lon = message.location.longitude
    lat = message.location.latitude

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Погода на сегодня",
        callback_data="weather_today")
    )
    builder.add(types.InlineKeyboardButton(
        text="Погода на пять дней вперед",
        callback_data="weather_five"))
    await message.answer('Выберите пункт', reply_markup=builder.as_markup())


@dp.callback_query(F.data == "weather_today")
async def get_weather(callback: CallbackQuery):

    api_url = f'http://api.openweathermap.org/data/2.5/weather?lang=ru&lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}&units=metric'
    response = requests.get(api_url)
    data = response.json()
    if data['cod'] != 200:
        await callback.answer(f'Не удалось получить информацию о погоде на сегодня. Код ошибки: {data["cod"]}')
    else:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        await callback.message.answer(f'Сегодня:\nПогода: <b>{weather_description}</b>\nТемпература: <b>{temperature}</b>°C')


@dp.callback_query(F.data == "weather_five")
async def get_weather(callback: CallbackQuery):
    base_url = f'http://api.openweathermap.org/data/2.5/forecast'
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric",
        "cnt": 5,
        "lang": "RU"

    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if response.status_code == 200:
            forecast = data["list"]
            for day in forecast:
                date = day["dt_txt"]
                temp = day["main"]["temp"]
                description = day["weather"][0]["description"]
                await callback.message.answer(f"Дата: <b>{date}</b>, Температура: <b>{temp}</b>°C, Описание: <b>{description}</b>")
        else:
            await callback.message.answer('Не удалось получить прогноз погоды на 5 дней. Пожалуйста, попробуйте позже.')
    except Exception as e:
        await callback.message.answer(f"Произошла ошибка: {str(e)}")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
