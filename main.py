import json

import telebot
import requests

bot = telebot.TeleBot('7831683127:AAGGh6By1hTbDbvgsAYiCSx-ORVnwVQKp1M')
API = '2e453531935987df0e6f868cd6bc946b'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} ! Напиши название города')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    # city = message.text.strip().lower()
    lat = message.text.strip().lower()
    lon = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API}&units=metric')
    data = json.loads(res.text)
    bot.reply_to(message, f'Сейчас погода: {data["main"]["temp"]}')


bot.polling(none_stop=True)
