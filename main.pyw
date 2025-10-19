import telebot
import time
import threading
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
import pyautogui
import tempfile
from PIL import Image, ImageDraw
from screeninfo import get_monitors
from dotenv import load_dotenv
import keyboard
import sys
import os
import io

work = False
def working():
    while work:
        time.sleep(30 * 60)
        bot.send_message(5650499270, 'Stand')
        time.sleep(10 * 60)
        bot.send_message(5650499270, 'Good')

video = False
def video_updater():
    print(screen_id, video)
    while screen_id != 0 and video:
        screen(None, 5650499270, screen_id)
        time.sleep(delay / 5)


# Введите сюда ваш токен, полученный у BotFather
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

delay = 0
speed = 10
path = "C:\\Users\\robom\\OneDrive\\Desktop"
screen_id = 0
comand_delete = True
cursor_draw = True
screenshot_resize = False
DELAY_MULTIPLICATOR = 5

# Обработчик всех текстовых сообщений
@bot.message_handler(commands=['screen'])
def screen(message=None, chat=None, id=None):
    global screen_id
    try:
        # Делаем скриншот сразу в память
        screenshot = pyautogui.screenshot()

        # Можно не рисовать ничего для ускорения
        if cursor_draw:
            draw = ImageDraw.Draw(screenshot)
            x, y = pyautogui.position()
            r = 5
            draw.ellipse((x - r, y - r, x + r, y + r), fill='red')

        if(screenshot_resize):
            screenshot = screenshot.resize((screenshot.width // 3, screenshot.height // 3))

        # Сохраняем в память без временных файлов
        img_bytes = io.BytesIO()
        screenshot.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        inline_kb = InlineKeyboardMarkup(row_width=5) 
        button1 = InlineKeyboardButton(text='Update', callback_data='=') 
        button2 = InlineKeyboardButton(text='Video', callback_data='video') 
        button3 = InlineKeyboardButton(text='^^', callback_data='up2') 
        button4 = InlineKeyboardButton(text='alt+f4', callback_data='close') 
        button5 = InlineKeyboardButton(text='alt+tab', callback_data='change') 
        inline_kb.add(button1, button2, button3, button4, button5) 
        button1 = InlineKeyboardButton(text='Delay-', callback_data='del-') 
        button2 = InlineKeyboardButton(text='Delay+', callback_data='del+') 
        button3 = InlineKeyboardButton(text='^', callback_data='up') 
        button4 = InlineKeyboardButton(text='ComDel', callback_data='comdel') 
        button5 = InlineKeyboardButton(text='ScreenRes', callback_data='scrres') 
        inline_kb.add(button1, button2, button3, button4, button5) 
        button1 = InlineKeyboardButton(text='<<', callback_data='left2') 
        button2 = InlineKeyboardButton(text='<', callback_data='left') 
        button3 = InlineKeyboardButton(text='LMB', callback_data='lmb') 
        button4 = InlineKeyboardButton(text='>', callback_data='right') 
        button5 = InlineKeyboardButton(text='>>', callback_data='right2') 
        inline_kb.add(button1, button2, button3, button4, button5) 
        button1 = InlineKeyboardButton(text='DLMB', callback_data='dlmb') 
        button2 = InlineKeyboardButton(text='RMB', callback_data='rmb') 
        button3 = InlineKeyboardButton(text='\\/', callback_data='down') 
        button4 = InlineKeyboardButton(text='sp-', callback_data='sp-') 
        button5 = InlineKeyboardButton(text='sp--', callback_data='sp--') 
        inline_kb.add(button1, button2, button3, button4, button5) 
        button1 = InlineKeyboardButton(text='Space', callback_data='space') 
        button2 = InlineKeyboardButton(text='Enter', callback_data='enter') 
        button3 = InlineKeyboardButton(text='\\/\\/', callback_data='down2') 
        button4 = InlineKeyboardButton(text='sp+', callback_data='sp+') 
        button5 = InlineKeyboardButton(text='sp++', callback_data='sp++') 
        inline_kb.add(button1, button2, button3, button4, button5)

        caption = f"speed:{speed}px; delay:{delay / DELAY_MULTIPLICATOR}s; Comand deleting:{comand_delete}; Screenshot resize: {screenshot_resize}"

        if id is None:
            m = bot.send_photo(chat_id=message.chat.id, photo=img_bytes, reply_markup=inline_kb, caption=caption)
            screen_id = m.id
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
    try:
        global speed, delay, video, comand_delete, screenshot_resize
        _delay = True
        if call.data == 'up':
            pyautogui.moveTo(pyautogui.position().x, pyautogui.position().y - speed, duration=delay / DELAY_MULTIPLICATOR)
            _delay = False
        elif call.data == 'down':
            pyautogui.moveTo(pyautogui.position().x, pyautogui.position().y + speed, duration=delay / DELAY_MULTIPLICATOR)
            _delay = False
        elif call.data == 'left':
            pyautogui.moveTo(pyautogui.position().x - speed, pyautogui.position().y, duration=delay / DELAY_MULTIPLICATOR)
            _delay = False
        elif call.data == 'right':
            pyautogui.moveTo(pyautogui.position().x + speed, pyautogui.position().y, duration=delay / DELAY_MULTIPLICATOR)
            _delay = False
        if call.data == 'up2':
            pyautogui.moveTo(pyautogui.position().x, pyautogui.position().y - speed * 2, duration=delay / DELAY_MULTIPLICATOR)
            _delay = False
        elif call.data == 'down2':
            pyautogui.moveTo(pyautogui.position().x, pyautogui.position().y + speed * 2, duration=delay / DELAY_MULTIPLICATOR)
            _delay = False
        elif call.data == 'left2':
            pyautogui.moveTo(pyautogui.position().x - speed * 2, pyautogui.position().y, duration=delay / DELAY_MULTIPLICATOR)
            _delay = False
        elif call.data == 'right2':
            pyautogui.moveTo(pyautogui.position().x + speed * 2, pyautogui.position().y, duration=delay / DELAY_MULTIPLICATOR)
            _delay = False
        elif call.data == 'lmb':
            pyautogui.click(button='left')
        elif call.data == 'comdel':
            comand_delete = not comand_delete
        elif call.data == 'scrres':
            screenshot_resize = not screenshot_resize
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
            speed *= 2
        elif call.data == 'sp-' and speed > 5:
            speed //= 2
        elif call.data == 'del+':
            delay += 1
        elif call.data == 'del-' and delay > 0:
            delay -= 1
        elif call.data == 'sp++':
            speed *= 4
        elif call.data == 'sp--' and speed > 10:
            speed //= 4
        elif call.data == 'space':
            keyboard.press("space")
        elif call.data == 'enter':
            keyboard.press("enter")
        elif call.data == "change":
            keyboard.press("alt")
            keyboard.press_and_release("tab")
            keyboard.release("alt")
        elif call.data == "close":
            keyboard.press("alt")
            keyboard.press_and_release("f4")
            keyboard.release("alt")

        bot.answer_callback_query(call.id, call.data)
        if(_delay):
            time.sleep(delay / DELAY_MULTIPLICATOR)
        screen(call.message, call.message.chat.id, call.message.id)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['work'])
def worker(message):
    global work
    work = True
    threading.Thread(target=working).start()
    bot.send_message(message.chat.id, 'Working mode activated')

@bot.message_handler(commands=['stop'])
def worker(message):
    global work
    work = False
    bot.send_message(message.chat.id, 'Working mode deactivated')

@bot.message_handler(commands=['video'])
def worker(message):
    global video
    video = True
    threading.Thread(target=video_updater).start()
    bot.send_message(message.chat.id, 'activated')

@bot.message_handler(commands=['shutdown'])
def worker(message):
    import os
    bot.send_message(message.chat.id, 'Goodbye')
    os.system('shutdown /s /t 1')

@bot.message_handler(func=lambda message: message.text.startswith("Wheel "))
def write(message):
    try:
        pyautogui.scroll(int(message.text[6:]))
    finally:
        if(comand_delete):
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@bot.message_handler(func=lambda message: message.text.startswith("Exec "))
def write(message):
    global answer
    def answer(text, message=message):
        bot.send_message(message.chat.id, str(text))
    try:
        exec(message.text[5:], globals())
        bot.send_message(message.chat.id, "Executed")
    finally:
        pass

@bot.message_handler(func=lambda message: message.text.startswith("Eval "))
def write(message):
    try:
        bot.send_message(message.chat.id, eval(message.text[5:]))
    finally:
        pass

@bot.message_handler(func=lambda message: message.text.startswith("Write "))
def write(message):
    pyautogui.write(message.text[6:])
    if(comand_delete):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    time.sleep(0.1)
    screen(message, message.chat.id, screen_id)

@bot.message_handler(func=lambda message: message.text.startswith("Hold "))
def hold(message):
    print(message.text)
    sp = message.text[5:].strip().split()
    #
    print(sp)
    pyautogui.keyDown(sp[0])
    if not sp:
            return
    try:
        key_to_press = sp[0]
        if len(sp) > 1:
            delay = float(sp[1])
        else:
            delay = float('inf')

        if delay >= 0:
            if(sp[0] in ('lmb', 'rmb', 'mmb')):
                pyautogui.mouseDown()
            else:
                keyboard.press(key_to_press)
            if delay != float('inf'):
                def a(delay=delay, key_to_press=key_to_press):
                    time.sleep(delay)
                    if(sp[0] in ('lmb', 'rmb', 'mmb')):
                        pyautogui.mouseUp()
                    else:
                        keyboard.release(key_to_press)
                threading.Thread(target=a).start()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    if(comand_delete):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    screen(message, message.chat.id, screen_id)

@bot.message_handler(func=lambda message: message.text.startswith("Release "))
def hold(message):
    if(comand_delete):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    screen(message, message.chat.id, screen_id)

@bot.message_handler(func=lambda message: message.text.startswith("Press "))
def press(message):
    spl = message.text[6:].split()
    if(len(spl) == 2):
        left, right = spl
    elif(len(spl) == 1):
        left, right = *spl, 1
    else:
        return
    
    lis = left.strip().split('+')
    if(message.text.endswith('++')):
        lis.append('+')
    for key in range(len(lis) - 1):
        try:
            keyboard.press(lis[key])
        except:
            if(lis[key] != ''):
                bot.send_message(message.chat.id, 'Unexpected key: ' + lis[key])
    try:
        for _ in range(int(right)):
            keyboard.press_and_release(lis[-1])
            time.sleep(0.05)
    except:
        if(lis[-1] != ''):
            bot.send_message(message.chat.id, 'Unexpected key: ' + lis[key])
    for key in range(len(lis) - 2, -1, -1):
        try:
            keyboard.release(lis[key])
        except:
            if(lis[key] != ''):
                bot.send_message(message.chat.id, 'Unexpected key: ' + lis[key])
    if(comand_delete):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    screen(message, message.chat.id, screen_id)

@bot.message_handler(commands=['ping'])
def hold(message):
    bot.send_message(message.chat.id, "PING")

@bot.message_handler(commands=['exit'])
def exit(message):
    bot.send_message(message.chat.id, "EXIT")
    os._exit(1)

@bot.message_handler(func=lambda message: message.text.startswith("Sd "))
def sd(message):
    global path
    if(os.path.exists(message.text[3:])):
        path = message.text[3:]

@bot.message_handler(func=lambda message: message.text.startswith("Cd "))
def cd(message):
    global path
    cmd = message.text[3:]
    if(cmd == '..'):
        path = "\\".join(path.split("\\")[:-1])
        bot.send_message(message.chat.id, path)
    else:
        contents = os.listdir(path)
        b = False
        for item in contents:
            if item == cmd and os.path.isdir(os.path.join(path, item)):
                b = True
                path = os.path.join(path, item)
                break
        if(b):
            bot.send_message(message.chat.id, path)
        else:
            bot.send_message(message.chat.id, f"Cannot find directory {cmd}")

@bot.message_handler(func=lambda message: message.text.startswith("Start "))
def write(message):
    import subprocess
    subprocess.Popen([os.path.join(path, message.text[6:])])

@bot.message_handler(func=lambda message: message.text.startswith("Type "))
def typee(message):
    name = message.text[5:]
    try:
        if(len(text := open(os.path.join(path, name), encoding="utf-8").read()) < 4000):
            bot.send_message(message.chat.id, text if text != "" else "**🟥EMPTY FILE🟥**")
        else:
            bot.send_document(message.chat.id, open(os.path.join(path, name), "rb"))
    except:
        bot.send_document(message.chat.id, open(os.path.join(path, name), "rb"))

@bot.message_handler(func=lambda message: message.text.startswith("Send "))
def typee(message):
    name = message.text[5:]
    bot.send_document(message.chat.id, open(os.path.join(path, name), "rb"))

@bot.message_handler(func=lambda message: message.text.startswith("Rewrite "))
def rewrite(message):
    name, *text = message.text[8:].split("\n")
    with open(os.path.join(path, name), "w") as f:
        f.write("\n".join(text))
    bot.send_message(message.chat.id, "Rewrited the file.")

@bot.message_handler(func=lambda message: message.text.startswith("Addwrite "))
def rewrite(message):
    name, *text = message.text[9:].split("\n")
    print(text)
    with open(os.path.join(path, name), "a") as f:
        f.write("\n".join(text))
    bot.send_message(message.chat.id, "Added to the file.")

@bot.message_handler(func=lambda message: message.text == "Dir")
def Dir(message):
    text = path + "\n\n"
    contents = os.listdir(path)

    for item in contents:
        if os.path.isdir(os.path.join(path, item)):
            text += f"[DIR] {item}\n"
    for item in contents:
        if os.path.isfile(os.path.join(path, item)):
            text += f"[FILE] {item}\n"
    
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['document'], func=lambda message: message.caption.startswith("Rewrite "))
def handle_document(message):
    file_id = message.document.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    name = message.caption[8:]
    if(os.path.exists(path, name)):
        with open(os.path.exists(path, name), 'wb') as f:
            f.write(downloaded_file)

    bot.reply_to(message, f"Rewrited {name}")

@bot.message_handler(content_types=['document'], func=lambda message: message.caption.startswith("Addwrite "))
def handle_document(message):
    file_id = message.document.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    name = message.caption[9:]
    if(os.path.exists(path, name)):
        with open(os.path.exists(path, name), 'wb') as f:
            f.write(downloaded_file)

    bot.reply_to(message, f"Added to file {name}")

@bot.message_handler(commands=['help'])
def hold(message):
    bot.send_message(message.chat.id, '''Comand list:
    Wheel <num>
    Press <keyboard shortcut> [times]
    Write <text>
    Hold <key> [time]
    Release <key>
    Eval <expression>
    Exec <python code>
                     Dir
    Cd <dir>
    Sd <dir>
    Start <file in current directory name>
    Type <file in current directory name>
    Send <file in current directory name>
    Rewrite <file in current directory name>\n    <text>
    Addwrite <file in current directory name>\n    <text>''')
    

#for Exec comand
def answer():
    pass

print()
print("active")
bot.send_message(5650499270, 'Hi')
commands = [
    telebot.types.BotCommand('/screen', 'Activate screenmove mode'),
    telebot.types.BotCommand('/exit', 'Exit bot'),
    telebot.types.BotCommand('/help', 'Comand list'),
    telebot.types.BotCommand('/work', 'Start working'),
    telebot.types.BotCommand('/stop', 'Stop working'),
    telebot.types.BotCommand('/shutdown', 'Shut down'),
    telebot.types.BotCommand('/ping', 'Ping'),
    telebot.types.BotCommand('/video', 'Video updater'),    
]
bot.set_my_commands(commands)
while True:
    try:
        bot.polling()
    except Exception as e:
        bot.send_message(5650499270, str(e))