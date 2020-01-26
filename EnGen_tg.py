#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os.path
from module1 import *
from TgTest import *
from gis import *
from urllib import request, parse
from bs4 import *
from urllib.parse import quote
import random
import re
import json
import time

from datetime import datetime
from threading import Timer
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Define a global variables
Holder = GlobalHolder()

#tg methods

def tg_error(update, context):
    update.message.reply_text('hello')
    update.message.reply_text("Callback: {0}".format(str(context.error)))
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def tg_test(update, context):
    newstr = ""
    try:
        update.message.reply_text("hello")
        update.message.reply_text("hello, " + update.message.from_user.first_name + "\n")
        update.message.reply_text("hello, " + update.message.from_user.first_name + "\n"+str(update.message.from_user.id) + "\n")
        update.message.reply_text("hello, " + update.message.from_user.first_name + "\n"
                                  +str(update.message.from_user.id) + "\n")
        update.message.reply_text("hello, " + update.message.from_user.first_name + "\n"
                                  +str(update.message.from_user.id) + "\n"
                                  +update.message.from_user.first_name + "\n"
                                  +update.message.from_user.last_name + "\n"
                                  +update.message.from_user.username + "\n")
        update.message.reply_text("hello, " + update.message.from_user.first_name + "\n"
                                  +update.message.from_user.id + "\n"
                                  +update.message.from_user.first_name + "\n"
                                  +update.message.from_user.last_name + "\n"
                                  +update.message.from_user.username + "\n")
        for i in range(0,100):
            newstr+="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff" + str(i) + "\n"
            update.message.reply_text(newstr)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_olymp(update, context):
    try:
        bot_authorize(update.message.chat.id)
        input_text = simple_message_handler(update.message.text, TgCommands.Olymp, True)
        msg = default_input(input_text, ModeType.Olymp)
        update.message.reply_text(msg)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_gibrid(update, context):
    try:
        bot_authorize(update.message.chat.id)
        input_text = simple_message_handler(update.message.text, TgCommands.Gibrid, True)
        msg = default_input(input_text, ModeType.Gibrid3)
        update.message.reply_text(msg)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_meta(update, context):
    try:
        bot_authorize(update.message.chat.id)
        input_text = simple_message_handler(update.message.text, TgCommands.Meta, True)
        msg = default_input(input_text, ModeType.Meta)
        update.message.reply_text(msg)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_logo(update, context):
    try:
        bot_authorize(update.message.chat.id)
        input_text = simple_message_handler(update.message.text, TgCommands.Logo, True)
        msg = default_input(input_text, ModeType.Logo)
        update.message.reply_text(msg)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_switch_mode(update, context):
    global Holder
    try:
        bot_authorize(update.message.chat.id)
        input_text = simple_message_handler(update.message.text, TgCommands.SwitchMode, False)
        settings = Holder.get(update.message.chat.id)
        mode = settings.current_mode
        if input_text is None:
            mode = settings.next_mode()
        else:
            newmodes = ModeType.get_modes_by_alias(input_text)
            if len(newmodes)==0:
                update.message.reply_text('mode not found')
                return
            else:
                if len(newmodes)>1:
                    found_modes = [ModeType.aliases_by_modes[mode_int][0] for mode_int in newmodes]
                    update.message.reply_text('more than one mode found:\n' + '\n'.join(found_modes))
                    return
                else:
                    mode = newmodes[0]
                    settings.current_mode = mode
        update.message.reply_text('switched to ' + ModeType.aliases_by_modes[mode][0])
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_default(update, context):
    try:
        bot_authorize(update.message.chat.id)
        settings = Holder.get(update.message.chat.id)
        mode = settings.current_mode
        if mode == ModeType.Disabled:
            return
        result = default_input(update.message.text, mode)
        if not result.is_success:
            print_long(update, "failed:\n" + result.message)
        for msg in result.values:
            print_long(update, msg)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def print_long(update, input_text):
    if len(input_text) > 4096:
        for x in range(0, len(input_text), 4096):
            update.message.reply_text(input_text[x:x+4096])
    else:
        update.message.reply_text(input_text)

#----------

def bot_authorize(id):
    global Holder
    if not id in Holder.settings_by_id:
        Holder.add(id)
        return
        #raise Exception('you are not authorized, please call /start')

def default_input(text, mode):
    text_handler = Holder.default_text_handlers_by_modes[mode]
    if text_handler is None:
        return Result.failed("current mode is not supported yet")
    return text_handler.do_action(text)

def simple_message_handler(full_text, command, empty_is_invalid = False):
    if len(full_text)<len(command)+3:
        if empty_is_invalid:
            raise Exception('command should contains arguments')
        return None
    return full_text[len(command)+2:]

def action_olymp(first, second, output=[]):
    return list(set(first).intersection(second))

def action_gibrid3(first, second, output=[]):
    union = []
    for i in first:
        for j in second:
            if len(i)<4 and len(j)<4:
                continue
            if i[-3:] == j[0:3]:
                union.append(i + '-' + j)
                output.append(i)
                output.append(j)
            if i[0:3] == j[-3:]:
                union.append(j + '-' + i)
                output.append(i)
                output.append(j)
    return union

def action_gibrid4(first, second, output=[]):
    union = []
    for i in first:
        for j in second:
            if len(i)<5 and len(j)<5:
                continue
            if i[-4:] == j[0:4]:
                union.append(i + '-' + j)
                output.append(i)
                output.append(j)
            if i[0:4] == j[-4:]:
                union.append(j + '-' + i)
                output.append(i)
                output.append(j)
    return union

def action_meta(first, second, output=[]):
    union = []
    for word1 in first:
        for word2 in second:
            if len(word1) != len(word2):
                continue
            counter = 0
            for i in range(0, len(word1)):
                if word1[i]!=word2[i]:
                    counter+=1
            if counter != 1:
                continue
            if word2 + '-' + word1 in union:
                continue
            union.append(word1 + '-' + word2)
            output.append(word1)
            output.append(word2)
    return union

def action_logo(first, second, output=[]):
    union = []
    for word1 in first:
        for word2 in second:
            long_word = ''
            short_word = ''
            if len(word1) == len(word2) + 1:
                long_word = word1
                short_word = word2
            else:
                if len(word2) == len(word1) + 1:
                    long_word = word2
                    short_word = word1
                else:
                    continue
            diff_index = 0
            for i in range(0, len(short_word)):
                if long_word[i]!=short_word[i]:
                    diff_index = i
                    break
            for i in range(diff_index, len(short_word)):
                if long_word[i + 1]!=short_word[i]:
                    diff_index = -1
                    break
            if diff_index==-1 and not long_word.startswith(short_word):
                continue
            if word2 + '-' + word1 in union:
                continue
            union.append(word1 + '-' + word2)
            output.append(word1)
            output.append(word2)
    return union
    
def action_bruk(first, second, output=[]):
    union = []
    for word1 in first:
        for word2 in second:
            if len(word1)==1 or len(word2)==1:
                continue
            long_word = ''
            short_word = ''
            if len(word1) == len(word2) + 1:
                long_word = word1
                short_word = word2
            else:
                if len(word2) == len(word1) + 1:
                    long_word = word2
                    short_word = word1
                else:
                    continue
            diff_index = 0
            for i in range(0, len(short_word)):
                if long_word[i]!=short_word[i]:
                    diff_index = i
                    break
            diff_index+=1
            if diff_index<len(short_word):
                for i in range(diff_index, len(short_word)):
                    if long_word[i + 1]!=short_word[i]:
                        diff_index = -1
                        break
            if diff_index==-1 and not long_word.startswith(short_word[:-1]):
                continue
            if word2 + '-' + word1 in union:
                continue
            union.append(word1 + '-' + word2)
            output.append(word1)
            output.append(word2)
    return union

def action_anag(first, second, output=[]):
    union = []
    for i in first:
        for j in second:
            if i==j or len(i)!=len(j):
                continue
            list1 = list(i)
            list2 = list(j)
            list1.sort()
            list2.sort()
            if list1 != list2:
                continue
            if j + '-' + i in union:
                continue
            union.append(i + '-' + j)
            output.append(i)
            output.append(j)
    return union

def action_plus(first, second, output=[]):
    union = []
    for word1 in first:
        for word2 in second:
            long_word = ''
            short_word = ''
            if len(word1) == len(word2) + 1:
                long_word = word1
                short_word = word2
            else:
                if len(word2) == len(word1) + 1:
                    long_word = word2
                    short_word = word1
                else:
                    continue
            long_list = list(long_word)
            short_list = list(short_word)
            long_list.sort()
            short_list.sort()
            diff_index = -2
            for i in range(0, len(short_list)):
                if long_list[i]!=short_list[i]:
                    diff_index = i
                    break
            if diff_index==-2:
                diff_index = -1
            else:
                for i in range(diff_index, len(short_list)):
                    if long_list[i + 1]!=short_list[i]:
                        diff_index = -2
                        break
            if diff_index==-2:
                continue
            if long_list[diff_index] + ': ' + word2 + '-' + word1 in union:
                continue
            union.append(long_list[diff_index] + ': ' + word1 + '-' + word2)
            output.append(word1)
            output.append(word2)
    union.sort()
    return union

def action_matr(first, second, third, output=[]):
    union = []
    for i in first:
        for j in second:
            if i==j:
                continue
            for index in range(0, len(i)-2):
                the_matr = i[index:index+3]
                if not the_matr in j:
                    continue
                for k in third:
                    if i==k or j==k:
                        continue
                    if not the_matr in k:
                        continue
                    if is_matr_exist(the_matr,i,j,k,union):
                        continue
                    union.append(the_matr + ': ' + i + '-' + j + '-' + k)
                    output.append(i)
                    output.append(j)
                    output.append(k)
    return union

def is_matr_exist(the_matr,i,j,k,union):
    return (the_matr + ': ' + j + '-' + i + '-' + k in union
    or the_matr + ': ' + k + '-' + i + '-' + j in union
    or the_matr + ': ' + i + '-' + k + '-' + j in union
    or the_matr + ': ' + j + '-' + k + '-' + i in union
    or the_matr + ': ' + k + '-' + j + '-' + i in union)

def main():
    # handler = Holder.default_text_handlers_by_modes[ModeType.Olymp]
    # start = time.time()
    
    # result = handler.do_action('кошка.собака,копыто')
    # end = time.time()
    # print(end - start)


    
    #input = 'кошка.собака,копыто'.strip().split('.')
    #first = parse_and_get_associations(input[0])
    #second = parse_and_get_associations(input[1])
    #action_result = do_action(first, second, ModeType.Olymp)
    #union = list(dict.fromkeys(action_result))
    #action_result = do_action(first, second, ModeType.Gibrid)
    #union = list(dict.fromkeys(action_result))



    #global pwd
    #settings = Settings()
    #session = requests.session()
    #settings.session = session
    #en_authorize(session, 'SanJJJJOk', pwd)
    #resp = session.get('http://ahtubinsk.en.cx/GameScenario.aspx?gid=67067')
    #get_img_tags(resp.text, settings)
    #get_words(settings, 10)

    #resp = session.get('http://72.en.cx/GameScenario.aspx?gid=67242')
    #resp = session.get('http://redray.en.cx/GameScenario.aspx?gid=67224')
    #ttt = get_img_tags(resp.text)
    #tttt = get_words(ttt[:20])
    #update = FakeUpdate()
    #update.message.text = ' '.join(tttt[1])
    #default_input(update,None,ModeType.Special,False,update.message.text)

    #answer = do_zaebis(update, None)
    updater = Updater("408100374:AAEhMleUbdVH_G1xmKeCAy8MlNfyBwB9AOo", use_context=True)
    #updater = Updater("979411435:AAEHIVLx8L8CxmjIHtitaH4L1GeV_OCRJ7M", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler(TgCommands.Olymp, tg_olymp))
    dp.add_handler(CommandHandler(TgCommands.Gibrid, tg_gibrid))
    dp.add_handler(CommandHandler(TgCommands.Meta, tg_meta))
    dp.add_handler(CommandHandler(TgCommands.Logo, tg_logo))
    dp.add_handler(CommandHandler(TgCommands.SwitchMode, tg_switch_mode))
    dp.add_handler(CommandHandler(TgCommands.Test, tg_test))
    dp.add_handler(MessageHandler(Filters.text, tg_default))

    dp.add_error_handler(tg_error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
