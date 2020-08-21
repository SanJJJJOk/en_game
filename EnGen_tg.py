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
    Got = 'got'
    Stop = 'stop'
    Set = 'set'
    Game = 'game'
    Zeroon = 'zeroon'
    Zerooff = 'zerooff'

class Emjs:
    First = '\ud83e\udd47'
    Second = '\ud83e\udd48'
    Third = '\ud83e\udd49'
    Other = '\ud83d\udd35'
    Bonus = '\u2705'
    Penalty = '\u274c'
    Point = '\ud83d\udccd'

def tg_error(update, context):
    err_msg = "Callback: {0}".format(str(context.error))
    update.message.reply_text(err_msg)
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    
Holder = GlobalInfo()
Is_monitoring_active = False
Is_zeroarmormode_active = False
Teams = []
Output_arr = []
Domain = 'demo'
Gameid = '30837'
Team1 = 'Win Team'
Team2 = 'полоскун'

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

        for inputteam in input_teams:
            for team in allteams:
                if inputteam in team and not team in teams:
                    teams.append(team)

        Teams = teams
        update.message.reply_text('\n'.join(teams))
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)

def tg_auto_teams(update, context):
    global Is_monitoring_active, Teams, Domain, Gameid, Team1, Team2
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
        if not Team1 in teamname and not Team2 in teamname:
            teams.append(teamname)
        teamname = find_text3[3].find("a").get_text()
        if not Team1 in teamname and not Team2 in teamname:
            teams.append(teamname)
        teamname = find_text3[5].find("a").get_text()
        if not Team1 in teamname and not Team2 in teamname:
            teams.append(teamname)
        Teams = teams
        update.message.reply_text('\n'.join(teams))
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)

def tg_update(update, context):
    global Is_monitoring_active, Is_zeroarmormode_active, Teams, Output_arr, Domain, Gameid
    try:
        while Is_monitoring_active:
            fp = request.urlopen("http://m."+Domain+".en.cx/GameBonusPenaltyTime.aspx?gid="+Gameid)
            mybytes = fp.read()

            mystr = mybytes.decode("utf8")
            fp.close()

            soup = BeautifulSoup(mystr, 'html.parser')
            regex_t = re.compile("^PlayersRepeater")
            regex_zero = re.compile("([0-9]+)с")
            find_text1 = soup.find_all('tr', {'id': regex_t})

            reply_str = ''
            zero_str = ''
            for i in find_text1:
                listt = [ ii for ii in i.children if ii.name=='td' ]
                st_team = listt[1].get_text()
                st_time = listt[0].get_text()
                st_key = st_team + st_time
                if not st_key in Output_arr:
                    if st_team in Teams:
                        st_text = listt[-1].get_text()
                        st_acttxt = listt[-2].get_text()
                        reply_str = reply_str + '\n' + get_emjs(st_team, st_acttxt) + st_text
                    if Is_zeroarmormode_active:
                        st_textzero = listt[-1].get_text()
                        zeromatch = regex_zero.findall(st_textzero)
                        if len(zeromatch)==0:
                            zero_str = zero_str + '\n' + '...хуита(==0)'
                        else:
                            if len(zeromatch)>1:
                                zero_str = zero_str + '\n' + '...говно(>1)'
                            else:
                                intsecs = int(zeromatch[0])
                                if intsecs>=60:
                                    zero_str = zero_str + '\n' + st_textzero
                    Output_arr.append(st_key)

            if not reply_str=='':
                print_long(update, context, reply_str)
            if Is_zeroarmormode_active and not zero_str=='':
                print_long(update, context, Emjs.Point + zero_str)
            time.sleep(5)
        update.message.reply_text("i'm off")
    except Exception as e:
        err_msg = "неизвестная ошибка update: {0}".format(str(e))
        update.message.reply_text(err_msg)
        
def get_emjs(teamname, actiontxt):
    global Is_monitoring_active, Teams, Output_arr, Domain, Gameid
    teamemjs = Emjs.Other
    if len(Teams)>0 and teamname==Teams[0]:
        teamemjs = Emjs.First
    if len(Teams)>1 and teamname==Teams[1]:
        teamemjs = Emjs.Second
    if len(Teams)>2 and teamname==Teams[2]:
        teamemjs = Emjs.Third
    if 'бонус' in actiontxt or 'bonus' in actiontxt:
        return teamemjs + '-' + Emjs.Bonus
    return teamemjs + '-' + Emjs.Penalty

def print_long(update, context, input_text):
    global Is_monitoring_active, Teams, Output_arr, Domain, Gameid
    if len(input_text) == 0:
        context.bot.send_message('-442090041', '-')
        return
    if len(input_text) > 4096:
        for x in range(0, len(input_text), 4096):
            context.bot.send_message('-442090041', input_text[x:x+4096])
    else:
        context.bot.send_message('-442090041', input_text)

def tg_go(update, context):
    global Is_monitoring_active
    try:
        Is_monitoring_active = True
        url = update.message.text[len(TgCommands.Go)+2:]
        x = Thread(target=tg_update, args=(update,context,))
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

#--------------------------------------2--------------------------------------------------------
def tg_zeroon(update, context):
    global Is_zeroarmormode_active
    try:
        Is_zeroarmormode_active = True
        update.message.reply_text('zero+')
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        
def tg_zerooff(update, context):
    global Is_zeroarmormode_active
    try:
        Is_zeroarmormode_active = False
        update.message.reply_text('zero-')
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)

#--------------------------------------main--------------------------------------------------------

def main():
    #updater = Updater("408100374:AAEhMleUbdVH_G1xmKeCAy8MlNfyBwB9AOo", use_context=True)
    updater = Updater("979411435:AAEHIVLx8L8CxmjIHtitaH4L1GeV_OCRJ7M", use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler(TgCommands.Auto, tg_auto_teams))
    dp.add_handler(CommandHandler(TgCommands.Go, tg_go))
    dp.add_handler(CommandHandler(TgCommands.Stop, tg_stop))
    dp.add_handler(CommandHandler(TgCommands.Set, tg_set))
    dp.add_handler(CommandHandler(TgCommands.Game, tg_p_game))
    dp.add_handler(CommandHandler(TgCommands.Zeroon, tg_zeroon))
    dp.add_handler(CommandHandler(TgCommands.Zerooff, tg_zerooff))
    #dp.add_handler(MessageHandler(Filters.text, tg_p_default))
    
    dp.add_error_handler(tg_error)

    updater.start_polling()
    
    updater.idle()


if __name__ == '__main__':
    main()
