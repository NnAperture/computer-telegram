import keyboard
import pyautogui
from . import globals as gl
from handler.movRel import *
import threading
from handler import screen as screenmod
import os
from . import FS
from handler.config import set_chat

bot = gl.bot

working_th = threading.Thread()
def working():
    while gl.work:
        time.sleep(30 * 60)
        bot.send_message(gl.chat, 'Stand')
        time.sleep(10 * 60)
        bot.send_message(gl.chat, 'Good')
if(gl.work):
    if(not working_th.is_alive()):
        (working_th := threading.Thread(target=working)).start()

@bot.message_handler(func=lambda message: message.text.lower() == "work")
def worker(message):
    print(message.chat.id)
    if(gl.chat != message.chat.id):
        set_chat(message.chat.id)
        gl.chat = message.chat.id
    global work, working_th
    work = True
    if(not working_th.is_alive()):
        (working_th := threading.Thread(target=working)).start()
    bot.send_message(message.chat.id, 'Working mode activated')

@bot.message_handler(func=lambda message: message.text.lower() == "stop")
def worker(message):
    print(message.chat.id)
    if(gl.chat != message.chat.id):
        set_chat(message.chat.id)
        gl.chat = message.chat.id
    global work
    work = False
    bot.send_message(message.chat.id, 'Working mode deactivated')

@bot.message_handler(commands=['shutdown'])
def worker(message):
    print(message.chat.id)
    if(gl.chat != message.chat.id):
        set_chat(message.chat.id)
        gl.chat = message.chat.id
    import os
    bot.send_message(message.chat.id, 'Goodbye')
    os.system('shutdown /s /t 1')

@bot.message_handler(func=lambda message: message.text.lower().startswith("wheel "))
def write(message):
    print(message.chat.id)
    if(gl.chat != message.chat.id):
        set_chat(message.chat.id)
        gl.chat = message.chat.id
    try:
        pyautogui.scroll(int(message.text[6:]))
    finally:
        if(gl.command_delete):
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@bot.message_handler(func=lambda message: message.text.lower().startswith("move "))
def hold(message):
    print(message.chat.id)
    if(gl.chat != message.chat.id):
        set_chat(message.chat.id)
        gl.chat = message.chat.id
    spl = message.text[5:].split()
    if(len(spl) == 2):
        moveRel(int(spl[0]), int(spl[1]), duration=gl.delay / gl.DELAY_MULTIPLICATOR)
    else:
        moveRel(int(spl[0]), int(spl[1]), int(spl[2]))
    if(gl.command_delete):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@bot.message_handler(func=lambda message: message.text.lower().startswith("exec "))
def write(message):
    print(message.chat.id)
    if(gl.chat != message.chat.id):
        set_chat(message.chat.id)
        gl.chat = message.chat.id
    global answer
    def answer(text, message=message):
        bot.send_message(message.chat.id, str(text))
    try:
        exec(message.text[5:], globals())
        bot.send_message(message.chat.id, "Executed")
    finally:
        pass

@bot.message_handler(func=lambda message: message.text.lower().startswith("eval "))
def write(message):
    print(message.chat.id)
    if(gl.chat != message.chat.id):
        set_chat(message.chat.id)
        gl.chat = message.chat.id
    try:
        bot.send_message(message.chat.id, eval(message.text[5:]))
    finally:
        pass

@bot.message_handler(func=lambda message: message.text.lower().startswith("write "))
def write(message):
    print(message.chat.id)
    if(gl.chat != message.chat.id):
        set_chat(message.chat.id)
        gl.chat = message.chat.id
    pyautogui.write(message.text[6:])
    if(gl.command_delete):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    time.sleep(0.1)
    screenmod.screen(message, message.chat.id, gl.screen_id)

@bot.message_handler(func=lambda message: message.text.lower().startswith("hold "))
def hold(message):
    print(message.chat.id)
    if(gl.chat != message.chat.id):
        set_chat(message.chat.id)
        gl.chat = message.chat.id
    sp = message.text[5:].strip().split()
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
    if(gl.command_delete):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    screenmod.screen(message, message.chat.id, gl.screen_id)

@bot.message_handler(func=lambda message: message.text.lower().startswith("release "))
def hold(message):
    print(message.chat.id)
    if(gl.chat != message.chat.id):
        set_chat(message.chat.id)
        gl.chat = message.chat.id
    if(gl.command_delete):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    screenmod.screen(message, message.chat.id, gl.screen_id)

@bot.message_handler(func=lambda message: message.text.lower().startswith("press "))
def press(message):
    print(message.chat.id)
    if(gl.chat != message.chat.id):
        set_chat(message.chat.id)
        gl.chat = message.chat.id
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
    if(gl.command_delete):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    screenmod.screen(message, message.chat.id, gl.screen_id)

@bot.message_handler(commands=['ping'])
def hold(message):
    print(message.chat.id)
    if(gl.chat != message.chat.id):
        set_chat(message.chat.id)
        gl.chat = message.chat.id
    bot.send_message(message.chat.id, "PING")

@bot.message_handler(commands=['exit'])
def exit(message):
    print(message.chat.id)
    if(gl.chat != message.chat.id):
        set_chat(message.chat.id)
        gl.chat = message.chat.id
    bot.send_message(message.chat.id, "Goodbye")
    os._exit(1)

@bot.message_handler(commands=['help'])
def help(message):
    print(message.chat.id)
    if(gl.chat != message.chat.id):
        set_chat(message.chat.id)
        gl.chat = message.chat.id
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
    Addwrite <file in current directory name>\n    <text>
                     
    Work - enable working mode (reminder to stand up during work)
    Stop - disable working mode''')
    

#for Exec comand
def answer():
    pass
