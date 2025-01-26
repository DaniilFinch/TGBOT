from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import asyncio
import requests

TOKEN = '7920616299:AAEwYr3yCJvUH7b_mGCRZoJGArbvHF-v__0'
bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer('Привет! Чтобы получить погоду пришлите мне название города.')


@dp.message(F.text)
async def get_weather(message: types.Message):
    city = message.text
    try:
       url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid=462ccc63e0ace635776db398a3977356'
       weather_data = requests.get(url).json()

       temperature = weather_data['main']['temp']
       temperature_feels = weather_data['main']['feels_like']
       wind_speed = weather_data['wind']['speed']
       cloud_cover = weather_data['weather'][0]['description']
       humidity = weather_data['main']['humidity']

       await message.answer(f'Температура воздуха: {temperature}°C\n'
                            f'Ощущается как: {temperature_feels}°C\n'
                            f'Ветер: {wind_speed} м/c\n'
                            f'Облачность: {cloud_cover}\n'
                            f'Влажность: {humidity}%')
    except KeyError:
        await message.answer(f'Не удалось определить город: {city}')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
