import asyncio
import logging
from aiogram import F
from functions import *
from config import *


logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN,parse_mode='HTML')
dp = Dispatcher()
dp.message.register(get_weather, F.location)
dp.callback_query.register(get_weather_today_coordinates, F.data == "data_today")
dp.callback_query.register(get_weather_five_days_coordinates, F.data == "data_five_days")
dp.callback_query.register(back,F.data == "back")
dp.message.register(get_weather_Moscow, F.text == "Получить погоду в Москве")
dp.message.register(get_weather_Tambov, F.text == "Получить погоду в Тамбове")
dp.message.register(start, F.text == "/start")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
