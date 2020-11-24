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
    Go = 'go'
    Stop = 'stop'
    Game = 'game'
    LvlStat = 'lvlstat'
    Points = 'points'

class Emjs:
    First = '\ud83e\udd47'
    Second = '\ud83e\udd48'
    Third = '\ud83e\udd49'
    Other = '\ud83d\udd35'
    Bonus = '\u2705'
    Penalty = '\u274c'
    Point = '\ud83d\udccd'

class ActionItem:
    def __init__(self, e_time, e_team, e_lvl, e_bonus, e_score, e_itemid, e_user):
        self.e_time = e_time
        self.e_team = e_team
        self.e_lvl = e_lvl
        self.e_bonus = e_bonus
        self.e_score = e_score
        self.e_itemid = e_itemid
        self.e_user = e_user

def tg_error(update, context):
    err_msg = "Callback: {0}".format(str(context.error))
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    
Holder = GlobalInfo()
Is_monitoring_active = False
Auto_update = True
Output_arr = {}
Domain = '72'
Gameid = '70696'
#Team1 = 'Win Team'
#Team2 = 'полоскун'

#def tg_set(update, context):
#    global Is_monitoring_active, Teams, Domain, Gameid
#    try:
#        input_teams = update.message.text[len(TgCommands.Set)+2:].split(' ')
        
#        teams = []
#        fp = request.urlopen("http://m."+Domain+".en.cx/GameStat.aspx?gid="+Gameid)
#        mybytes = fp.read()

#        mystr = mybytes.decode("utf8")
#        fp.close()

#        soup = BeautifulSoup(mystr, 'html.parser')
#        regex_m = re.compile("^totalCell")
#        find_text3 = soup.find_all("td", {'class': regex_m})
    
#        allteams = []
#        for itemstat in find_text3:
#            teamname = itemstat.find("a").get_text()
#            if not teamname in allteams:
#                allteams.append(teamname)

#        for inputteam in input_teams:
#            for team in allteams:
#                if inputteam in team and not team in teams:
#                    teams.append(team)

#        Teams = teams
#        update.message.reply_text('\n'.join(teams))
#    except Exception as e:
#        err_msg = "неизвестная ошибка: {0}".format(str(e))
#        update.message.reply_text(err_msg)

#def tg_auto_teams(update, context):
#    global Is_monitoring_active, Teams, Domain, Gameid
#    try:
#        teams = []
#        fp = request.urlopen("http://m."+Domain+".en.cx/GameStat.aspx?gid="+Gameid)
#        mybytes = fp.read()

#        mystr = mybytes.decode("utf8")
#        fp.close()

#        soup = BeautifulSoup(mystr, 'html.parser')
#        regex_m = re.compile("^totalCell")
#        find_text3 = soup.find_all("td", {'class': regex_m})
    
#        #teamname = find_text3[1].find("a").get_text()
#        #if not Team1 in teamname and not Team2 in teamname:
#        #    teams.append(teamname)
#        #teamname = find_text3[3].find("a").get_text()
#        #if not Team1 in teamname and not Team2 in teamname:
#        #    teams.append(teamname)
#        #teamname = find_text3[5].find("a").get_text()
#        #if not Team1 in teamname and not Team2 in teamname:
#        #    teams.append(teamname)
#        Teams = teams
#        update.message.reply_text('\n'.join(teams))
#    except Exception as e:
#        err_msg = "неизвестная ошибка: {0}".format(str(e))
#        update.message.reply_text(err_msg)



#---------------------------------------def---------------------------------------------------------

def download_data():
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid
    fp = request.urlopen("http://"+Domain+".en.cx/GameBonusPenaltyTime.aspx?gid="+Gameid)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    soup = BeautifulSoup(mystr, 'html.parser')
    regex_t = re.compile("^PlayersRepeater")
    regex_zero = re.compile("([0-9]+)с")
    find_text1 = soup.find_all('tr', {'id': regex_t})

    action_items = []

    #TODO:

    
            #fp = request.urlopen("http://m."+Domain+".en.cx/GameBonusPenaltyTime.aspx?gid="+Gameid)
            #mybytes = fp.read()

            #mystr = mybytes.decode("utf8")
            #fp.close()

            #soup = BeautifulSoup(mystr, 'html.parser')
            #regex_t = re.compile("^PlayersRepeater")
            #regex_zero = re.compile("([0-9]+)с")
            #find_text1 = soup.find_all('tr', {'id': regex_t})

            #reply_str = ''
            #zero_str = ''
            #for i in find_text1:
            #    listt = [ ii for ii in i.children if ii.name=='td' ]
            #    st_team = listt[1].get_text()
            #    st_time = listt[0].get_text()
            #    st_key = st_team + st_time
            #    if not st_key in Output_arr:
            #        if st_team in Teams:
            #            st_text = listt[-1].get_text()

    return action_items

def update_data(action_items):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid
    new_items_ids = []
    for item in action_items:
        if not item.e_itemid in Output_arr:
            Output_arr[item.e_itemid] = item
            new_items_ids.append(item.e_itemid)
    return new_items_ids

#-------------------------------------tg-run-------------------------------------------------------

def tg_run(update, context):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid
    try:
        while Is_monitoring_active:
            action_items = download_data()
            new_items_ids = update_data(action_items)
            for id in new_items_ids:
                item = Output_arr[id]
                reply_str = reply_str + '\n'
                if item.e_bonus and item.e_score==1:
                    reply_str = reply_str + Emjs.Point
                else:
                    if item.e_bonus:
                        reply_str = reply_str + Emjs.Bonus
                    else:
                        reply_str = reply_str + Emjs.Penalty
                    reply_str = reply_str + '(' + item.e_score + 's)\n'
                reply_str = reply_str + item.e_team + ' at ' + str(item.e_time) + ' by ' + item.e_user
            if not reply_str=='':
                print_long(update, context, reply_str)
            time.sleep(60)
        update.message.reply_text("i'm off")
    except Exception as e:
        err_msg = "неизвестная ошибка update: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
        
#---------------------------------------tg---------------------------------------------------------

def tg_points_stat(update, context):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid
    try:
        input_int = int(update.message.text[len(TgCommands.Points)+2:])
        if Auto_update:
            action_items = download_data()
            new_items_ids = update_data(action_items)
        items = [Output_arr[key] for key in Output_arr]
        output = {}
        for item in items:
            if item.e_user in output:
                output[item.e_user] = output[item.e_user] + item.e_score
            else:
                output[item.e_user] = item.e_score

        output_sorted = list(output.items())
        output_sorted.sort(key=lambda i: i[1], reverse=True)
        reply_str=''
        for i in output_sorted:
            reply_str = reply_str + i[0] + '-' + i[1]
        if not reply_str=='':
            print_long(update, context, reply_str)
    except Exception as e:
        err_msg = "неизвестная ошибка update: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))

def tg_lvl_stat(update, context):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid
    try:
        input_int = int(update.message.text[len(TgCommands.LvlStat)+2:])
        if Auto_update:
            action_items = download_data()
            new_items_ids = update_data(action_items)
        items = [Output_arr[key] for key in Output_arr if Output_arr[key].e_lvl==input_int]
        output = {}
        for item in items:
            if item.e_team in output:
                output[item.e_team] = output[item.e_team] + item.e_score
            else:
                output[item.e_team] = item.e_score
        output_sorted = list(output.items())
        output_sorted.sort(key=lambda i: i[1], reverse=True)
        reply_str=''
        for i in output_sorted:
            reply_str = reply_str + i[0] + '-' + i[1]
        if not reply_str=='':
            print_long(update, context, reply_str)
    except Exception as e:
        err_msg = "неизвестная ошибка update: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))

def tg_go(update, context):
    global Is_monitoring_active
    try:
        Is_monitoring_active = True
        action_items = download_data()
        new_items_ids = update_data(action_items)
        x = Thread(target=tg_run, args=(update,context,))
        x.start()
        update.message.reply_text('started')
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))

def tg_stop(update, context):
    global Is_monitoring_active
    try:
        Is_monitoring_active = False
        update.message.reply_text('stopped')
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
        
def tg_game(update, context):
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

#-------------------------------------tghelp-------------------------------------------------------

def print_long(update, context, input_text):
    if len(input_text) == 0:
        update.message.reply_text('-')
        return
    if len(input_text) > 4096:
        for x in range(0, len(input_text), 4096):
            update.message.reply_text(input_text[x:x+4096])
    else:
        update.message.reply_text(input_text)
        
#--------------------------------------main--------------------------------------------------------

def main():
    #updater = Updater("408100374:AAEhMleUbdVH_G1xmKeCAy8MlNfyBwB9AOo", use_context=True)
    updater = Updater("979411435:AAEHIVLx8L8CxmjIHtitaH4L1GeV_OCRJ7M", use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler(TgCommands.Go, tg_go))
    dp.add_handler(CommandHandler(TgCommands.Stop, tg_stop))
    dp.add_handler(CommandHandler(TgCommands.Game, tg_game))
    dp.add_handler(CommandHandler(TgCommands.LvlStat, tg_lvl_stat))
    dp.add_handler(CommandHandler(TgCommands.Points, tg_points_stat))
    #dp.add_handler(MessageHandler(Filters.text, tg_p_default))
    
    dp.add_error_handler(tg_error)

    updater.start_polling()
    
    updater.idle()


if __name__ == '__main__':
    main()
