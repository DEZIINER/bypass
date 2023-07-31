import pyrogram
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import bypasser
import os
import ddl
import requests
import threading
from texts import HELP_TEXT
from ddl import ddllist
import re


# bot
bot_token = os.environ.get("TOKEN", "")
api_hash = os.environ.get("HASH", "") 
api_id = os.environ.get("ID", "")
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)  


# handle ineex
def handleIndex(ele,message,msg):
    result = bypasser.scrapeIndex(ele)
    try: app.delete_messages(message.chat.id, msg.id)
    except: pass
    for page in result: app.send_message(message.chat.id, page, reply_to_message_id=message.id, disable_web_page_preview=True)


# loop thread
def loopthread(message,otherss=False):

    urls = []
    if otherss: texts = message.caption
    else: texts = message.text

    if texts in [None,""]: return
    for ele in texts.split():
        if "http://" in ele or "https://" in ele:
            urls.append(ele)
    if len(urls) == 0: return

    if bypasser.ispresent(ddllist,urls[0]):
        msg = app.send_message(message.chat.id, "⚡ **__𝑮𝑬𝑵𝑬𝑹𝑨𝑻𝑰𝑵𝑮...__**", reply_to_message_id=message.id)
    else:
        if urls[0] in "https://olamovies" or urls[0] in "https://psa.pm/":
            msg = app.send_message(message.chat.id, "**__🔎 ᴛʜɪꜱ ᴍɪɢʜᴛ ᴛᴀᴋᴇ ꜱᴏᴍᴇ ᴛɪᴍᴇ...__**", reply_to_message_id=message.id)
        else:
            msg = app.send_message(message.chat.id, "**__🔎 𝙱𝚢𝚙𝚊𝚜𝚜𝚒𝚗𝚐...𝙿𝚕𝚎𝚊𝚜𝚎 𝚆𝚊𝚒𝚝__**", reply_to_message_id=message.id)

    link = ""
    for ele in urls:
        if re.search(r"https?:\/\/(?:[\w.-]+)?\.\w+\/\d+:", ele):
            handleIndex(ele,message,msg)
            return
        elif bypasser.ispresent(ddllist,ele):
            try: temp = ddl.direct_link_generator(ele)
            except Exception as e: temp = "**Error**: " + str(e)
        else:    
            try: temp = bypasser.shortners(ele)
            except Exception as e: temp = "**Error**: " + str(e)
        print("bypassed:",temp)
        if temp != None: link = link + temp + "\n\n"
    
    if otherss:
        try:
            app.send_photo(message.chat.id, message.photo.file_id, f'__{link}__', reply_to_message_id=message.id)
            app.delete_messages(message.chat.id,[msg.id])
            return
        except: pass

    try: app.edit_message_text(message.chat.id, msg.id, f'__{link}__', disable_web_page_preview=True)
    except:
        try: app.edit_message_text(message.chat.id, msg.id, "__Failed to Bypass__")
        except:
            try: app.delete_messages(message.chat.id, msg.id)
            except: pass
            app.send_message(message.chat.id, "**__Failed to Bypass__**")


# start command
@app.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    app.send_message(message.chat.id, f"**__👋 Ꮋι **{message.from_user.mention}**, ɪ ᴀᴍ ʟɪɴᴋ ʙʏᴘᴀꜱꜱᴇʀ ʙᴏᴛ 😈, ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ʟɪɴᴋꜱ ᴀɴᴅ ɪ ᴡɪʟʟ ʏᴏᴜ ɢᴇᴛ ʏᴏᴜʀ ʀᴇꜱᴜʟᴛꜱ.\n𝑪𝑯𝑬𝑪𝑲𝑶𝑼𝑻 /help ᴛᴏ ʀᴇᴀᴅ ᴍᴏʀᴇ__**",
    reply_markup=InlineKeyboardMarkup([
        [ InlineKeyboardButton("𝑶𝑾𝑵𝑬𝑹 😎", url="https://telegram.me/dr_starnge")],
        [ InlineKeyboardButton("𝑺𝑼𝑷𝑷𝑶𝑹𝑻 ✅", url="https://telegram.me/myfliix_2") ]]), 
        [ InlineKeyboardButton("𝐃𝐎𝐍𝐀𝐓𝐄 😢", url="https://telegra.ph/file/7899f3e7bbf669d303219.jpg") ]]),    
        reply_to_message_id=message.id)


# help command
@app.on_message(filters.command(["help"]))
def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    app.send_message(message.chat.id, HELP_TEXT, reply_to_message_id=message.id, disable_web_page_preview=True)


# links
@app.on_message(filters.text)
def receive(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    bypass = threading.Thread(target=lambda:loopthread(message),daemon=True)
    bypass.start()


# doc thread
def docthread(message):
    msg = app.send_message(message.chat.id, "**__🔎 𝙱𝚢𝚙𝚊𝚜𝚜𝚒𝚗𝚐...𝙿𝚕𝚎𝚊𝚜𝚎 𝚆𝚊𝚒𝚝__**", reply_to_message_id=message.id)
    print("sent DLC file")
    sess = requests.session()
    file = app.download_media(message)
    dlccont = open(file,"r").read()
    link = bypasser.getlinks(dlccont,sess)
    app.edit_message_text(message.chat.id, msg.id, f'__{link}__')
    os.remove(file)


# files
@app.on_message([filters.document,filters.photo,filters.video])
def docfile(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    
    try:
        if message.document.file_name.endswith("dlc"):
            bypass = threading.Thread(target=lambda:docthread(message),daemon=True)
            bypass.start()
            return
    except: pass

    bypass = threading.Thread(target=lambda:loopthread(message,True),daemon=True)
    bypass.start()


# server loop
print("Bot Starting")
app.run()
