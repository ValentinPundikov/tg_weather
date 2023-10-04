from aiogram.filters.command import Command
import logging
import asyncio
from functions import *


dp = Dispatcher()
bot = Bot(token=TOKEN, parse_mode='HTML')
logging.basicConfig(level=logging.INFO)

dp.callback_query.register(get_weather_today_coordinates,F.data=="data_today")
dp.callback_query.register(get_weather_five_days_coordinates,F.data=="data_five_days")
dp.callback_query.register(back,F.data=="back")
dp.message.register(get_weather, F.text == "Получить погоду на местности")
dp.message.register(get_weather_Moscow, F.text == "Получить погоду в Москве")
dp.message.register(get_weather_Tambov(), F.text == "Получить погоду в Тамбове")
dp.message.register(start, F.text == "/start")

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
