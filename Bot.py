from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData

import lyricsgenius
token = "XHUCKXOEPYzU8jy0kopz6e5NdhNNnpoTxgOzlq5vSMhvIFjXB72W-Kc_JnKzJmZF"
genius = lyricsgenius.Genius(token)

from shazamio import Shazam
shazam = Shazam()

import logging
import os
import json
import time

from yt_d import yt_down


logging.basicConfig(level=logging.INFO, filename="bot.log",filemode="w")

botpath = os.getcwd()

with open("Token.json","r+") as fl:
    Tfile = fl.read()
    try:
        TOKEN = json.loads(Tfile)["TOKEN"]
    except:
        TOKEN = input("введите токен (https://t.me/BotFather): ")
        fl.write(json.dumps({"TOKEN":TOKEN}, sort_keys=True, indent=4))

bot = Bot(TOKEN)
dp = Dispatcher(bot)

start_msg = """
Привет {},
Этот бот сделан в рамках моего проекта.
Чтобы узнать возможности этого бота напиши в этот чат /help
Приятного использования!!!
"""

help_msg = """
Хорошо что ты это спросил!
/start                     старотовое сообщение
/help                      это сообщение
/yt_d [url] [format]      файл видео с [url] в формате audio/video поддерживаются youtube
/lyr [search]              Ищет текст песни
отправте гс файл или песню лично боту и он пришлет ее название и тест
"""
songs = {}
### not Telegram async func ###

    ## Telegram ##
def mes_inf(message, log=False):
    user_id = message.from_user.id
    user_fn = message.from_user.full_name
    m_time = time.asctime()
    text = message.text
    logmsg = f"[{user_id}:{user_fn}]] : [{text}]                                          {m_time}"
    if log:
        logging.info(f"{logmsg}\n\n")
    return user_fn, user_id, text, m_time

async def bot_reply(message, answer):
    user_fn,user_id,text,m_time = mes_inf(message, log=False)
    log = f" BOT: [{user_id}:{user_fn}]] : [{answer}]                                       {m_time}"
    log = filter(lambda ch: ch not in "\n", log)
    string = ""
    for i in log:
        string += i
    logging.info(f"{string}\n\n")
    await message.reply(answer)

def is_admin(id):
    with open("admins.json","r") as admins:
        py_obj = json.loads(admins.read())
        if str(id) in list(py_obj.keys()):
            return True
        else:
            return False


    ## USERS ##
def add_user(message):
    user_fn,user_id,text,m_time = mes_inf(message,log=False)
    with open("users.json","r") as users:
        users = json.loads(users.read())
        if str(user_id) not in list(users.keys()):
            users.update({str(user_id):{"full name":user_fn, "time": m_time}})
    with open("users.json","w") as users1:
        users1.write(json.dumps(users,indent=4))


    ## LYR ##

def get_songs(text):
    a = genius.search(text)["hits"]
    songs = []
    for i in range(len(a)):
        artist = a[i]["result"]["artist_names"]
        title = a[i]["result"]["title"]
        songs.append(f"{artist} -- {title}")
    return songs

def get_text(song):
	artist = song.split(" -- ")[0]
	title = song.split(" -- ")[1]

	song = genius.search_song(title,artist)

	lyrics = song.lyrics

	return [lyrics, artist, title]



@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def somebody_added(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(f"Wellcome to the club, {user.full_name}")

@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def somebody_added(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(f"Ну и катись отсюда, {user.full_name}")

@dp.message_handler(commands=["start"])
async def on_start(message: types.Message):
    user_fn, user_id, text, m_time = mes_inf(message,log=False)
    add_user(message)
    await bot_reply(message, start_msg.format(user_fn))

@dp.message_handler(commands=["help"])
async def on_start(message: types.Message):
    user_fn, user_id, text, m_time = mes_inf(message,log=False)
    add_user(message)
    await bot_reply(message, help_msg)

callback_yt = CallbackData("yt", "action")
@dp.message_handler(commands=["yt_d"])
async def yt_d(message: types.Message):
    user_fn, user_id, text, m_time = mes_inf(message, log=False)
    add_user(message)
    text = text.split(" ")[1:]
    url = text[0]
    try:
        vtype = text[1]
    except:
        vtype = "video"

    flen = len(os.listdir(f"{botpath}/yt"))

    await bot_reply(message, "Загружаем видео...")

    if "youtu" in url:
        service = "youtube"
        
    f = yt_down(url, vtype, f"{botpath}/yt/", flen)
    if f == "mp3":
        try:
            with open(f"{botpath}/yt/{flen}.{f}","rb") as doc:
                await message.answer_audio(doc)
                logging.info("BOT info: Успешно ")
        except:
            await bot_reply(message, "Файл не должен весить больше 50 мб. извините.")
            logging.info("BOT info: Провал ")
    else:
        try:
            with open(f"{botpath}/yt/{flen}.{f}","rb") as doc:
                await message.answer_video(doc)
                logging.info("BOT info: Успешно ")
        except:
            await bot_reply(message, "Файл не должен весить больше 50 мб. извините.")
            logging.info("BOT info: Провал ")
    


cb_lyr = CallbackData("lyr", "id", "chat")
@dp.message_handler(commands=["lyr"])
async def Lyrics(message: types.Message):
    user_fn,user_id,text,m_time = mes_inf(message, log=False)
    add_user(message)
    search = text.split(" ")[1:]
    print(" ".join(search))
    
    songs.update({str(message.chat.id) : get_songs(" ".join(search))})
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(songs[str(message.chat.id)])):
        n_song = songs[str(message.chat.id)][i]
        keyboard.add(types.InlineKeyboardButton(text=n_song, callback_data=cb_lyr.new(id=str(i), chat=str(message.chat.id))))
    await message.answer("Выбери нужную песню: ", reply_markup=keyboard)
    

@dp.message_handler(content_types=[types.ContentType.VOICE,types.ContentType.AUDIO,types.ContentType.DOCUMENT])
async def on_shazam(message: types.Message):
    user_fn,user_id,text,m_time = mes_inf(message,log=False)
    add_user(message)
    if message.content_type == types.ContentType.VOICE:
        file_id = message.voice.file_id
    elif message.content_type == types.ContentType.AUDIO:
        file_id = message.audio.file_id
    elif message.content_type == types.ContentType.DOCUMENT:
        file_id = message.document.file_id
    else:
        await message.reply("Формат документа не поддерживается")
        return
    
    file = await bot.get_file(file_id)
    file_path = file.file_path
    flen = len(os.listdir(f"{botpath}/music"))
    await bot.download_file(file_path, f"{botpath}/music/{flen}.mp3")
    out = await shazam.recognize_song(f"{botpath}/music/{flen}.mp3")
    title = out["track"]["title"]
    artist = out["track"]["subtitle"]
    try:
        lyr = out["track"]["sections"][1]["text"]
        lyr = '\n'.join(lyr)
    except:
        lyr = ""
    ans = f"{title} - {artist}\n\n {lyr}"
    await bot_reply(message, ans)


#### CALLBACK Handler
@dp.callback_query_handler(cb_lyr.filter())
async def callback_lyr(call: types.CallbackQuery, callback_data: dict):
    sid = int(callback_data["id"])
    chat = callback_data["chat"]
    
    text = songs[chat][sid]
    
    a = get_text(text)
    ans = f"{a[1]} - {a[2]}\n\n\n{a[0].replace('Embed','').replace('You might also like','')}"
    await bot_reply(call.message, ans)
    await call.answer()
        


if __name__ == "__main__":
    executor.start_polling(dp)
