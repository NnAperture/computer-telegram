import telebot
from dotenv import load_dotenv
from handler.config import config
from handler import globals as gl
from handler.movRel import *
import os

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = telebot.TeleBot(TOKEN)
print()
print("active")
try:
    bot.send_message(gl.chat, 'Hi')
except:
    pass
commands = [
    telebot.types.BotCommand('/help', 'Text comand list'),
    telebot.types.BotCommand('/ping', 'Ping (useless, but you can check if your bot works)'),
    telebot.types.BotCommand('/screen', 'Activate screenmove mode'),
    telebot.types.BotCommand('/shutdown', 'Shut your computer down'),
    telebot.types.BotCommand('/exit', 'Exit bot'),
]
bot.set_my_commands(commands)
gl.bot = bot


import handler.handle
bot.polling()
while True:
    try:
        bot.polling()
    except Exception as e:
        try:
            bot.send_message(gl.chat, str(e))
        except:
            pass