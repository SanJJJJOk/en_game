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
from module2 import *
from TgTest import *
from gis import *
from urllib import request, parse
from bs4 import *
from urllib.parse import quote
import random
import re
import json
import time
import base64
from datetime import datetime, date, time, timedelta

from threading import Timer
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def tg_error(update, context):
    err_msg = "Callback: {0}".format(str(context.error))
    update.message.reply_text(err_msg)
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    
Holder = GlobalInfo()

class TgCommands:
    Move = 'move'
    Del = 'del'
    Add = 'add'
    FastAdd = 'fastadd'
    QuickDel = 'quickdel'
    Money = 'money'
    Help = 'help'
    Count = 'count'
    Fullstat = 'fullstat'
    Stat = 'stat'
    
#def is_meta_check(word1, word2):
#    if len(word1) != len(word2):
#        return False
#    counter = 0
#    for i in range(0, len(word1)):
#        if word1[i]!=word2[i]:
#            counter+=1
#    return counter == 1

#def is_logo_check(word1, word2):
#    long_word = ''
#    short_word = ''
#    if len(word1) == len(word2) + 1:
#        long_word = word1
#        short_word = word2
#    else:
#        if len(word2) == len(word1) + 1:
#            long_word = word2
#            short_word = word1
#        else:
#            return False
#    diff_index = 0
#    for i in range(0, len(short_word)):
#        if long_word[i]!=short_word[i]:
#            diff_index = i
#            break
#    for i in range(diff_index, len(short_word)):
#        if long_word[i + 1]!=short_word[i]:
#            diff_index = -1
#            break
#    return diff_index!=-1 or long_word.startswith(short_word)

#def smart_check(word, symbol):
#    if word in GlobalMonopoly.holder:
#        return None
#    for exist_word in GlobalMonopoly.holder:
#        if is_meta_check(exist_word, word) or is_logo_check(exist_word, word):
#            exist_symbols = [i.symbol for i in GlobalMonopoly.holder[exist_word]]
#            if symbol in exist_symbols:
#                return SmartResult(word, exist_word, True)
#            return SmartResult(word, exist_word, False)
#    return None





            #last_action = GlobalMonopoly.last_ations[update.message.from_user.id]
            #if not last_action is None:
            #    if last_action.action_type == ActionTypes.TypoMiss and last_action.msg_id == reply_msg.id:
            #        if update.message.text.startswith('д'):
            #            del GlobalMonopoly.holder[last_action.some_field.added_word]
            #            if not last_action.action_symbol in GlobalMonopoly.holder[last_action.action_word]:
            #                GlobalMonopoly.holder[last_action.action_word].append(last_action.action_symbol)
            #            update.message.reply_text('сделано')
            #            return
            #        if update.message.text.startswith('н'):
            #            GlobalMonopoly.last_ations[update.message.from_user.id] = None
            #            update.message.reply_text('ок, буду молчать в тряпочку')
            #            return
            #        update.message.reply_text('ну ёба, да или нет скажи, че ты мне пишешь?')
            #        return
        
                    #smart_check_result = smart_check(input_word, input_symbol)
                    #if smart_check_result is None:
                    #    add_result = add_word_symbol(input_word, input_symbol)
                    #    if add_result is None:
                    #        update.message.reply_text(Result.Result1 + 'было уже')
                    #    else:
                    #        update.message.reply_text(Result.Result0 + 'опачки, уже ' + str(add_result) + ' штуки')
                    #else:
                    #    add_result = add_word_symbol(input_word, input_symbol)
                    #    if smart_check_result.is_symbol_exist:
                    #        GlobalMonopoly.last_ations[update.message.from_user.id] = ActionItem(update.message.from_user.id, update.message.message_id, is_group_msg, text, input_word, input_symbol, smart_check_result, ActionTypes.TypoMiss)
                    #        update.message.reply_text('я, конечно, добавил "' + input_word  + '", но походу ты имел в виду "' + smart_check_result + '". причем "' + symbol + '" там уже существует. ответь реплаем на это сообщение да если хочешь исправить, нет - если не хочешь. или просто проигнорируй')
                    #    else:
                    #        GlobalMonopoly.last_ations[update.message.from_user.id] = ActionItem(update.message.from_user.id, update.message.message_id, is_group_msg, text, input_word, input_symbol, smart_check_result, ActionTypes.TypoMiss)
                    #        update.message.reply_text('я, конечно, добавил "' + input_word  + '", но походу ты имел в виду "' + smart_check_result + '". ответь реплаем на это сообщение да если хочешь исправить, нет - если не хочешь. или просто проигнорируй')


        #if text.startswith('+'):
        #    int_value = get_int(text[1:])
        #    if int_value is None:
        #        update.message.reply_text('эт не число')
        #        return
        #    GlobalMonopoly.money = GlobalMonopoly.money + int_value
        #    update.message.reply_text('добавлено ' + str(int_value) + ', осталось ' + str(GlobalMonopoly.money))
        #    return

        #if text.startswith('-'):
        #    int_value = get_int(text[1:])
        #    if int_value is None:
        #        update.message.reply_text('эт не число')
        #        return
        #    GlobalMonopoly.money = GlobalMonopoly.money - int_value
        #    update.message.reply_text('вычтено ' + str(int_value) + ', осталось ' + str(GlobalMonopoly.money))
        #    return

def get_small_info(word):
    if not word in GlobalMonopoly.holder:
        return None
    count = len(GlobalMonopoly.holder[word])
    new_symbols = [i.symbol for i in GlobalMonopoly.holder[word]]
    new_symbols.sort()
    return word + ' уже ' + str(count) + ' штук(' + ', '.join(new_symbols) + ')'

def get_int(text):
    try:
        return int(text)
    except Exception as e:
        return None

def tg_p_default(update, context):
    try:
        text = update.message.text.lower()
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
       
def tg_p_stat(update, context):
    try:
        #----------------------------------------count bonuses and penalties----------------------------
        fp = request.urlopen("http://m.kurgan.en.cx/GameBonusPenaltyTime.aspx?gid=68107")
        mybytes = fp.read()

        mystr_monitoring = mybytes.decode("utf8")
        fp.close()

        soup = BeautifulSoup(mystr_monitoring, 'html.parser')
        regex_t = re.compile("^PlayersRepeater")
        find_text1 = soup.find_all('tr', {'id': regex_t})

        count_bonuses = {}
        count_penalties = {}
        count_something = {}
        for i in find_text1:
            listt = [ ii for ii in i.children if ii.name=='td' ]
            st_teamname = listt[1].get_text()
            st_textbonus = listt[-2].get_text().lower()
            if 'бонус' in st_textbonus:
                if st_teamname in count_bonuses:
                    count_bonuses[st_teamname] = count_bonuses[st_teamname] + 1
                else:
                    count_bonuses[st_teamname] = 1
                continue
            if 'штраф' in st_textbonus:
                if st_teamname in count_penalties:
                    count_penalties[st_teamname] = count_penalties[st_teamname] + 1
                else:
                    count_penalties[st_teamname] = 1
                continue
            if st_teamname in count_something:
                count_something[st_teamname] = count_something[st_teamname] + 1
            else:
                count_something[st_teamname] = 1

        #----------------------------------------stat----------------------------

        output_dict = {}


        fp = request.urlopen(update.message.text[6:])
        mybytes = fp.read()

        mystr = mybytes.decode("utf8")
        fp.close()

        soup = BeautifulSoup(mystr, 'html.parser')
        regex_m = re.compile("^totalCell")
        find_text3 = soup.find_all("td", {'class': regex_m})

        for i in find_text3:
            txtitem = i.get_text()
            if 'бонус' in txtitem:
                ind = txtitem.index('бонус')
                txtbp = txtitem[ind+5:].replace(' ','')
                ttertert = get_count_sec(txtbp)
                team_name = i.find("a").get_text()
                output_dict[team_name] = ttertert
            if 'штраф' in txtitem:
                ind = txtitem.index('штраф')
                txtbp = txtitem[ind+5:].replace(' ','')
                ttertert = get_count_sec(txtbp)
                team_name = i.find("a").get_text()
                output_dict[team_name] = -ttertert
        
        otwt_val = -1
        for key in output_dict:
            if 'Win Team' in key:
                otwt_val = output_dict[key]
        for key in output_dict:
            output_dict[key] = output_dict[key] - otwt_val

        output_sorted = {}
        list_d = list(output_dict.items())
        list_d.sort(key=lambda i: i[1], reverse=True)
        output_str = ''
        for i in list_d:
            output_str = output_str + '\n' +  str(i[1]) + '-' + i[0] + '( '
            if i[0] in count_bonuses:
                output_str = output_str + str(count_bonuses[i[0]])
            else:
                output_str = output_str + '0'
            output_str = output_str + ' - '
            if i[0] in count_penalties:
                output_str = output_str + str(count_penalties[i[0]])
            else:
                output_str = output_str + '0'
            output_str = output_str + ' )'
            if i[0] in count_something:
                output_str = output_str + '***' + str(count_something[i[0]])

        update.message.reply_text(output_str)

    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))

def get_count_sec(input_str):
    output_sec = 0
    if 'ч' in input_str:
        ind = input_str.index('ч')
        curr = int(input_str[:ind])
        output_sec = output_sec + curr * 3600
        input_str = input_str[ind + 1:]
    if 'м' in input_str:
        ind = input_str.index('м')
        curr = int(input_str[:ind])
        output_sec = output_sec + curr * 60
        input_str = input_str[ind + 1:]
    if 'с' in input_str:
        ind = input_str.index('с')
        curr = int(input_str[:ind])
        output_sec = output_sec + curr
    return output_sec

def main():
    updater = Updater("408100374:AAEhMleUbdVH_G1xmKeCAy8MlNfyBwB9AOo", use_context=True)
    #updater = Updater("979411435:AAEHIVLx8L8CxmjIHtitaH4L1GeV_OCRJ7M", use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler(TgCommands.Stat, tg_p_stat))
    #dp.add_handler(MessageHandler(Filters.text, tg_p_default))
    
    dp.add_error_handler(tg_error)

    updater.start_polling()
    
    updater.idle()


if __name__ == '__main__':
    main()
