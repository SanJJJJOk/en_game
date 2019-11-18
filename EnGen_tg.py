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
from urllib import request, parse #it is used for sociation request
import requests #from Ads, to create session
from bs4 import *
from urllib.parse import quote
import random
import re
import json

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
    update.message.reply_text("Error: {0}".format(str(e)))

def tg_test(update, context):
    newstr = ""
    #try:
    raise Exception()
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
    #except Exception as e:
    #    update.message.reply_text("Error: {0}".format(str(e)))

def tg_en_auth(update, context):
    global Holder
    try:
        if not is_authorized(update):
            return
        input_text = update.message.text
        if len(input_text)<5:
            update.message.reply_text('invalid request')
            return
        input_text = input_text[4:]
        input = input_text.strip().split(' ')
        if len(input)!=2:
            update.message.reply_text('invalid request')
            return
        settings = Holder.get(update.message.chat.id)
        is_en_auth = en_authorize(settings.session, input[0], input[1])
        update.message.reply_text(is_en_auth)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_load_imgs(update, context):
    global Holder
    try:
        if not is_authorized(update):
            return
        input_text = update.message.text
        if len(input_text)<7:
            update.message.reply_text('invalid request')
            return
        input_text = input_text[6:]
        settings = Holder.get(update.message.chat.id)
        resp = settings.session.get(input_text)
        get_img_tags(resp.text, settings)
        update.message.reply_text('images is loaded: {0} count'.format(len(settings.game_imgs)))
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_yandex_img_request(update, context):
    global Holder
    try:
        if not is_authorized(update):
            return
        settings = Holder.get(update.message.chat.id)
        search_count = len(settings.game_imgs)
        if len(update.message.text)>6:
            search_count = int(update.message.text[6:])
        get_words(settings, search_count)
        update.message.reply_text('yahoo')
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_print_words(update, context):
    global Holder
    try:
        if not is_authorized(update):
            return
        settings = Holder.get(update.message.chat.id)
        update.message.reply_text(len(settings.game_imgs))
        print_long(update, ' '.join(settings.game_imgs))
        print_long(update, '\n'.join(settings.game_imgs))
        update.message.reply_text(len(settings.yandex_tags_main))
        print_long(update, ' '.join(settings.yandex_tags_main))
        print_long(update, '\n'.join(settings.yandex_tags_main))
        update.message.reply_text(len(settings.yandex_tags_all))
        print_long(update, ' '.join(settings.yandex_tags_all))
        print_long(update, '\n'.join(settings.yandex_tags_all))
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def print_long(update, input_text):
    if len(input_text) > 4096:
        for x in range(0, len(input_text), 4096):
            update.message.reply_text(input_text[x:x+4096])
    else:
        update.message.reply_text(info)

def tg_imgs_action(update, context):
    global Holder
    try:
        if not is_authorized(update):
            return
        settings = Holder.get(update.message.chat.id)
        do_ohuenno(settings.yandex_tags_main, settings.yandex_tags_main, [ModeType.Gibrid, ModeType.Meta, ModeType.Logo, ModeType.Anag], False)
        do_ohuenno(settings.yandex_tags_all, settings.yandex_tags_all, [ModeType.Gibrid, ModeType.Meta, ModeType.Logo, ModeType.Anag], False)
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
        newmode = ModeType.get_modes_by_alias(prefix)
        if len(newmode)==0:
            update.message.reply_text('invalid request. mode not found')
            return
        else:
            if len(newmode)>1:
                update.message.reply_text('invalid request. more than one mode found:\n' + '\n'.join([str(mode_int) for mode_int in newmode]))
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
    try:
        if mode == ModeType.Special:
            do_zaebis(update, context, input_text, [ModeType.Gibrid, ModeType.Meta, ModeType.Logo, ModeType.Anag])
            return
        input = input_text.strip().split('.')
        if input_text[0]=='$':
            do_zaebis(update, context, input_text[1:], [mode])
            return
        if mode == ModeType.Matr:
            if len(input) != 3:
                update.message.reply_text('invalid request')
                return
            matr_msg = do_matr(input)
            update.message.reply_text(matr_msg)
            return
        if len(input) != 2:
            update.message.reply_text('invalid request')
            return
        msg =  do_beautiful(input, mode, is_org)
        update.message.reply_text(msg)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def is_authorized(update):
    if update.message.chat.id in Holder.settings_by_id:
        return True
    else:
        Holder.add(update.message.chat.id)
        return True
        #update.message.reply_text('you are not authorized, please call /start')
        #return False
        
def do_zaebis(update, context, input_text, modes):
    need_associations = False
    if input_text[0]=='$':
        input_text = input_text[1:]
        need_associations = True
    input = input_text.strip().split('.')
    first = []
    second = []
    if len(input)==2:
        first = re.findall(r"[\w']+", input[0])
        second = re.findall(r"[\w']+", input[1])
        if need_associations:
            first = get_first_associations(first, 5)
            second = get_first_associations(second, 5)
        first.extend(second)
    else:
        first = re.findall(r"[\w']+", input_text)
        if need_associations:
            first = get_first_associations(first, 5)
        second = first
    first = [item.lower() for item in first]
    second = [item.lower() for item in second]
    do_ohuenno(first, second, modes)

def do_ohuenno(first, second, modes, print_useless = True):
    output = []
    for mode in modes:
        action_result = []
        if mode == ModeType.Matr:
            action_result = action_matr(first, first, second, output)
        else:
            action_result = do_action(first, second, mode, output)
        union = list(dict.fromkeys(action_result))
        update.message.reply_text(str(mode) + ':\n' + str(len(union)) + '\n' + '\n'.join(union))
    if not print_useless:
        return
    union_ul = []
    for word in first:
        if not word in output:
            union_ul.append(word)
    update.message.reply_text('useless words:\n' + str(len(union_ul)) + '\n' + '\n'.join(union_ul))
    
def default_print(update, words, prefix = None):
    output_str = str(len(words)) + '\n' + '\n'.join(words)
    if not prefix in None:
        output_str = prefix + '\n' + output_str
    update.message.reply_text(output_str)

#----------

def do_beautiful(input, mode, is_org):
    first = get_input_associations(input[0].strip(), is_org)
    second = get_input_associations(input[1].strip(), is_org)
    action_result = do_action(first, second, mode)
    union = list(dict.fromkeys(action_result))
    msg = '\n'.join(union)
    return str(len(union)) + '\n' + msg

def do_action(first, second, mode, output = []):
    if mode == ModeType.Olymp:
        return action_olymp(first, second, output)
    if mode == ModeType.Gibrid:
        return action_gibrid(first, second, output)
    if mode == ModeType.Meta:
        return action_meta(first, second, output)
    if mode == ModeType.Logo:
        return action_logo(first, second, output)
    if mode == ModeType.Anag:
        return action_anag(first, second, output)
    if mode == ModeType.Plus:
        return action_plus(first, second, output)
    return []

def action_olymp(first, second, output=[]):
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
            if diff_index!=-2:
                union.append(long_list[diff_index] + ': ' + word1 + '-' + word2)
                output.append(word1)
                output.append(word2)
    union.sort()
    return union

def do_matr(input):
    first = get_input_associations(input[0].strip(), False)
    second = get_input_associations(input[1].strip(), False)
    third = get_input_associations(input[2].strip(), False)
    action_result = action_matr(first, second, third)
    union = list(dict.fromkeys(action_result))
    msg = '\n'.join(union)
    return str(len(union)) + '\n' + msg

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
                    if the_matr in k:
                        union.append(the_matr + ': ' + i + '-' + j + '-' + k)
                        output.append(i)
                        output.append(j)
                        output.append(k)
    return union

def get_input_associations(input_str, is_org):
    input_words = input_str.split(',')
    union = []
    for word in input_words:
        corrected_word = word.strip().lower()
        if corrected_word[0]=='!':
            corrected_word = corrected_word[1:]
        else:
            associations = get_associations(corrected_word)
            union.extend(associations)
            #if is_org:
                #associations2 = get_associations2(corrected_word)
                #corrected_ass2 = [item.lower() for item in associations2]
                #union.extend(corrected_ass2)
        if corrected_word[0]=='!':
            corrected_word = corrected_word[1:]
            associations = get_associations(corrected_word)
            if len(associations)>20:
                union.extend(associations[:20])
            else:
                union.extend(associations)
        union.append(corrected_word)
    return union

def get_first_associations(words, count):
    union = []
    for word in words:
        associations = get_associations(word)
        union.append(word)
        if len(associations)>count:
            union.extend(associations[:count])
        else:
            union.extend(associations)
    return list(dict.fromkeys(union))

def get_associations(input_word):
    data = parse.urlencode({
        'word':input_word,
        'back':False,
        'max_count':0
        }).encode()
    req =  request.Request('https://sociation.org/ajax/word_associations/', data=data)
    resp = request.urlopen(req)
    json_resp = json.load(resp)
    if not 'associations' in json_resp:
        return []
    associations = json_resp['associations']
    return [item['name'] for item in associations]

#def get_associations2(word):
#    url = 'http://wordassociations.net/ru/{0}/{1}'.format(quote('ассоциации-к-слову'),quote(word))
#    t = 0
#    try:
#        fp = request.urlopen(url)
#    except:
#        t = 1
#    mybytes = fp.read()
    
#    mystr = mybytes.decode("utf8")
#    fp.close()
    
#    soup = BeautifulSoup(mystr)
#    ass_list = soup.find('div', {'class': 'wordscolumn'})
#    a_list = ass_list.findAll('a')
#    return [item.string for item in a_list]

def get_img_tags(input_text, settings):
    soup = BeautifulSoup(input_text)
    imgs = soup.findAll('img')
    settings.game_imgs = [img['src'] for img in imgs]

def get_words(settings, search_count):
    img_urls = settings.game_imgs
    if search_count<len(settings.game_imgs):
        img_urls = settings.game_imgs[:search_count]
    output1 = []
    output2 = []
    for img_url in img_urls:
        tags = get_yandex_tags(img_url)
        for tag in tags:
            if tag.count(' ')==0:
                output1.append(tag)
            tag_words = re.findall(r"[\w']+", tag)
            output2.extend(tag_words)
    output1 = list(dict.fromkeys(output1))
    output2 = list(dict.fromkeys(output2))
    settings.yandex_tags_main = output1
    settings.yandex_tags_all = output2

def get_yandex_tags(img_url):
    url = 'https://yandex.ru/images/search?url={0}&rpt=imageview'.format(quote(img_url, safe=''))
    t = 0
    try:
        fp = request.urlopen(url)
    except:
        t = 1
    mybytes = fp.read()
    
    mystr = mybytes.decode("utf8")
    fp.close()
    
    soup = BeautifulSoup(mystr)
    ass_list = soup.find('div', {'class': 'tags__wrapper'})
    a_list = ass_list.findAll('a')
    return [item.string for item in a_list]

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
    if resp.history:
        logger.info("LogIN")
        return True
    else:
        logger.info("LogOUT")
        return False

def main():
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

    dp.add_handler(CommandHandler("en", tg_en_auth))
    dp.add_handler(CommandHandler("load", tg_load_imgs))
    dp.add_handler(CommandHandler("find", tg_yandex_img_request))
    dp.add_handler(CommandHandler("print", tg_print_words))
    dp.add_handler(CommandHandler("do", tg_imgs_action))
    dp.add_handler(CommandHandler("test", tg_test))
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
