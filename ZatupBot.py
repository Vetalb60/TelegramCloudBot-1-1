import telebot
import logging

from GoogleDrive import *
from Variables import *


bot = telebot.TeleBot(token_)

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.from_user.id,helloMessage_)

@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.from_user.id, botCommands_)

@bot.message_handler(content_types=['text'])
def anyText_handler(message):
    bot.send_message(message.from_user.id, notUndstndMessage_)

@bot.message_handler(content_types=['document','photo'])
def anyFile_hendler(message):
    global docs_flag
    while(docs_flag == False) :
        pass
    docs_flag = False
    if message.document == None:
        file_info = bot.get_file(message.photo[-1].file_id)
        uploadFile(file_info, str(message.photo[-1].file_size))
    else:
        file_info = bot.get_file(message.document.file_id)
        uploadFile(file_info,message.document.file_name)
    docs_flag = True


def main(use_logging,level_name):
    if use_logging:
        telebot.logger.setLevel(logging.getLevelName(level_name))
    bot.polling(none_stop = True,interval=.5)


if __name__ == '__main__':
    main(True,'DEBUG')