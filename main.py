import telebot
import requests
import json

bot = telebot.TeleBot('7557624575:AAEEj79BO0T5y505m3rQcRjIZfM8Pc9ocYc')
API = '4ced331457796d67ffddddce9ccb0190'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привіт! Я бот, який надає прогноз погоди. Будьласка вкажи місто (або населений пункт)')


@bot.message_handler(content_types=['text'])
def get_weather(message):
     city = message.text.strip().lower()
     res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
     data = json.loads(res.text)
     bot.reply_to(message, f'Погода сьогодні: {data["main"]["temp"]}')

bot.polling(none_stop=True)
