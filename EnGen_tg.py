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
from datetime import datetime, date, timedelta

from threading import Thread
from threading import Timer
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class TgCommands:
    Auto = 'auto'
    Go = 'go'
    Stop = 'stop'
    Set = 'set'

def tg_error(update, context):
    err_msg = "Callback: {0}".format(str(context.error))
    update.message.reply_text(err_msg)
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    
Holder = GlobalInfo()
Is_monitoring_active = False
Teams = []
Output_arr = []
Domain = 'kurgan'
Gameid = '68107'

def tg_set(update, context):
    global Is_monitoring_active, Teams, Domain, Gameid
    try:
        input_teams = update.message.text[len(TgCommands.Set)+2:].split(' ')
        
        teams = []
        fp = request.urlopen("http://m."+Domain+".en.cx/GameStat.aspx?gid="+Gameid)
        mybytes = fp.read()

        mystr = mybytes.decode("utf8")
        fp.close()

        soup = BeautifulSoup(mystr, 'html.parser')
        regex_m = re.compile("^totalCell")
        find_text3 = soup.find_all("td", {'class': regex_m})
    
        allteams = []
        for itemstat in find_text3:
            teamname = itemstat.find("a").get_text()
            if not teamname in allteams:
                allteams.append(teamname)

        for team in allteams:
            for inputteam in input_teams:
                if inputteam in team and not team in teams:
                    teams.append(team)

        Teams = teams
        update.message.reply_text('\n'.join(teams))
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)

def tg_auto_teams(update, context):
    global Is_monitoring_active, Teams, Domain, Gameid
    try:
        teams = []
        fp = request.urlopen("http://m."+Domain+".en.cx/GameStat.aspx?gid="+Gameid)
        mybytes = fp.read()

        mystr = mybytes.decode("utf8")
        fp.close()

        soup = BeautifulSoup(mystr, 'html.parser')
        regex_m = re.compile("^totalCell")
        find_text3 = soup.find_all("td", {'class': regex_m})
    
        teamname = find_text3[1].find("a").get_text()
        if not 'Win Team' in teamname:
            teams.append(teamname)
        teamname = find_text3[3].find("a").get_text()
        if not 'Win Team' in teamname:
            teams.append(teamname)
        teamname = find_text3[5].find("a").get_text()
        if not 'Win Team' in teamname:
            teams.append(teamname)
        Teams = teams
        update.message.reply_text('\n'.join(teams))
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)

def tg_update(update, context, domain, gameid):
    global Is_monitoring_active, Teams, Output_arr, Domain, Gameid
    try:
        while Is_monitoring_active:
            fp = request.urlopen("http://m."+Domain+".en.cx/GameBonusPenaltyTime.aspx?gid="+Gameid)
            mybytes = fp.read()

            mystr = mybytes.decode("utf8")
            fp.close()

            soup = BeautifulSoup(mystr, 'html.parser')
            regex_t = re.compile("^PlayersRepeater")
            find_text1 = soup.find_all('tr', {'id': regex_t})

            reply_str = ''
            for i in find_text1:
                listt = [ ii for ii in i.children if ii.name=='td' ]
                st_team = listt[1].get_text()
                st_time = listt[0].get_text()
                st_key = st_team + st_time
                if not st_key in Output_arr:
                    if st_team in Teams:
                        st_text = listt[-1].get_text()
                        reply_str = reply_str + '\n' + st_text
                    Output_arr.append(st_key)

            time.sleep(5)
        update.message.reply_text("i'm off")
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)

def tg_go(update, context):
    global Is_monitoring_active
    try:
        Is_monitoring_active = True
        url = update.message.text[len(TgCommands.Go)+2:]
        x = Thread(target=tg_update, args=(update,context,url,))
        x.start()
        update.message.reply_text('started')
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)

def tg_stop(update, context):
    global Is_monitoring_active
    try:
        Is_monitoring_active = False
        update.message.reply_text('stopped')
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)

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
    #fp = request.urlopen("http://m.kurgan.en.cx/GameBonusPenaltyTime.aspx?tid=10301&level=0&gid=68107")
    #fp = request.urlopen("http://m.kurgan.en.cx/GameBonusPenaltyTime.aspx?gid=68107")
    #fp = request.urlopen("http://m.kurgan.en.cx/GameStat.aspx?gid=68107")
    #mybytes = fp.read()

    #mystr = mybytes.decode("utf8")
    #fp.close()

    #file = open('125.txt', 'w', encoding='utf-8')
    #file.truncate(0)
    #file.write(mystr)
    #file.close()

    
    file = open('124.txt', 'r', encoding='utf-8')
    mystr_stat = file.read()
    file.close()


    file = open('125.txt', 'r', encoding='utf-8')
    mystr = file.read()
    file.close()
    output_dict = {}

    soup = BeautifulSoup(mystr_stat, 'html.parser')
    regex_m = re.compile("^totalCell")
    find_text3 = soup.find_all("td", {'class': regex_m})

    #------------------------------------------top team------------------------------------------
    list_top4 = []
    top_team = find_text3[0].find("a").get_text()
    if not 'Win Team' in top_team:
        list_top4.append(top_team)
        
    top_team = find_text3[2].find("a").get_text()
    if not 'Win Team' in top_team:
        list_top4.append(top_team)
        
    top_team = find_text3[4].find("a").get_text()
    if not 'Win Team' in top_team:
        list_top4.append(top_team)
        
    top_team = find_text3[6].find("a").get_text()
    if not 'Win Team' in top_team:
        list_top4.append(top_team)
    #------------------------------------------top team------------------------------------------
    #otwt_val = -1
    #for key in output_dict:
    #    if 'Win Team' in key:
    #        otwt_val = output_dict[key]
    #for key in output_dict:
    #    output_dict[key] = output_dict[key] - otwt_val

    #output_sorted = {}
    #list_d = list(output_dict.items())
    #list_d.sort(key=lambda i: i[1], reverse=True)
    #output_str = ''
    #for i in list_d:
    #    output_str = output_str + '\n' +  str(i[1]) + '-' + i[0]

    soup = BeautifulSoup(mystr, 'html.parser')
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

    updater = Updater("408100374:AAEhMleUbdVH_G1xmKeCAy8MlNfyBwB9AOo", use_context=True)
    #updater = Updater("979411435:AAEHIVLx8L8CxmjIHtitaH4L1GeV_OCRJ7M", use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler(TgCommands.Auto, tg_auto_teams))
    dp.add_handler(CommandHandler(TgCommands.Go, tg_go))
    dp.add_handler(CommandHandler(TgCommands.Stop, tg_stop))
    dp.add_handler(CommandHandler(TgCommands.Set, tg_set))
    #dp.add_handler(MessageHandler(Filters.text, tg_p_default))
    
    dp.add_error_handler(tg_error)

    updater.start_polling()
    
    updater.idle()


if __name__ == '__main__':
    main()
