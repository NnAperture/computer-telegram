import os
from . import globals as gl
import subprocess
import difflib

path = gl.path
bot = gl.bot

import os
import difflib

def closest_path(approx_path: str) -> str | None:
    approx_path = os.path.normpath(approx_path)

    dir_path, last_part = os.path.split(approx_path)
    if not dir_path:
        dir_path = '.'

    if not os.path.isdir(dir_path):
        return None

    try:
        candidates = os.listdir(dir_path)
    except PermissionError:
        return None

    if not candidates:
        return None

    lower_last = last_part.lower()
    lower_candidates = {c.lower(): c for c in candidates}
    prefix_matches = [
        orig for low, orig in lower_candidates.items()
        if low.startswith(lower_last)
    ]
    if prefix_matches:
        prefix_matches.sort(key=lambda x: (len(x), x.lower()))
        return os.path.join(dir_path, prefix_matches[0])

    matches = difflib.get_close_matches(lower_last, list(lower_candidates.keys()), n=1, cutoff=0.6)
    if matches:
        return os.path.join(dir_path, lower_candidates[matches[0]])

    return None

@bot.message_handler(func=lambda message: message.text.lower().startswith("sd "))
def sd(message):
    global path
    new_path = message.text[3:]
    if os.path.exists(new_path):
        path = new_path
    else:
        fixed = closest_path(new_path)
        if fixed and os.path.exists(fixed):
            path = fixed
            bot.send_message(message.chat.id, f"✅ Path changed: {fixed}")
        else:
            bot.send_message(message.chat.id, f"❌ Path not found: {new_path}")
    Dir(message)

@bot.message_handler(func=lambda message: message.text.lower().startswith("cd "))
def cd(message):
    global path
    cmd = message.text[3:].strip()
    if cmd == '..':
        path = os.path.dirname(os.path.normpath(path))
        bot.send_message(message.chat.id, path)
        Dir(message)
        return
    clean_path = os.path.normpath(path)
    if len(clean_path) == 2 and clean_path[1] == ':':
        clean_path += "\\"

    target_path = os.path.join(clean_path, cmd)
    if os.path.isdir(target_path):
        path = target_path
        bot.send_message(message.chat.id, path)
        Dir(message)
        return
    fixed = closest_path(target_path)
    if fixed and os.path.isdir(fixed):
        path = fixed
        bot.send_message(message.chat.id, f"✅ Перешёл по похожему пути: {path}")
    else:
        bot.send_message(message.chat.id, f"❌ Cannot find directory {cmd}")

    Dir(message)

@bot.message_handler(func=lambda message: message.text.lower().startswith("start "))
def start(message):
    name = message.text[6:]
    lpath = os.path.join(path, name)
    if not os.path.exists(lpath):
        fixed = closest_path(lpath)
        if fixed and os.path.exists(fixed):
            lpath = fixed
            bot.send_message(message.chat.id, f"✅ Path changed: {lpath}")
        else:
            bot.send_message(message.chat.id, f"❌ File not found: {lpath}")
            return
    if not run_shortcut(lpath):
        subprocess.Popen([lpath])


@bot.message_handler(func=lambda message: message.text.lower().startswith("type "))
def typee(message):
    name = message.text[5:]
    lpath = os.path.join(path, name)
    if not os.path.exists(lpath):
        fixed = closest_path(lpath)
        if fixed and os.path.exists(fixed):
            lpath = fixed
            bot.send_message(message.chat.id, f"✅ Path changed: {lpath}")
        else:
            bot.send_message(message.chat.id, f"❌ File not found: {lpath}")
            return

    try:
        text = open(lpath, encoding="utf-8").read()
        if len(text) < 4000:
            bot.send_message(message.chat.id, text if text != "" else "**🟥EMPTY FILE🟥**")
        else:
            bot.send_document(message.chat.id, open(lpath, "rb"))
    except Exception:
        bot.send_document(message.chat.id, open(lpath, "rb"))


@bot.message_handler(func=lambda message: message.text.lower().startswith("send "))
def send_file(message):
    name = message.text[5:]
    lpath = os.path.join(path, name)
    if not os.path.exists(lpath):
        fixed = closest_path(lpath)
        if fixed and os.path.exists(fixed):
            lpath = fixed
            bot.send_message(message.chat.id, f"✅ Path changed: {lpath}")
        else:
            bot.send_message(message.chat.id, f"❌ File not found: {lpath}")
            return
    bot.send_document(message.chat.id, open(lpath, "rb"))

@bot.message_handler(func=lambda message: message.text.lower().startswith("rewrite "))
def rewrite(message):
    name, *text = message.text[8:].split("\n")
    lpath = os.path.join(path, name)
    if not os.path.exists(lpath):
        fixed = closest_path(lpath)
        if fixed:
            lpath = fixed
            bot.send_message(message.chat.id, f"✅ Path changed: {lpath}")
    with open(lpath, "w", encoding="utf-8") as f:
        f.write("\n".join(text))
    bot.send_message(message.chat.id, "Rewrited the file.")


@bot.message_handler(func=lambda message: message.text.lower().startswith("addwrite "))
def addwrite(message):
    name, *text = message.text[9:].split("\n")
    lpath = os.path.join(path, name)
    if not os.path.exists(lpath):
        fixed = closest_path(lpath)
        if fixed:
            lpath = fixed
            bot.send_message(message.chat.id, f"✅ Path changed: {lpath}")
    with open(lpath, "a", encoding="utf-8") as f:
        f.write("\n".join(text))
    bot.send_message(message.chat.id, "Added to the file.")


@bot.message_handler(func=lambda message: message.text.lower() == "dir")
def Dir(message):
    text = path + "\n\n"
    contents = os.listdir(path + '\\')
    for item in contents:
        if os.path.isdir(os.path.join(path + '\\', item)):
            text += f"[DIR] {item}\n"
    for item in contents:
        if os.path.isfile(os.path.join(path + '\\', item)):
            text += f"[FILE] {item}\n"
    bot.send_message(message.chat.id, text)


def run_shortcut(file_path: str) -> bool:
    file_path = os.path.abspath(file_path)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.lower().endswith(".lnk"):
        try:
            subprocess.Popen(['cmd', '/c', 'start', '', file_path], shell=True)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    else:
        return False
