import telebot
from telebot import types
import webbrowser
import sqlite3

bot = telebot.TeleBot('7831683127:AAGGh6By1hTbDbvgsAYiCSx-ORVnwVQKp1M')
name = None


@bot.message_handler(commands=['start'])
def main(message):
    conn = sqlite3.connect('db.sql')
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрируем! Введи свое имя')
    bot.register_next_step_handler(message, user_name)
    # markup = types.ReplyKeyboardMarkup()
    # btn1 = types.KeyboardButton('Перейти на сайт')  # Создание кнопки
    # markup.row(btn1)
    # btn2 = types.KeyboardButton('Удалить фото')  # Создание кнопки
    # btn3 = types.KeyboardButton('Изменить фото')  # Создание кнопки
    # markup.row(btn2, btn3)
    # file = open('./photo.png', 'rb')
    # bot.send_photo(message.chat.id, file, reply_markup=markup)
    # # bot.reply_to(message, 'Неплохое фото!', reply_markup=markup)
    # bot.send_message(message.chat.id, 'Привет', reply_markup=markup)
    # bot.register_next_step_handler(message, on_click)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('db.sql')
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователей', callback_data='list'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован', reply_markup=markup)


def on_click(message):
    if message.text == 'Перейти на сайт':
        bot.send_message(message.chat.id, 'Website is open')
    elif message.text == 'Удалить фото':
        bot.send_message(message.chat.id, 'Delete')


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://www.accuweather.com/')


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://vk.ru')  # Создание кнопки
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')  # Создание кнопки
    btn3 = types.InlineKeyboardButton('Изменить фото', callback_data='edit')  # Создание кнопки
    markup.row(btn2, btn3)
    bot.reply_to(message, 'Неплохое фото!', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, 'Help information')


@bot.message_handler()
def info(message):
    if message.text.lower == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('db.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    info = ''
    for el in users:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n'

    cur.close()
    conn.close()
    bot.send_message(call.message.chat.id, info)


bot.polling(none_stop=True)
