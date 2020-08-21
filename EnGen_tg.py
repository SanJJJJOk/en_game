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
from telegram import ParseMode

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def tg_error(update, context):
    err_msg = "Callback: {0}".format(str(context.error))
    update.message.reply_text(err_msg)
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    
Holder = GlobalInfo()
Domain = 'demo'
Gameid = '30837'
Team1 = 'Win Team'
Team2 = 'полоскун'

class TgCommands:
    Fullstat = 'fullstat'
    Stat = 'stat'
    Game = 'game'
    
def tg_p_fullstat(update, context):
    global Domain, Gameid
    try:
        fp = request.urlopen("http://m."+Domain+".en.cx/GameBonusPenaltyTime.aspx?gid="+Gameid)
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
            if 'bonus' in st_textbonus:
                if st_teamname in count_bonuses:
                    count_bonuses[st_teamname] = count_bonuses[st_teamname] + 1
                else:
                    count_bonuses[st_teamname] = 1
                continue
            if 'penalty' in st_textbonus:
                if st_teamname in count_penalties:
                    count_penalties[st_teamname] = count_penalties[st_teamname] + 1
                else:
                    count_penalties[st_teamname] = 1
                continue
            if st_teamname in count_something:
                count_something[st_teamname] = count_something[st_teamname] + 1
            else:
                count_something[st_teamname] = 1

        tg_base_stat(update, context, count_bonuses, count_penalties, count_something, True)

    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
        
def tg_p_stat(update, context):
    global Domain, Gameid
    try:
        tg_base_stat(update, context, {}, {}, {}, False)
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))

def tg_p_game(update, context):
    global Domain, Gameid
    try:
        input = update.message.text[len(TgCommands.Game)+2:].split(' ')
        Domain = input[0]
        Gameid = input[1]
        update.message.reply_text('збс,'+Domain+Gameid)
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))

def tg_base_stat(update, context, count_bonuses, count_penalties, count_something, add_bp):
    global Domain, Gameid, Team1, Team2
    output_dict = {}

    fp = request.urlopen("http://m."+Domain+".en.cx/GameStat.aspx?gid="+Gameid)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    soup = BeautifulSoup(mystr, 'html.parser')
    regex_m = re.compile("^totalCell")
    find_text3 = soup.find_all("td", {'class': regex_m})

    for i in find_text3:
        txtitem = i.get_text()
        if 'bonus' in txtitem:
            ind = txtitem.index('bonus')
            txtbp = txtitem[ind+5:].replace(' ','')
            ttertert = get_count_sec(txtbp)
            team_name = i.find("a").get_text()
            output_dict[team_name] = ttertert
        if 'penalty' in txtitem:
            ind = txtitem.index('penalty')
            txtbp = txtitem[ind+5:].replace(' ','')
            ttertert = get_count_sec(txtbp)
            team_name = i.find("a").get_text()
            output_dict[team_name] = -ttertert
        
    otwt_val = -1
    for key in output_dict:
        if Team1 in key or Team2 in key:
            otwt_val = output_dict[key]
    for key in output_dict:
        output_dict[key] = output_dict[key] - otwt_val

    output_sorted = {}
    list_d = list(output_dict.items())
    list_d.sort(key=lambda i: i[1], reverse=True)
    output_str = ''
    for i in list_d:
        output_str = output_str + '\n`' +  smart_extend(str(i[1]), 5) + '-' + smart_extend(i[0], 13) + '`'
        if not add_bp:
            continue
        output_str = output_str + '` '
        if i[0] in count_bonuses:
            output_str = output_str + int_extend_reverse(count_bonuses[i[0]])
        else:
            output_str = output_str + '0'
        output_str = output_str + '-'
        if i[0] in count_penalties:
            output_str = output_str + int_extend_reverse(count_penalties[i[0]])
        else:
            output_str = output_str + '0'
        output_str = output_str + '`'
        if i[0] in count_something:
            output_str = output_str + '***' + int_extend_reverse(count_something[i[0]])

    update.message.reply_text(output_str, parse_mode='markdown')
       
def smart_extend(input_str, amount):
    input_str = input_str.replace('`', '_')
    if len(input_str)>amount:
        return input_str[:amount]
    while len(input_str)<amount:
        input_str = input_str + ' '
    return input_str

def int_extend_reverse(input_int):
    input_str = str(input_int)
    while len(input_str)<3:
        input_str = ' ' + input_str
    return input_str

def get_count_sec(input_str):
    output_sec = 0
    if 'h' in input_str:
        ind = input_str.index('h')
        curr = int(input_str[:ind])
        output_sec = output_sec + curr * 3600
        input_str = input_str[ind + 1:]
    if 'm' in input_str:
        ind = input_str.index('m')
        curr = int(input_str[:ind])
        output_sec = output_sec + curr * 60
        input_str = input_str[ind + 1:]
    if 's' in input_str:
        ind = input_str.index('s')
        curr = int(input_str[:ind])
        output_sec = output_sec + curr
    return output_sec

def main():
    updater = Updater("408100374:AAEhMleUbdVH_G1xmKeCAy8MlNfyBwB9AOo", use_context=True)
    #updater = Updater("979411435:AAEHIVLx8L8CxmjIHtitaH4L1GeV_OCRJ7M", use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler(TgCommands.Game, tg_p_game))
    dp.add_handler(CommandHandler(TgCommands.Stat, tg_p_stat))
    dp.add_handler(CommandHandler(TgCommands.Fullstat, tg_p_fullstat))
    #dp.add_handler(MessageHandler(Filters.text, tg_p_default))
    
    dp.add_error_handler(tg_error)

    updater.start_polling()
    
    updater.idle()


if __name__ == '__main__':
    main()
