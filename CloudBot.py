#   "Main"
#   CloudBot.py
#
#   Copyright (c) Alex Green.All rights reserved.
#
#
import telebot
import logging
import re
from waitress import serve
from GoogleDrive import *
from Variables import *
from flask import Flask


app = Flask(__name__, static_folder='static')
bot = telebot.TeleBot(token_)

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.from_user.id,startMessage_)

@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.from_user.id, botCommands_)

@bot.message_handler(content_types=['text'])
def anyText_handler(message):
    if (re.search(r'\bhello\b', message.text.lower())
     or re.search(r'\bhi\b', message.text.lower())):
        bot.send_message(message.from_user.id, helloMessage_ + str(message.from_user.first_name) + '!')
    else:
        bot.send_message(message.from_user.id, nUMessage_)

@bot.message_handler(content_types=['document','photo','video','audio','voice','animation'])
def anyFile_hendler(message):
    global files_flag
    while(files_flag == False) :
        pass
    files_flag = False
    if message.photo != None:
        file_info = bot.get_file(message.photo[-1].file_id)
        bot.send_message(message.from_user.id, str(uploadFile(file_info, str(message.photo[-1].file_size),'photo')))
    elif message.document != None:
        file_info = bot.get_file(message.document.file_id)
        bot.send_message(message.from_user.id, str(uploadFile(file_info,message.document.file_name,'document')))
    elif message.video != None:
        file_info = bot.get_file(message.video.file_id)
        bot.send_message(message.from_user.id, str(uploadFile(file_info, message.video.file_size,'video')))
    elif message.audio != None:
        file_info = bot.get_file(message.audio.file_id)
        bot.send_message(message.from_user.id, str(uploadFile(file_info, message.audio.file_size, 'audio')))
    elif message.voice != None:
        file_info = bot.get_file(message.voice.file_id)
        bot.send_message(message.from_user.id, str(uploadFile(file_info, message.voice.file_size, 'voice')))
    elif message.animation != None:
        file_info = bot.get_file(message.animation.file_id)
        bot.send_message(message.from_user.id, str(uploadFile(file_info, message.animation.file_size, 'animation')))
    files_flag = True



def main(use_logging,level_name):
    if use_logging:
        telebot.logger.setLevel(logging.getLevelName(level_name))
    bot.polling(none_stop = True,interval=.5)


if __name__ == '__main__':
    main(True,'DEBUG')
    serve(app, host="0.0.0.0", port=8080)