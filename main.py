import telebot

bot = telebot.TeleBot('7557624575:AAEEj79BO0T5y505m3rQcRjIZfM8Pc9ocYc')
API = '4ced331457796d67ffddddce9ccb0190'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привіт! Я бот, який надає прогноз погоди')
@bot.message_handler(content_types=['text'])
def get_weather(message):
 city = message.text.strip().lower()


bot.polling(none_stop=True)

# if __name__ == '__main__':
#     bot.infinity_polling()