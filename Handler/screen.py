import keyboard
import pyautogui
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from PIL import Image, ImageDraw
from . import globals as gl
import io
from handler.movRel import *
import threading
from handler.config import set_chat
bot = gl.bot

@bot.message_handler(commands=['screen'])
def screen(message=None, chat=None, id=None):
    if(message != None):
        print(message.chat.id)
        if(gl.chat != message.chat.id):
            set_chat(message.chat.id)
            gl.chat = message.chat.id
    try:
        screenshot = pyautogui.screenshot()
        if gl.cursor_draw:
            draw = ImageDraw.Draw(screenshot)
            x, y = pyautogui.position()
            r = 8
            draw.ellipse((x - r, y - r, x + r, y + r), fill='green')
            r = 6
            draw.ellipse((x - r, y - r, x + r, y + r), fill='red')
            r = 5
            color = 'green'
            
            for _ in range(2):
                x, y = pyautogui.position()
                x -= gl.speed
                draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
                x -= gl.speed
                draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
                x, y = pyautogui.position()
                x += gl.speed
                draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
                x += gl.speed
                draw.ellipse((x - r, y - r, x + r, y + r), fill=color)

                x, y = pyautogui.position()
                y -= gl.speed
                draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
                y -= gl.speed
                draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
                x, y = pyautogui.position()
                y += gl.speed
                draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
                y += gl.speed
                draw.ellipse((x - r, y - r, x + r, y + r), fill=color)

                x, y = pyautogui.position()
                y -= gl.speed
                x -= gl.speed
                draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
                x, y = pyautogui.position()
                y -= gl.speed
                x += gl.speed
                draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
                x, y = pyautogui.position()
                y += gl.speed
                x -= gl.speed
                draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
                x, y = pyautogui.position()
                y += gl.speed
                x += gl.speed
                draw.ellipse((x - r, y - r, x + r, y + r), fill=color)

                r = 3
                color = 'white'

        if(gl.screenshot_resize):
            screenshot = screenshot.resize((screenshot.width // 3, screenshot.height // 3))
        img_bytes = io.BytesIO()
        screenshot.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        inline_kb = InlineKeyboardMarkup(row_width=5) 
        button1 = InlineKeyboardButton(text='Update', callback_data='=') 
        button2 = InlineKeyboardButton(text='DLMB', callback_data='dlmb') 
        button3 = InlineKeyboardButton(text='↑↑', callback_data='up2') 
        button4 = InlineKeyboardButton(text='RMB', callback_data='rmb') 
        button5 = InlineKeyboardButton(text='sp++', callback_data='sp++') 
        inline_kb.add(button1, button2, button3, button4, button5) 

        button1 = InlineKeyboardButton(text='Video', callback_data='video') 
        button2 = InlineKeyboardButton(text='←↑', callback_data='upleft') 
        button3 = InlineKeyboardButton(text='↑', callback_data='up') 
        button4 = InlineKeyboardButton(text='↑→', callback_data='upright') 
        button5 = InlineKeyboardButton(text='sp+', callback_data='sp+') 
        inline_kb.add(button1, button2, button3, button4, button5) 

        button1 = InlineKeyboardButton(text='←←', callback_data='left2') 
        button2 = InlineKeyboardButton(text='←', callback_data='left') 
        button3 = InlineKeyboardButton(text='LMB', callback_data='lmb') 
        button4 = InlineKeyboardButton(text='→', callback_data='right') 
        button5 = InlineKeyboardButton(text='→→', callback_data='right2') 
        inline_kb.add(button1, button2, button3, button4, button5) 

        button1 = InlineKeyboardButton(text='Resolution', callback_data='scrres') 
        button2 = InlineKeyboardButton(text='←↓', callback_data='downleft') 
        button3 = InlineKeyboardButton(text='↓', callback_data='down') 
        button4 = InlineKeyboardButton(text='↓→', callback_data='downright') 
        button5 = InlineKeyboardButton(text='sp-', callback_data='sp-') 
        inline_kb.add(button1, button2, button3, button4, button5) 

        button1 = InlineKeyboardButton(text='Delay-', callback_data='del-') 
        button2 = InlineKeyboardButton(text='Delay+', callback_data='del+') 
        button3 = InlineKeyboardButton(text='↓↓', callback_data='down2') 
        button4 = InlineKeyboardButton(text='enter', callback_data='enter') 
        button5 = InlineKeyboardButton(text='sp--', callback_data='sp--') 
        inline_kb.add(button1, button2, button3, button4, button5)

        button1 = InlineKeyboardButton(text='tab', callback_data='tab') 
        button2 = InlineKeyboardButton(text='k←', callback_data='kleft') 
        button3 = InlineKeyboardButton(text='k↓', callback_data='kdown') 
        button4 = InlineKeyboardButton(text='k↑', callback_data='kup') 
        button5 = InlineKeyboardButton(text='k→', callback_data='kright') 
        inline_kb.add(button1, button2, button3, button4, button5)

        button1 = InlineKeyboardButton(text='Texthelp', callback_data='help') 
        button2 = InlineKeyboardButton(text='alt+f4', callback_data='close') 
        button3 = InlineKeyboardButton(text='alt+tab', callback_data='change') 
        button4 = InlineKeyboardButton(text='alt+2tab', callback_data='change2') 
        button5 = InlineKeyboardButton(text='ComDelete', callback_data='comdel') 
        inline_kb.add(button1, button2, button3, button4, button5)

        caption = f"speed:{gl.speed}px; delay:{gl.delay / gl.DELAY_MULTIPLICATOR}s; Comand deleting:{gl.command_delete}; Screenshot resize: {gl.screenshot_resize}"

        if id is None:
            m = bot.send_photo(chat_id=message.chat.id, photo=img_bytes, reply_markup=inline_kb, caption=caption)
            gl.screen_id = m.id
        else:
            bot.edit_message_media(
                chat_id=chat,
                message_id=id,
                media=InputMediaPhoto(media=img_bytes, caption=caption),
                reply_markup=inline_kb
            )

    except Exception as e:
        print(e)

@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    print(call.message.chat.id)
    global video
    try:
        _delay = True
        if call.data == 'up':
            moveRel(0, -gl.speed, gl.delay / gl.DELAY_MULTIPLICATOR)
            _delay = False
        elif call.data == 'down':
            moveRel(0, +gl.speed, gl.delay / gl.DELAY_MULTIPLICATOR)
            _delay = False
        elif call.data == 'left':
            moveRel(-gl.speed, 0, gl.delay / gl.DELAY_MULTIPLICATOR)
            _delay = False
        elif call.data == 'right':
            moveRel(+gl.speed, 0, gl.delay / gl.DELAY_MULTIPLICATOR)
            _delay = False

        elif call.data == 'upleft':
            moveRel(-gl.speed, -gl.speed, gl.delay / gl.DELAY_MULTIPLICATOR)
            _delay = False
        elif call.data == 'upright':
            moveRel(gl.speed, -gl.speed, gl.delay / gl.DELAY_MULTIPLICATOR)
            _delay = False
        elif call.data == 'downleft':
            moveRel(-gl.speed, gl.speed, gl.delay / gl.DELAY_MULTIPLICATOR)
            _delay = False
        elif call.data == 'downright':
            moveRel(gl.speed, gl.speed, gl.delay / gl.DELAY_MULTIPLICATOR)
            _delay = False

        elif call.data == 'up2':
            moveRel(0, -gl.speed * 2, gl.delay / gl.DELAY_MULTIPLICATOR)
            _delay = False
        elif call.data == 'down2':
            moveRel(0, +gl.speed * 2, gl.delay / gl.DELAY_MULTIPLICATOR)
            _delay = False
        elif call.data == 'left2':
            moveRel(-gl.speed * 2, 0, gl.delay / gl.DELAY_MULTIPLICATOR)
            _delay = False
        elif call.data == 'right2':
            moveRel(+gl.speed * 2, 0, gl.delay / gl.DELAY_MULTIPLICATOR)
            _delay = False

        elif call.data == 'lmb':
            pyautogui.click(button='left')
        elif call.data == 'comdel':
            gl.command_delete = not gl.command_delete
        elif call.data == 'scrres':
            gl.screenshot_resize = not gl.screenshot_resize
        elif call.data == 'video':
            video = not video
            if(video):
                threading.Thread(target=video_updater).start()
        elif call.data == 'dlmb':
            pyautogui.click(button='left')
            time.sleep(0.1)
            pyautogui.click(button='left')
        elif call.data == 'rmb':
            pyautogui.click(button='right')
        elif call.data == 'sp+':
            gl.speed *= 2
        elif call.data == 'sp-' and gl.speed > 5:
            gl.speed //= 2
        elif call.data == 'del+':
            gl.delay += 1
        elif call.data == 'del-' and gl.delay > 0:
            gl.delay -= 1
        elif call.data == 'sp++':
            gl.speed *= 4
        elif call.data == 'sp--' and gl.speed > 10:
            gl.speed //= 4
        elif call.data == 'space':
            _delay = False
            keyboard.press("space")
            time.sleep(gl.delay)
            keyboard.release("space")
        elif call.data == 'enter':
            _delay = False
            keyboard.press("enter")
            time.sleep(gl.delay)
            keyboard.release("enter")
        elif call.data == "change":
            keyboard.press("alt")
            keyboard.press_and_release("tab")
            keyboard.release("alt")
        elif call.data == "change2":
            keyboard.press("alt")
            keyboard.press("tab")
            keyboard.release("tab")
            keyboard.press("tab")
            keyboard.release("tab")
            keyboard.release("alt")
        elif call.data == "close":
            keyboard.press("alt")
            keyboard.press_and_release("f4")
            keyboard.release("alt")
        elif call.data == 'kup':
            _delay = False
            keyboard.press("up")
            time.sleep(gl.delay)
            keyboard.release("up")
        elif call.data == 'kdown':
            _delay = False
            keyboard.press("down")
            time.sleep(gl.delay)
            keyboard.release("down")
        elif call.data == 'kleft':
            _delay = False
            keyboard.press("left")
            time.sleep(gl.delay)
            keyboard.release("left")
        elif call.data == 'kright':
            _delay = False
            keyboard.press("right")
            time.sleep(gl.delay)
            keyboard.release("right")
        elif call.data == 'tab':
            _delay = False
            keyboard.press("tab")
            time.sleep(gl.delay)
            keyboard.release("tab")
        elif call.data == 'help':
            from .handle import help
            help(call.message)

        bot.answer_callback_query(call.id, call.data)
        if(_delay):
            time.sleep(gl.delay / gl.DELAY_MULTIPLICATOR)
        screen(call.message, call.message.chat.id, call.message.id)
    except Exception as e:
        print(e)

video = False
def video_updater():
    print(gl.screen_id, video)
    while gl.screen_id != 0 and video:
        screen(None, gl.chat, gl.screen_id)
        time.sleep(gl.delay / 5)
