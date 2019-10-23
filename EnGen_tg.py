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
from urllib import request
from bs4 import *
from urllib.parse import quote

from datetime import datetime
from threading import Timer
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Define a global variables
Holder = SettingsHolder()

#tg methods

def tg_error(update, context):
	logger.warning('Update "%s" caused error "%s"', update, context.error)

def tg_switch_mode(update, context):
    global Holder
    if not is_authorized(update):
        return
    settings = Holder.get(update.message.chat.id)
    mode = settings.next_mode()
    update.message.reply_text('switched to ' + mode.name)

def tg_default(update, context):
    mode = Holder.get(update.message.chat.id).current_mode
    if (mode == ModeType.Nan):
        return
    input = update.message.text.strip().split('.')
    if len(input) != 2:
        update.message.reply_text('invalid input')
        return
    msg =  do_beautiful(input, mode)
    update.message.reply_text(msg)

def is_authorized(update):
    if update.message.chat.id in Holder.settings_by_id:
        return True
    else:
        Holder.add(update.message.chat.id)
        #update.message.reply_text('you are not authorized, please call /start')
        #return False

#----------

def do_beautiful(input, mode):
    first = get_input_associations(input[0].strip())
    second = get_input_associations(input[1].strip())
    union = []
    if mode_num == 0:
        union = list(set(first).intersection(second))
    else:
        if mode_num == 1:
            for i in first:
                for j in second:
                    if i[-3:] == j[0:3]:
                        union.append(i + '-' + j)
                    if i[0:3] == j[-3:]:
                        union.append(j + '-' + i)
        else:
            for i in first:
                for j in second:
                    meta_result = do_meta(i,j)
                    if meta_result:
                        union.append(i + '-' + j)

    result_union = list(dict.fromkeys(union))
    msg = '\n'.join(result_union)
    return str(len(result_union)) + '\n' + msg

def do_action(first, second, mode):
    if mode == ModeType.Olymp:
        return action_olymp(first, second)
    if mode == ModeType.Gibrid:
        return action_gibrid(first, second)
    if mode == ModeType.Meta:
        return action_meta(first, second)
    return []

def action_olymp(first, second):
    return  list(set(first).intersection(second))

def action_gibrid(first, second):
    union = []
    for i in first:
        for j in second:
            if i[-3:] == j[0:3]:
                union.append(i + '-' + j)
            if i[0:3] == j[-3:]:
                union.append(j + '-' + i)
    return union

def action_meta(first, second):
    union = []
    for word1 in first:
        for word2 in second:
            if len(word1) != len(word2):
                continue
            counter = 0
            for i in range(0, len(word1)):
                if word1[i]!=word2[i]:
                    counter+=1
            if counter == 1:
                union.append(i + '-' + j)
    return union

def get_input_associations(input_str):
    input_words = input_str.split(',')
    union = []
    for word in input_words:
        corrected_word = word.strip().lower()
        if corrected_word[0]=='!':
            corrected_word = corrected_word[1:]
        else:
            associations = get_associations(corrected_word)
            union.extend(associations)
        union.append(corrected_word)
    return union

def get_associations(word):
    url = 'http://www.sociation.org/word/{0}'.format(quote(word))
    try:
        fp = request.urlopen(url)
    except:
        return []
    mybytes = fp.read()
    
    mystr = mybytes.decode("utf8")
    fp.close()
    
    soup = BeautifulSoup(mystr)
    ass_list = soup.find('ol', {'class': 'associations_list'})
    a_list = ass_list.findAll('a')
    return [item.string for item in a_list]

def main():
    updater = Updater("408100374:AAEhMleUbdVH_G1xmKeCAy8MlNfyBwB9AOo", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("mode", tg_switch_mode))
    dp.add_handler(MessageHandler(Filters.text, do_zaebis))

    dp.add_error_handler(tg_error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
