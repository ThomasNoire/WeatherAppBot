# import telebot
# import requests
# import json
#
# bot = telebot.TeleBot('7557624575:AAEEj79BO0T5y505m3rQcRjIZfM8Pc9ocYc')
# API = '4ced331457796d67ffddddce9ccb0190'
#
# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(message.chat.id, 'Привіт! Я бот, який надає прогноз погоди. Будьласка вкажи місто (або населений пункт)')
#
#
# @bot.message_handler(content_types=['text'])
# def get_weather(message):
#      city = message.text.strip().lower()
#      res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
#      data = json.loads(res.text)
#      bot.reply_to(message, f'Погода сьогодні: {data["main"]["temp"]}')
#
# bot.polling(none_stop=True)

import telebot
import requests
from telebot import types

API_TOKEN = '7557624575:AAEEj79BO0T5y505m3rQcRjIZfM8Pc9ocYc'
API_KEY = '4ced331457796d67ffddddce9ccb0190'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

bot = telebot.TeleBot(API_TOKEN)

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'uk'
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()


def get_forecast(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',  # Температура в градусах Цельсія
        'lang': 'uk'  # Мова відповіді
    }
    response = requests.get(FORECAST_URL, params=params)
    return response.json()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Напишіть назву міста, щоб дізнатися прогноз погоди.")


@bot.message_handler(func=lambda message: True)
def send_weather(message):
    city = message.text
    weather_data = get_weather(city)

    if weather_data.get('cod') != 200:
        bot.reply_to(message, f"Не вдалося знайти місто: {city}. Спробуйте ще раз.")
    else:
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        temp_min = weather_data['main']['temp_min']
        temp_max = weather_data['main']['temp_max']

        weather_info = f"Погода в місті {city}:\n" \
                       f"Температура: {temp}°C\n" \
                       f"Опис: {description}\n" \
                       f"Температура від {temp_min}°C до {temp_max}°C"

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        item1 = types.KeyboardButton("Прогноз на завтра")
        item2 = types.KeyboardButton("Прогноз на наступні 5 днів")
        markup.add(item1, item2)

        bot.send_message(message.chat.id, weather_info, reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == "Прогноз на завтра")
def send_tomorrow_forecast(message):
    city = message.text
    forecast_data = get_forecast(city)

    tomorrow_forecast = forecast_data['list'][1]
    temp = tomorrow_forecast['main']['temp']
    description = tomorrow_forecast['weather'][0]['description']

    forecast_info = f"Прогноз на завтра:\nТемпература: {temp}°C\nОпис: {description}"
    bot.send_message(message.chat.id, forecast_info)


@bot.message_handler(func=lambda message: message.text == "Прогноз на наступні 5 днів")
def send_5day_forecast(message):
    city = message.text
    forecast_data = get_forecast(city)

    forecast_info = "Прогноз на наступні 5 днів:\n"
    for i in range(0, 40, 8):
        day_forecast = forecast_data['list'][i]
        temp = day_forecast['main']['temp']
        description = day_forecast['weather'][0]['description']
        time = day_forecast['dt_txt']

        forecast_info += f"{time}: {temp}°C, {description}\n"

    bot.send_message(message.chat.id, forecast_info)


bot.polling(none_stop=True)

