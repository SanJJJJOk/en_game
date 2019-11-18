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

def simple_message_handler(update, command, empty_is_invalid = False):
    bot_authorize(update)
    input_text = update.message.text
    if len(input_text)<len(command)+3:
        if empty_is_invalid:
            raise Exception('command should contains arguments')
        return None
    return input_text[len(command)+2:]

def tg_en_auth(update, context):
    global Holder
    try:
        input_text = simple_message_handler(update, TgCommands.EnAuth, True)
        input = input_text.strip().split(' ')
        if len(input)!=2:
            raise Exception('invalid request')
        settings = Holder.get(update.message.chat.id)
        is_en_auth = en_authorize(settings.session, input[0], input[1])
        update.message.reply_text(is_en_auth)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_load_imgs(update, context):
    global Holder
    try:
        input_text = simple_message_handler(update, TgCommands.LoadImgs, True)
        settings = Holder.get(update.message.chat.id)
        resp = settings.session.get(input_text)
        settings.game_imgs = get_img_tags(resp.text)
        update.message.reply_text('images is loaded: {0} count'.format(len(settings.game_imgs)))
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_yandex_img_request(update, context):
    global Holder
    try:
        input_text = simple_message_handler(update, TgCommands.ImgReq, False)
        settings = Holder.get(update.message.chat.id)
        search_count = len(settings.game_imgs)
        if not input_text is None:
            search_count = int(input_text)
        result = get_words(settings.game_imgs, search_count)
        settings.yandex_tags_filtered = result[0]
        settings.yandex_tags_all = result[1]
        settings.not_found_imgs = result[2]
        update.message.reply_text('yahoo')
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_print_words(update, context):
    global Holder
    try:
        bot_authorize(update)
        settings = Holder.get(update.message.chat.id)
        update.message.reply_text(len(settings.game_imgs))
        print_long(update, '\n'.join(settings.game_imgs))
        update.message.reply_text(len(settings.yandex_tags_filtered))
        print_long(update, ' '.join(settings.yandex_tags_filtered))
        print_long(update, '\n'.join(settings.yandex_tags_filtered))
        update.message.reply_text(len(settings.yandex_tags_all))
        print_long(update, ' '.join(settings.yandex_tags_all))
        print_long(update, '\n'.join(settings.yandex_tags_all))
        update.message.reply_text(len(settings.not_found_imgs))
        print_long(update, '\n'.join(settings.not_found_imgs))
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_imgs_action(update, context):
    global Holder
    try:
        bot_authorize(update)
        settings = Holder.get(update.message.chat.id)
        do_ohuenno(settings.yandex_tags_filtered, settings.yandex_tags_filtered, [ModeType.Gibrid, ModeType.Meta, ModeType.Logo, ModeType.Anag], False)
        do_ohuenno(settings.yandex_tags_all, settings.yandex_tags_all, [ModeType.Gibrid, ModeType.Meta, ModeType.Logo, ModeType.Anag], False)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_olymp(update, context):
    try:
        input_text = simple_message_handler(update, TgCommands.Olymp, True)
        msg = default_input(input_text, ModeType.Olymp)
        update.message.reply_text(msg)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_gibrid(update, context):
    try:
        input_text = simple_message_handler(update, TgCommands.Gibrid, True)
        msg = default_input(input_text, ModeType.Gibrid)
        update.message.reply_text(msg)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_meta(update, context):
    try:
        input_text = simple_message_handler(update, TgCommands.Meta, True)
        msg = default_input(input_text, ModeType.Meta)
        update.message.reply_text(msg)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_logo(update, context):
    try:
        input_text = simple_message_handler(update, TgCommands.Logo, True)
        msg = default_input(input_text, ModeType.Logo)
        update.message.reply_text(msg)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_switch_mode(update, context):
    global Holder
    try:
        input_text = simple_message_handler(update, TgCommands.SwitchMode, False)
        settings = Holder.get(update.message.chat.id)
        mode = settings.current_mode
        if input_text is None:
            mode = settings.next_mode()
        else:
            newmode = ModeType.get_modes_by_alias(input_text)
            if len(newmode)==0:
                raise Exception('invalid request. mode not found')
            else:
                if len(newmode)>1:
                    raise Exception('invalid request. more than one mode found:\n' + '\n'.join([str(mode_int) for mode_int in newmode]))
                else:
                    mode = newmode[0]
                    settings.current_mode = mode
        update.message.reply_text('switched to ' + mode.name)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_default(update, context):
    try:
        bot_authorize(update)
        input_text = update.message.text
        mode = Holder.get(update.message.chat.id).current_mode
        if mode == ModeType.Disabled:
            return
        if mode == ModeType.Special:
            parsed = special_parse(input_text)
            output_messages = do_special_search(parsed[0], parsed[1], [ModeType.Gibrid, ModeType.Meta, ModeType.Logo, ModeType.Anag])
            for msg in output_messages:
                print_long(msg)
            return
        if input_text[0]=='$':
            parsed = special_parse(input_text[1:])
            output_messages = do_special_search(parsed[0], parsed[1], [mode])
            for msg in output_messages:
                print_long(msg)
            return
        msg = default_input(input_text, mode)
        update.message.reply_text(msg)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

#def default_list_print(update, words, prefix = None):
#    output_str = str(len(words)) + '\n' + '\n'.join(words)
#    if not prefix in None:
#        output_str = prefix + '\n' + output_str
#    update.message.reply_text(output_str)
    
def print_long(update, input_text):
    if len(input_text) > 4096:
        for x in range(0, len(input_text), 4096):
            update.message.reply_text(input_text[x:x+4096])
    else:
        update.message.reply_text(input_text)

def bot_authorize(update):
    global Holder
    if not update.message.chat.id in Holder.settings_by_id:
        Holder.add(update.message.chat.id)
        return
        #raise Exception('you are not authorized, please call /start')

#----------

def do_special_search(first, second, modes, print_needless = True):
    needless_words = []
    output_messages = []
    for mode in modes:
        action_result = []
        if mode == ModeType.Matr:
            action_result = action_matr(first, first, second, needless_words)
        else:
            action_result = do_action(first, second, mode, needless_words)
        union = list(dict.fromkeys(action_result))
        output_messages.append(str(mode) + ':\n' + str(len(union)) + '\n' + '\n'.join(union))
    if not print_needless:
        return output_messages
    union_nl = []
    for word in first:
        if not word in needless_words:
            union_nl.append(word)
    output_messages.append('needless words:\n' + str(len(union_nl)) + '\n' + '\n'.join(union_nl))
    return output_messages
    
def special_parse(input_text):
    need_associations = False
    if input_text[0]=='+':
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
    return [first, second]

def default_input(input_text, mode):
    input = input_text.strip().split('.')
    if mode == ModeType.Matr:
        if len(input) != 3:
            raise Exception('invalid request')
        first = parse_and_get_associations(input[0])
        second = parse_and_get_associations(input[1])
        third = parse_and_get_associations(input[2])
        action_result = action_matr(first, second, third)
        union = list(dict.fromkeys(action_result))
        return str(len(union)) + '\n' + '\n'.join(union)
        return
    if len(input) != 2:
        raise Exception('invalid request')
    first = parse_and_get_associations(input[0])
    second = parse_and_get_associations(input[1])
    action_result = do_action(first, second, mode)
    union = list(dict.fromkeys(action_result))
    return str(len(union)) + '\n' + '\n'.join(union)

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

def parse_and_get_associations(input_str):
    input_words = input_str.strip().split(',')
    union = []
    for word in input_words:
        corrected_word = word.strip().lower()
        if corrected_word[0]=='!':
            corrected_word = corrected_word[1:]
        else:
            associations = get_associations(corrected_word)
            union.extend(associations)
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

def get_img_tags(html_text):
    soup = BeautifulSoup(html_text)
    imgs = soup.findAll('img')
    return [img['src'] for img in imgs]

def get_words(img_urls, search_count):
    if search_count<len(img_urls):
        img_urls = img_urls[:search_count]
    output1 = []
    output2 = []
    output3 = []
    for img_url in img_urls:
        tags = get_yandex_tags(img_url)
        if len(tags)==0:
            output3.append(img_url)
        for tag in tags:
            if tag.count(' ')==0:
                output1.append(tag)
            tag_words = re.findall(r"[\w']+", tag)
            output2.extend(tag_words)
    output1 = list(dict.fromkeys(output1))
    output2 = list(dict.fromkeys(output2))
    return [output1, output2, output3]

def get_yandex_tags(img_url):
    url = 'https://yandex.ru/images/search?url={0}&rpt=imageview'.format(quote(img_url, safe=''))
    try:
        fp = request.urlopen(url)
    except:
        return []
    mybytes = fp.read()
    
    mystr = mybytes.decode("utf8")
    fp.close()
    
    soup = BeautifulSoup(mystr)
    ass_list = soup.find('div', {'class': 'tags__wrapper'})
    if ass_list is None:
        return []
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

    dp.add_handler(CommandHandler(TgCommands.EnAuth, tg_en_auth))
    dp.add_handler(CommandHandler(TgCommands.LoadImgs, tg_load_imgs))
    dp.add_handler(CommandHandler(TgCommands.ImgReq, tg_yandex_img_request))
    dp.add_handler(CommandHandler(TgCommands.PrintWords, tg_print_words))
    dp.add_handler(CommandHandler(TgCommands.ImgsAction, tg_imgs_action))
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
