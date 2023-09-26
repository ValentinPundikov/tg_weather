import requests
from aiogram.types import Message, CallbackQuery
import sqlite3
from sqldata import *

from keyboards import keyboard_1, keyboard_3
from aiogram import Bot, Dispatcher, types, F
from config import *



async def start(message: Message):
    if str(message.from_user.id) in str(ADMIN_ID):
        createDB()
        check_user(message.from_user.id)
        await message.answer(f"Приветствую тебя, Администратор!\n<b>Твой ID: {message.from_user.id}</b>", reply_markup=keyboard_1.as_markup())
    else:
        await message.answer("Доступ запрещен!", reply_markup=keyboard_1.as_markup())

async def get_weather(message: Message):
    await message.answer("Выбери опцию:", reply_markup=keyboard_3.as_markup())
    lat = message.location.latitude
    lon = message.location.longitude
    add_lat_lon(message.from_user.id,lat,lon)

async def get_weather_today_coordinates(callback: CallbackQuery):
    lat = get_lat(callback.from_user.id)
    lon = get_lon(callback.from_user.id)
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'lat': lat,
        'lon': lon,
        'units': 'metric',
        'appid': OPENWEATHERMAP_API_KEY,
        'lang': 'ru'
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        city_name = data['name']
        country = data['sys']['country']
        await callback.message.answer(f'Погода в {city_name}, {country}:\nСейчас {weather_description}\nТемпература: {temperature}°C\nВлажность: {humidity}%\nСкорость ветра: {wind_speed} м/с',reply_markup=keyboard_1.as_markup())
    else:
        await callback.message.answer("Не удалось получить данные о погоде.",reply_markup=keyboard_1.as_markup())

async def get_weather_five_days_coordinates(callback: types.CallbackQuery):
    lat = get_lat(callback.from_user.id)
    lon = get_lon(callback.from_user.id)
    base_url = 'http://api.openweathermap.org/data/2.5/forecast'
    params = {
        'lat': lat,
        'lon': lon,
        'units': 'metric',
        'appid': OPENWEATHERMAP_API_KEY,
        'lang': 'ru',
        'cnt': 10  # Получаем данные на 5 дней с интервалом в 3 часа (5 дней * 8 отчетов в день)
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        forecast_list = data['list']
        weather_forecast = []

        for entry in forecast_list:
            time = entry['dt_txt']
            weather_description = entry['weather'][0]['description']
            temperature = entry['main']['temp']
            humidity = entry['main']['humidity']
            wind_speed = entry['wind']['speed']
            weather_forecast.append({
                'time': time,
                'description': weather_description,
                'temperature': temperature,
                'humidity': humidity,
                'wind_speed': wind_speed
            })

        for data in weather_forecast:
            await callback.message.answer(
                f"Время: {data['time']}\nПогода: {data['description']}\nТемпература: {data['temperature']}°C\nВлажность: {data['humidity']}%\nСкорость ветра: {data['wind_speed']} м/с")
    else:
        await callback.message.answer("Не удалось получить данные о погоде.", reply_markup=keyboard_1.as_markup())

async def back(callback: types.CallbackQuery):
    await callback.message.answer("Главное меню:",reply_markup=keyboard_1.as_markup())
async def get_weather_Moscow(message: Message):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': 'Moscow',
        'units': 'metric',
        'appid': OPENWEATHERMAP_API_KEY,
        'lang': 'ru'
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        city_name = data['name']
        country = data['sys']['country']
        await message.answer(f'Погода в {city_name}, {country}:\nСегодня {weather_description}\nТемпература: {temperature}°C\nВлажность: {humidity}%\nСкорость ветра: {wind_speed} м/с',reply_markup=keyboard_1.as_markup())
    else:
        await message.answer('Не удалось получить данные о погоде в Москве.')


async def get_weather_Tambov(message: Message):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': 'Tambov',
        'units': 'metric',
        'appid': OPENWEATHERMAP_API_KEY,
        'lang': 'ru'
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        city_name = data['name']
        country = data['sys']['country']
        await message.answer(
            f'Погода в {city_name}, {country}:\nСегодня {weather_description}\nТемпература: {temperature}°C\nВлажность: {humidity}%\nСкорость ветра: {wind_speed} м/с',reply_markup=keyboard_1.as_markup())
    else:
        await message.answer('Не удалось получить данные о погоде в Тамбове.')


