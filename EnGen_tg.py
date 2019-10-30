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
import requests
from bs4 import *
from urllib.parse import quote
import random

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
    update.message.reply_text('switched to ' + mode.name)

def tg_default(update, context):
    mode = Holder.get(update.message.chat.id).current_mode
    if (mode == ModeType.Disabled):
        return
    default_input(update, context, mode, False, update.message.text)

def default_input(update, context, mode, is_org, input_text):
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

#----------

def do_beautiful(input, mode, is_org):
    #if mode == ModeType.Olymp:
        #res = tmp_olymp(input)
        #msg = '\n'.join(res)
        #return str(len(res)) + '\n' + msg
    first = get_input_associations(input[0].strip(), is_org)
    second = get_input_associations(input[1].strip(), is_org)
    if mode == ModeType.Special:
        action_g = do_action(first, second, ModeType.Gibrid)
        action_m = do_action(first, second, ModeType.Meta)
        action_l = do_action(first, second, ModeType.Logo)
        union_g = list(dict.fromkeys(action_g))
        union_m = list(dict.fromkeys(action_m))
        union_l = list(dict.fromkeys(action_l))
        return str(len(union_g)) + '\n' + '\n'.join(union_g) + str(len(union_m)) + '\n' + '\n'.join(union_m) + str(len(union_l)) + '\n' + '\n'.join(union_l)
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

def action_logo(first, second):
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
            if diff_index!=-1:
                union.append(word1 + '-' + word2)
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

#def fill_game(input):
#    global Holder
#    game = TestGame()
#    random.seed()

#    success = False
#    simple_range = list(range(len(input)))
#    counter = 0
#    while not success:
#        counter += 1
#        print(counter)
#        input_words = []
#        random.shuffle(simple_range)
#        for i in range(8):
#            input_words.append(input[simple_range[i]])
#        w9 = get_rand_word(input_words[0],input_words[1])
#        if w9==None:
#            continue
#        w10 = get_rand_word(input_words[2],input_words[3])
#        if w10==None:
#            continue
#        w11 = get_rand_word(input_words[4],input_words[5])
#        if w11==None:
#            continue
#        w12 = get_rand_word(input_words[6],input_words[7])
#        if w12==None:
#            continue
#        w13 = get_rand_word(w9,w10)
#        if w13==None:
#            continue
#        w14 = get_rand_word(w11,w12)
#        if w14==None:
#            continue
#        w15 = get_rand_word(w13,w14)
#        if w15==None:
#            continue
#        game.words = input_words
#        game.words.append('-')
#        game.words.append(w9)
#        game.words.append(w10)
#        game.words.append(w11)
#        game.words.append(w12)
#        game.words.append('-')
#        game.words.append(w13)
#        game.words.append(w14)
#        game.words.append('-')
#        game.words.append(w15)
#        success = True
#    return game

#def get_rand_word(w1,w2):
#    ass1 = get_associations(w1)
#    ass2 = get_associations(w2)
#    union = list(set(ass1).intersection(ass2))
#    if len(union)==0:
#        return None
#    if len(union)<6:
#        return union[random.randint(0, len(union) - 1)]
#    return union[random.randint(0, 3)]

def main():
    #url = 'http://wordassociations.net/ru/{0}/{1}'.format(quote('ассоциации-к-слову'),quote('любовь'))
    #t = 0
    #try:
    #    fp = request.urlopen(url)
    #except:
    #    t = 1
    #mybytes = fp.read()
    
    #mystr = mybytes.decode("utf8")
    #fp.close()
    
    #soup = BeautifulSoup(mystr)
    #ass_list = soup.find('div', {'class': 'wordscolumn'})
    #a_list = ass_list.findAll('a')
    #ttt = [item.string for item in a_list]
    #lent = len(ttt)
    #game = fill_game(['картошка','мыло','квартира','дом','семья','корыто','бабушка','дерево','конкурс','малина','обед'])
    #test(input())
    #ttt = action_logo(['qwe','asdf'],['qwrr','asfdf'])
    #test()
    #update = FakeUpdate()
    #update.message.text = '/mode o'
    #t = tg_switch_mode(update, None)
    updater = Updater("408100374:AAEhMleUbdVH_G1xmKeCAy8MlNfyBwB9AOo", use_context=True)
    dp = updater.dispatcher

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
