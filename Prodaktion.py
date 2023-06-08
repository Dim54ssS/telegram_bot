import subprocess
import time
import pyowm
import telebot
from telebot import types
owm = pyowm.OWM('26f1c0c1f4e07a2aedfe989325c14b90', language='ua')
token='6244102409:AAE1gj2p0XsNonQ6F5HQBc_7u-nv5nR0x0U'

bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("⚡ Світло вдома є?")
    btn2 = types.KeyboardButton("Погода")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Привіт, я твій новий бот для перевірки світла та погоди", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "⚡ Світло вдома є?":
        output = subprocess.run(['./svet.sh'], capture_output=True, text=True).stdout.strip()
        bot.send_message(message.chat.id, text=output)
    elif message.text == "Погода":
        markup = types.InlineKeyboardMarkup()
        cities = ['Київ', 'Попельня', 'Залісці']
        for city in cities:
            btn = types.InlineKeyboardButton(city, callback_data=f'weather-{city}')
            markup.add(btn)
        bot.send_message(message.chat.id, text="Обери місто:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="Нуууу, таке я поки що не вмію...")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.message:
        if call.data.startswith('weather-'):
            city = call.data.split('-')[1]
            try:
                observation = owm.weather_at_place(city)
                w = observation.get_weather()
                temperature = w.get_temperature('celsius')['temp']
                description = w.get_detailed_status()
                bot.send_message(call.message.chat.id, f"Погода в місті {city}:\nТемпература: {temperature}°C\n{description}")
            except:
                bot.send_message(call.message.chat.id, f"Не вдалось отримати погоду для міста {city}. Спробуйте ще раз.")
            bot.edit_message_reply_markup(call.message.chat)
bot.polling(none_stop=True)

