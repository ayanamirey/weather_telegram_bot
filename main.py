import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import aioschedule

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды\nПример: /pg tashkent")


@dp.message_handler(commands=['pg'])
async def get_weather(message: types.Message):
    print()
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F328',
        'Smoke': 'Туман \U0001F328',
    }

    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text.split()[-1]}&appid={open_weather_token}&units=metric'
        )
        data = r.json()

        city = data['name']
        cur_weather = data['main']['temp']

        weather_descr = data['weather'][0]['main']
        if weather_descr in code_to_smile:
            wd = code_to_smile[weather_descr]
        else:
            wd = 'Посмотри в окно, не пойму что там за погода'

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        await message.reply(f'***{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}***\n'
                            f'Погода в городе: {city}\nТемпература: {cur_weather} C° {wd}\n'
                            f'Влажность: {humidity} %\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/c\n'
                            f'Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n'
                            f'***Хорошего дня!***')

    except Exception as e:
        await message.reply('\U00002620 Проверьте название города \U00002620')


if __name__ == '__main__':
    executor.start_polling(dp)
