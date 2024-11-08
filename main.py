import telebot

bot = telebot.TeleBot('7557624575:AAEEj79BO0T5y505m3rQcRjIZfM8Pc9ocYc')

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Привіт! Я бот, який надає прогноз погоди')
