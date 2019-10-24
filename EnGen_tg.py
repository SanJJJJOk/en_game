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

def tg_olymp(update, context):
    if not is_authorized(update):
        return
    default_input(update, context, ModeType.Olymp)

def tg_gibrid(update, context):
    if not is_authorized(update):
        return
    default_input(update, context, ModeType.Gibrid)

def tg_meta(update, context):
    if not is_authorized(update):
        return
    default_input(update, context, ModeType.Meta)

def tg_logo(update, context):
    if not is_authorized(update):
        return
    default_input(update, context, ModeType.Logo)

def tg_switch_mode(update, context):
    global Holder
    if not is_authorized(update):
        return
    settings = Holder.get(update.message.chat.id)
    mode = settings.current_mode
    if len(update.message.text) < 7:
        mode = settings.next_mode()
    else:
        prefix = update.message.text[6:]
        newmode = is_started_with(prefix, ModeType.get_well_known_mode_types())
        if len(newmode)==0:
            update.message.reply_text('invalid request. mode not found')
            return
        else:
            if len(newmode)>1:
                update.message.reply_text('invalid request. more than one mode found')
                return
            else:
                mode = newmode[0]
    update.message.reply_text('switched to ' + mode.name)

def tg_default(update, context):
    mode = Holder.get(update.message.chat.id).current_mode
    if (mode == ModeType.Disabled):
        return
    default_input(update, context, mode)

def default_input(update, context, mode):
    input = update.message.text.strip().split('.')
    if len(input) != 2:
        update.message.reply_text('invalid request')
        return
    msg =  do_beautiful(input, mode)
    update.message.reply_text(msg)

def is_authorized(update):
    if update.message.chat.id in Holder.settings_by_id:
        return True
    else:
        Holder.add(update.message.chat.id)
        return True
        #update.message.reply_text('you are not authorized, please call /start')
        #return False

#----------

def do_beautiful(input, mode):
    first = get_input_associations(input[0].strip())
    second = get_input_associations(input[1].strip())
    action_result = do_action(first, second, mode)
    union = list(dict.fromkeys(action_result))
    msg = '\n'.join(union)
    return str(len(union)) + '\n' + msg

def do_action(first, second, mode):
    if mode == ModeType.Olymp:
        return action_olymp(first, second)
    if mode == ModeType.Gibrid:
        return action_gibrid(first, second)
    if mode == ModeType.Meta:
        return action_meta(first, second)
    if mode == ModeType.Logo:
        return action_logo(first, second)
    return []

def action_olymp(first, second):
    return list(set(first).intersection(second))

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
                union.append(word1 + '-' + word2)
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

def is_started_with(prefix, mapper: dict):
    result = []
    for word in mapper.keys():
        if word.startswith(prefix):
            result.append(mapper[word])
    return result
    pass

def main():
    #update = FakeUpdate()
    #update.message.text = '/mode o'
    #t = tg_switch_mode(update, None)
    updater = Updater("408100374:AAEhMleUbdVH_G1xmKeCAy8MlNfyBwB9AOo", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("o", tg_olymp))
    dp.add_handler(CommandHandler("g", tg_gibrid))
    dp.add_handler(CommandHandler("m", tg_meta))
    dp.add_handler(CommandHandler("l", tg_logo))
    dp.add_handler(CommandHandler("mode", tg_switch_mode))
    dp.add_handler(MessageHandler(Filters.text, tg_default))

    dp.add_error_handler(tg_error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
