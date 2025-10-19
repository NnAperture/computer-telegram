import telebot
from handler.config import config

bot = telebot.TeleBot

screen_id = 0
delay = config["screen"]["delay"]
DELAY_MULTIPLICATOR = config["screen"]["delay_step"]
speed = config["screen"]["speed"]
command_delete = config["screen"]["command_delete"]
cursor_draw = config["screen"]["cursor_draw"]
screenshot_resize = config["screen"]["screenshot_resize"]

path = config["FS"]["path"]

work = config["addictive"]["work"]
chat = config["addictive"]["your_chat"]
