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
from urllib import request
import requests
from bs4 import *
from urllib.parse import quote
import random
import re

from datetime import datetime
from threading import Timer
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Define a global variables
Holder = SettingsHolder()
Gis = gis()

#tg methods

def tg_error(update, context):
	logger.warning('Update "%s" caused error "%s"', update, context.error)

def tg_gis(update, context):
    input_text = update.message.text[5:]
    do_search_city(update, input_text)
    return

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
    if not is_authorized(update):
        return
    input_text = update.message.text
    if len(input_text)<4:
        update.message.reply_text('invalid request')
        return
    default_input(update, context, ModeType.Olymp, False, input_text[3:])

def tg_olymp2(update, context):
    if not is_authorized(update):
        return
    input_text = update.message.text
    if len(input_text)<4:
        update.message.reply_text('invalid request')
        return
    default_input(update, context, ModeType.Olymp, True, input_text[3:])

def tg_gibrid(update, context):
    if not is_authorized(update):
        return
    input_text = update.message.text
    if len(input_text)<4:
        update.message.reply_text('invalid request')
        return
    default_input(update, context, ModeType.Gibrid, False, input_text[3:])

def tg_meta(update, context):
    if not is_authorized(update):
        return
    input_text = update.message.text
    if len(input_text)<4:
        update.message.reply_text('invalid request')
        return
    default_input(update, context, ModeType.Meta, False, input_text[3:])

def tg_logo(update, context):
    if not is_authorized(update):
        return
    input_text = update.message.text
    if len(input_text)<4:
        update.message.reply_text('invalid request')
        return
    default_input(update, context, ModeType.Logo, False, input_text[3:])

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
                settings.current_mode = mode
    update.message.reply_text('switched to ' + mode.name)

def tg_default(update, context):
    mode = Holder.get(update.message.chat.id).current_mode
    if (mode == ModeType.Disabled):
        return
    default_input(update, context, mode, False, update.message.text)

def default_input(update, context, mode, is_org, input_text):
    if mode == ModeType.Special:
        do_zaebis(update, context)
        return
    input = input_text.strip().split('.')
    if len(input) != 2:
        update.message.reply_text('invalid request')
        return
    msg =  do_beautiful(input, mode, is_org)
    update.message.reply_text(msg)

def is_authorized(update):
    if update.message.chat.id in Holder.settings_by_id:
        return True
    else:
        Holder.add(update.message.chat.id)
        return True
        #update.message.reply_text('you are not authorized, please call /start')
        #return False
        
def do_search_city(update, pattern):
    output_cities = []
    for city in Gis.all_cities:
        found = re.match(pattern,city)
        if not found is None:
            output_cities.append(city)
    update.message.reply_text(str(len(output_cities)) + '\n' + '\n'.join(output_cities))

def do_zaebis(update, context):
    global Gis
    input_text = update.message.text.strip().lower()
    pattern = '^' + input_text.replace('*','.*') + '$'
    do_search_city(update, pattern)
    return
    input_text = update.message.text.strip()
    need_print_useless = False
    if input_text[0]=='!':
        input_text = input_text[1:]
        need_print_useless = True
    input = input_text.strip().split('.')
    first = []
    second = []
    if len(input)==2:
        first = re.findall(r"[\w']+", input[0])
        second = re.findall(r"[\w']+", input[1])
        first.extend(second)
    else:
        first = re.findall(r"[\w']+", input_text)
        second = first
    first = [item.lower() for item in first]
    second = [item.lower() for item in second]
    output = []
    res_g = action_gibrid(first, second, output)
    res_m = action_meta(first, second, output)
    res_l = action_logo(first, second, output)
    res_a = action_anag(first, second, output)
    union_g = list(dict.fromkeys(res_g))
    union_m = list(dict.fromkeys(res_m))
    union_l = list(dict.fromkeys(res_l))
    union_a = list(dict.fromkeys(res_a))
    output_str = str(len(union_g)) + '\n' + '\n'.join(union_g) + '\n-\n' + str(len(union_m)) + '\n' + '\n'.join(union_m) + '\n-\n' + str(len(union_l)) + '\n' + '\n'.join(union_l) + '\n-\n' + str(len(union_a)) + '\n' + '\n'.join(union_a)
    update.message.reply_text(output_str)
    if not need_print_useless:
        return
    union_ul = []
    for word in first:
        if not word in output:
            union_ul.append(word)
    update.message.reply_text(str(len(union_ul)) + '\n' + '\n'.join(union_ul))

#----------

def do_beautiful(input, mode, is_org):
    #if mode == ModeType.Olymp:
        #res = tmp_olymp(input)
        #msg = '\n'.join(res)
        #return str(len(res)) + '\n' + msg
    first = get_input_associations(input[0].strip(), is_org)
    second = get_input_associations(input[1].strip(), is_org)
    #if mode == ModeType.Special:
    #    action_g = do_action(first, second, ModeType.Gibrid)
    #    action_m = do_action(first, second, ModeType.Meta)
    #    action_l = do_action(first, second, ModeType.Logo)
    #    union_g = list(dict.fromkeys(action_g))
    #    union_m = list(dict.fromkeys(action_m))
    #    union_l = list(dict.fromkeys(action_l))
    #    return str(len(union_g)) + '\n' + '\n'.join(union_g) + '\n-\n' + str(len(union_m)) + '\n' + '\n'.join(union_m) + '\n-\n' + str(len(union_l)) + '\n' + '\n'.join(union_l)
    action_result = do_action(first, second, mode)
    union = list(dict.fromkeys(action_result))
    msg = '\n'.join(union)
    return str(len(union)) + '\n' + msg

def tmp_olymp(input):
    input_chars = input[0].strip().split(',')
    input_words = input[1].strip().split(',')
    union = []
    for word in input_words:
        corrected_word = word.strip().lower()
        if corrected_word[0]=='!':
            corrected_word = corrected_word[1:]
        else:
            associations = get_associations(corrected_word)
            union.extend(associations)
        union.append(corrected_word)
    result = []
    for uword in union:
        if uword[0] in input_chars:
            result.append(uword)
    return result

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

def action_gibrid(first, second, output=[]):
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
    union.append('---')
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
            if counter == 1:
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
            if diff_index!=-1 or long_word.startswith(short_word):
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
            if list1 == list2:
                union.append(i + '-' + j)
                output.append(i)
                output.append(j)
    return union

def get_input_associations(input_str, s_org):
    input_words = input_str.split(',')
    union = []
    for word in input_words:
        corrected_word = word.strip().lower()
        if corrected_word[0]=='!':
            corrected_word = corrected_word[1:]
        else:
            associations = get_associations(corrected_word)
            union.extend(associations)
            if s_org:
                associations2 = get_associations2(corrected_word)
                corrected_ass2 = [item.lower() for item in associations2]
                union.extend(corrected_ass2)
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

def get_associations2(word):
    url = 'http://wordassociations.net/ru/{0}/{1}'.format(quote('ассоциации-к-слову'),quote(word))
    t = 0
    try:
        fp = request.urlopen(url)
    except:
        t = 1
    mybytes = fp.read()
    
    mystr = mybytes.decode("utf8")
    fp.close()
    
    soup = BeautifulSoup(mystr)
    ass_list = soup.find('div', {'class': 'wordscolumn'})
    a_list = ass_list.findAll('a')
    return [item.string for item in a_list]

def is_started_with(prefix, mapper: dict):
    result = []
    for key in mapper.keys():
        for word in mapper[key]:
            if word.startswith(prefix.lower()):
                result.append(key)
                break
    return result

def en_authorize(session, login, password):
    url = 'http://72.en.cx/Login.aspx?return=%%2f'
    userdata = {
        'socialAssign': 0,
        'Login': login,
        'Password': password,
        'EnButton1': 'Вход',
        'ddlNetwork': 1
    }

    resp = session.post(url, data=userdata)
    result = False
    if resp.history:
        logger.info("LogIN")
        result = True
    else:
        logger.info("LogOUT")
        result = False
    pass

def main():
    #update = FakeUpdate()
    #update.message.text = "А*ан"
    #answer = do_zaebis(update, None)
    updater = Updater("408100374:AAEhMleUbdVH_G1xmKeCAy8MlNfyBwB9AOo", use_context=True)
    #updater = Updater("979411435:AAEHIVLx8L8CxmjIHtitaH4L1GeV_OCRJ7M", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("test", tg_test))
    dp.add_handler(CommandHandler("gis", tg_gis))
    dp.add_handler(CommandHandler("z", tg_olymp2))
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
