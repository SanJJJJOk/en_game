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

class ETypes:
    Undefined = 'undefined'
    Egg = 'egg'
    Task = 'task'
    Hint = 'hint'
    MiniTask = 'minitask'
    MiniHint = 'minihint'
    War = 'war'

class TgCommands:
    Secret = 'secret'
    Go = 'go'
    Stop = 'stop'
    Game = 'game'
    TeamStat = 'tstat'
    UserStat = 'ustat'
    TeamEggs = 'teggs'
    UserEggs = 'ueggs'
    Backup = 'backup'
    ByTeamStat = 'btstat'
    ByTeamEggs = 'bteggs'

class Emjs:
    Bonus = '\u2705'
    Penalty = '\u274c'
    Point = '\ud83d\udccd'
    Egg = '\ud83e\udd5a'
    Task = '\ud83d\udca1'
    Hint = '\u2757\ufe0f'
    MiniTask = '\ud83d\udd6f'
    MiniHint = '\u2755'
    # War = '\ud83d\udca5'
    First = '\ud83e\udd47'
    Second = '\ud83e\udd48'
    Third = '\ud83e\udd49'
    Other = '\ud83d\udd35'

class ActionItemsSet:
    def __init__(self):
        self.score_sum = 0
        self.items = []

    def add(self, item):
        self.items.append(item)
        self.score_sum = self.score_sum + item.e_score

class ActionInfo:
    def __init__(self):
        self.task_count = 0
        self.hint_count = 0
        self.minitask_count = 0
        self.minihint_count = 0
        self.egg_count = 0
        self.war_count = 0

class ActionItem:
    def __init__(self, e_dtime, e_team, e_lvl, e_bonus, e_score, e_itemid, e_user, e_type, e_isgood):
        self.e_dtime = e_dtime
        self.e_team = e_team
        self.e_lvl = e_lvl
        self.e_bonus = e_bonus
        self.e_score = e_score
        self.e_itemid = e_itemid
        self.e_user = e_user
        self.e_type = e_type
        self.e_isgood = e_isgood

def tg_error(update, context):
    err_msg = "Callback: {0}".format(str(context.error))
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    
Is_monitoring_active = False
Auto_update = True
Output_arr = {}
Domain = '72'
Gameid = '70696'
ChatHolder = []

#---------------------------------------info---------------------------------------------------------

def check_other_commands(update, context):
    user_info = "user:" + str(update.message.chat.id) + "\n" + str(update.message.date) + "\n"+str(update.message.from_user.id) + "\n"+str(update.message.from_user.first_name) + "\n"+str(update.message.from_user.last_name) + "\n"+str(update.message.from_user.username)
    context.bot.send_message('228485598', user_info + '\n\n' + update.message.text)

def bot_authorize(update, context):
    global ChatHolder
    if not update.message.chat.id in ChatHolder:
        ChatHolder.append(update.message.chat.id)
        user_info = "authorized user:" + str(update.message.chat.id) + "\n" + str(update.message.date) + "\n"+str(update.message.from_user.id) + "\n"+str(update.message.from_user.first_name) + "\n"+str(update.message.from_user.last_name) + "\n"+str(update.message.from_user.username)
        context.bot.send_message('228485598', user_info)
        return
        #raise Exception('you are not authorized, please call /start')

#---------------------------------------base---------------------------------------------------------

def get_unique(arr) -> []:
    return list(dict.fromkeys(arr))

def sec_to_str(val):
    neg_prefix = ''
    if val < 0:
        val = -val
        neg_prefix = '-'
    minval = str(round(val // 60))
    secval = str(round(val % 60))
    if len(secval)==1:
        secval = '0' + secval
    return neg_prefix + minval + ':' + secval

def get_action_info(items):
    info = ActionInfo()
    for item in items:
        if item.e_type==ETypes.Task:
            info.task_count = info.task_count + 1
            continue
        if item.e_type==ETypes.Hint:
            info.hint_count = info.hint_count + 1
            continue
        if item.e_type==ETypes.Egg:
            info.egg_count = info.egg_count + 1
            continue
        if item.e_type==ETypes.MiniTask:
            info.minitask_count = info.minitask_count + 1
            continue
        if item.e_type==ETypes.MiniHint:
            info.minihint_count = info.minihint_count + 1
        #     continue
        # if item.e_type==ETypes.War:
        #     info.war_count = info.war_count + 1
    return info

def info_to_str(info, is_zero_shown):
    result = ''
    if is_zero_shown or info.task_count>0:
        result = result + Emjs.Task + str(info.task_count) + ' '
    if is_zero_shown or info.minitask_count>0:
        result = result + Emjs.MiniTask + str(info.minitask_count) + ' '
    if is_zero_shown or info.hint_count>0:
        result = result + Emjs.Hint + str(info.hint_count) + ' '
    if is_zero_shown or info.minihint_count>0:
        result = result + Emjs.MiniHint + str(info.minihint_count) + ' '
    if is_zero_shown or info.egg_count>0:
        result = result + Emjs.Egg + str(info.egg_count) + ' '
    # if is_zero_shown or info.war_count>0:
    #     result = result + Emjs.War + str(info.war_count) + ' '
    return result.strip()

def get_score_emjs_data(score_values):
    output = {}
    unique_values = get_unique(score_values)
    if not 0 in unique_values:
        unique_values.append(0)
    unique_values.sort(reverse=True)

    if len(unique_values)<4:
        for val in unique_values:
            output[val] = '-'
        return output

    output[unique_values[0]] = Emjs.First
    output[unique_values[1]] = Emjs.Second
    output[unique_values[2]] = Emjs.Third
    other_unique_values = unique_values[3:]
    for val in other_unique_values:
        output[val] = Emjs.Other

    return output

def get_action_type(score):
    if score==1:
        return ETypes.Egg
    if score==2:
        return ETypes.MiniTask
    if score==60:
        return ETypes.Task
    if score==-30:
        return ETypes.Hint
    if score==-1:
        return ETypes.MiniHint
    return ETypes.Undefined

#---------------------------------------upd---------------------------------------------------------

def update_data():
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid
    fp = request.urlopen("http://"+Domain+".en.cx/GameBonusPenaltyTime.aspx?gid="+Gameid)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    soup = BeautifulSoup(mystr, 'html.parser')

    bp_items = soup.find_all('tr', {'id': re.compile("^PlayersRepeater")})

    action_items = []
    for i in bp_items:
        bp_tag = i.find('a', {'id': re.compile("lnkBonus")})
        if bp_tag.get_text()=='':
            bp_tag = i.find('a', {'id': re.compile("lnkPenalty")})

        bp_link = bp_tag['href']
        stind = bp_link.index('correct=') + 8
        enind = bp_link.index('&gid=')
        e_itemid = bp_link[stind:enind]

        if e_itemid in Output_arr:
            continue

        e_dtime = i.find('td').get_text()
        e_team = i.find('a', {'id': re.compile("lnkPlayerInfo")}).get_text()
        e_lvl = int(i.find('td', {'id': re.compile("tdLevelColumnValue")}).get_text())

        bp_tag_txt = bp_tag.get_text()
        e_bonus = bp_tag_txt.startswith('б')
            
        input_bp = bp_tag_txt.strip().split(' ')
        input_bp_correct = [x for x in input_bp if not(x is None or x == '')]
        scoreval = int(input_bp_correct[1])
        if input_bp_correct[2].startswith('м'):
            scoreval = scoreval * 60
        e_score = scoreval
        if not e_bonus:
            e_score = -e_score

        e_type = get_action_type(e_score)

        fp2 = request.urlopen("http://72.en.cx/" + bp_link)
        mybytes2 = fp2.read()
        mystr2 = mybytes2.decode("utf8")
        fp2.close()
        soup2 = BeautifulSoup(mystr2, 'html.parser')

        user_tag = soup2.find('a', {'id': re.compile("lnkCorrectInfoUserInfo")})
        e_user = None
        if not user_tag is None:
            e_user = user_tag.get_text()

        action_item = ActionItem(e_dtime, e_team, e_lvl, e_bonus, e_score, e_itemid, e_user, e_type, True)
        action_items.append(action_item)
        Output_arr[e_itemid] = action_item

    return action_items

#-------------------------------------tg-run-------------------------------------------------------

def tg_run(update, context):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid
    try:
        errors_count = 0
        while Is_monitoring_active:
            try:
                new_items = update_data()
                reply_strs=[]
                for i in new_items:
                    reply_str = ''
                    if i.e_bonus and i.e_score==1:
                        reply_str = reply_str + Emjs.Point
                    else:
                        if i.e_bonus:
                            reply_str = reply_str + Emjs.Bonus
                        else:
                            reply_str = reply_str + Emjs.Penalty
                        reply_str = reply_str + '(' + str(i.e_score) + 's)'
                    reply_str = reply_str + ' ' + i.e_team + ' at ' + str(i.e_dtime) + ' by ' + i.e_user
                    team_lvl_items = [Output_arr[ii] for ii in Output_arr if Output_arr[ii].e_team==i.e_team and Output_arr[ii].e_lvl==i.e_lvl]
                    team_items = [Output_arr[ii] for ii in Output_arr if Output_arr[ii].e_team==i.e_team]
                    info_lvl = get_action_info(team_lvl_items)
                    info = get_action_info(team_items)
                    reply_str = reply_str + '\n' + str(i.e_lvl) + 'lv:' + info_to_str(info_lvl, True) + '\nall:' + info_to_str(info, True)
                    reply_strs.append(reply_str)
                if len(reply_strs)>0:
                    print_long(update, context, '\n\n'.join(reply_strs))
            except Exception as e:
                err_msg = "неизвестная ошибка update: {0}".format(str(e))
                update.message.reply_text(err_msg)
                context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
                errors_count = errors_count + 1
            if errors_count>100:
                break
            time.sleep(60)
        update.message.reply_text("i'm off")
    except Exception as e:
        err_msg = "неизвестная ошибка update: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
        
#-------------------------------------tgstat---------------------------------------------------------

def tg_base_in_teams_stat_eggs(update, context, command, is_only_eggs):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid, ChatHolder
    try:
        bot_authorize(update, context)
        check_other_commands(update, context)
        spec_lvl = 0
        if len(update.message.text)>len(command)+2:
            spec_lvl = int(update.message.text[len(command)+2:])
        if Auto_update:
            new_items = update_data()
        output = {}
        for key in Output_arr:
            item = Output_arr[key]
            if not item.e_isgood:
                continue
            if spec_lvl!=0 and item.e_lvl!=spec_lvl:
                continue
            if is_only_eggs and item.e_type!=ETypes.Egg:
                continue
            item_key = item.e_team
            if not item_key in output:
                output[item_key] = ActionItemsSet()
            output[item_key].add(item)
        output_sorted = list(output.items())
        output_sorted.sort(key=lambda i: i[1].score_sum, reverse=True)

        is_zero_shown = not is_only_eggs
        for team_item in output_sorted:
            o2_output = {}
            for o2_item in team_item[1].items:
                item_key = o2_item.e_user
                if not item_key in o2_output:
                    o2_output[item_key] = ActionItemsSet()
                o2_output[item_key].add(o2_item)
            o2_output_sorted = list(o2_output.items())
            o2_output_sorted.sort(key=lambda i: i[1].score_sum, reverse=True)

            score_emjs_data = get_score_emjs_data([i[1].score_sum for i in o2_output_sorted])

            reply_str = team_item[0] + ':\n'
            for i in o2_output_sorted:
                info = get_action_info(i[1].items)
                reply_str = reply_str + score_emjs_data[i[1].score_sum] + '-' + i[0] + ' (' + sec_to_str(i[1].score_sum) + '): ' + info_to_str(info, is_zero_shown) + '\n'
            print_long(update, context, reply_str)
    except Exception as e:
        err_msg = "неизвестная ошибка update: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))

def tg_base_stat_eggs(update, context, command, is_by_team, is_only_eggs):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid, ChatHolder
    try:
        bot_authorize(update, context)
        check_other_commands(update, context)
        spec_lvl = 0
        if len(update.message.text)>len(command)+2:
            spec_lvl = int(update.message.text[len(command)+2:])
        if Auto_update:
            new_items = update_data()
        output = {}
        for key in Output_arr:
            item = Output_arr[key]
            if not item.e_isgood:
                continue
            if spec_lvl!=0 and item.e_lvl!=spec_lvl:
                continue
            if is_only_eggs and item.e_type!=ETypes.Egg:
                continue
            if not is_by_team and item.e_type==ETypes.War:
                continue
            item_key = item.e_team if is_by_team else item.e_user
            if not item_key in output:
                output[item_key] = ActionItemsSet()
            output[item_key].add(item)
        output_sorted = list(output.items())
        output_sorted.sort(key=lambda i: i[1].score_sum, reverse=True)

        score_emjs_data = get_score_emjs_data([i[1].score_sum for i in output_sorted])

        reply_str = ''
        is_zero_shown = not is_only_eggs
        for i in output_sorted:
            info = get_action_info(i[1].items)
            reply_str = reply_str + score_emjs_data[i[1].score_sum] + '-' + i[0] + ' (' + sec_to_str(i[1].score_sum) + '): ' + info_to_str(info, is_zero_shown) + '\n'
        if not reply_str=='':
            print_long(update, context, reply_str)
    except Exception as e:
        err_msg = "неизвестная ошибка update: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))

def tg_user_eggs(update, context):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid, ChatHolder
    tg_base_stat_eggs(update, context, TgCommands.UserEggs, False, True)
        
def tg_team_eggs(update, context):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid, ChatHolder
    tg_base_stat_eggs(update, context, TgCommands.TeamEggs, True, True)

def tg_team_stat(update, context):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid, ChatHolder
    tg_base_stat_eggs(update, context, TgCommands.TeamStat, True, False)

def tg_user_stat(update, context):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid, ChatHolder
    tg_base_stat_eggs(update, context, TgCommands.UserStat, False, False)
    
def tg_team_stat_intt(update, context):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid, ChatHolder
    tg_base_in_teams_stat_eggs(update, context, TgCommands.ByTeamStat, False)

def tg_team_eggs_intt(update, context):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid, ChatHolder
    tg_base_in_teams_stat_eggs(update, context, TgCommands.ByTeamEggs, True)

#------------------------------------tg: go/stop------------------------------------------------------

def tg_go(update, context):
    global Is_monitoring_active, ChatHolder
    try:
        bot_authorize(update, context)
        check_other_commands(update, context)
        if str(update.message.from_user.id)!='228485598':
            update.message.reply_text('ты кто?')
            return
        Is_monitoring_active = True
        x = Thread(target=tg_run, args=(update,context,))
        x.start()
        update.message.reply_text('started')
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))

def tg_stop(update, context):
    global Is_monitoring_active, ChatHolder
    try:
        bot_authorize(update, context)
        check_other_commands(update, context)
        if str(update.message.from_user.id)!='228485598':
            update.message.reply_text('ты кто?')
            return
        Is_monitoring_active = False
        update.message.reply_text('stopped')
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
        
#---------------------------------import/export----------------------------------------------------

def restore(input_data):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid
    Output_arr = {}
    input_items = input_data['items']
    for i in input_items:
        e_dtime = i['e_dtime']
        e_team = i['e_team']
        e_lvl = i['e_lvl']
        e_bonus = i['e_bonus']
        e_score = i['e_score']
        e_itemid = i['e_itemid']
        e_user = i['e_user']
        e_type = i['e_type']
        e_isgood = i['e_isgood']
        item = ActionItem(e_dtime, e_team, e_lvl, e_bonus, e_score, e_itemid, e_user, e_type, e_isgood)
        Output_arr[e_itemid] = item
    return None
    
def tg_backup(update, context):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid, ChatHolder
    try:
        bot_authorize(update, context)
        check_other_commands(update, context)
        output_dict = {
            'items': []
            }
        items = output_dict['items']
        for key in Output_arr:
            i = Output_arr[key]
            items.append({
                'e_dtime': i.e_dtime,
                'e_team': i.e_team,
                'e_lvl': i.e_lvl,
                'e_bonus': i.e_bonus,
                'e_score': i.e_score,
                'e_itemid': i.e_itemid,
                'e_user': i.e_user,
                'e_type': i.e_type,
                'e_isgood': i.e_isgood,
                })
        m_str = json.dumps(output_dict, ensure_ascii=False, indent=2)
        file = open('123.json', 'w', encoding='utf-8')
        file.truncate(0)
        file.write(m_str)
        file.close()

        file = open('123.json','rb')
        context.bot.send_document('228485598', file)
        file.close()
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
    
def tg_document(update, context):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid, ChatHolder
    try:
        bot_authorize(update, context)
        check_other_commands(update, context)
        if str(update.message.chat.id)!='228485598':
            update.message.reply_text('ты кто?')
            return
        file = update.message.document.get_file()
        input_filedata = file.download_as_bytearray()
        json_data = json.loads(input_filedata)
        output_msg = restore(json_data)
        if output_msg is None:
            update.message.reply_text('збс')
        else:
            update.message.reply_text(output_msg)
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
        
def tg_secret(update, context):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid, ChatHolder
    try:
        bot_authorize(update, context)
        check_other_commands(update, context)
        update.message.reply_text('sr23уй')
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
        
def tg_default_txt(update, context):
    global Is_monitoring_active, Auto_update, Output_arr, Domain, Gameid, ChatHolder
    try:
        bot_authorize(update, context)
        check_other_commands(update, context)
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))

#--------------------------------------main--------------------------------------------------------

def main():
    file = open('data.json','r',encoding='utf-8')
    input_filedata = file.read()
    file.close()
    bytesdata = input_filedata.encode('utf-8')
    json_data = json.loads(bytesdata)
    output_msg = restore(json_data)

    #updater = Updater("408100374:AAEhMleUbdVH_G1xmKeCAy8MlNfyBwB9AOo", use_context=True)
    updater = Updater("979411435:AAEHIVLx8L8CxmjIHtitaH4L1GeV_OCRJ7M", use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler(TgCommands.Secret, tg_secret))
    dp.add_handler(CommandHandler(TgCommands.Go, tg_go))
    dp.add_handler(CommandHandler(TgCommands.Stop, tg_stop))
    dp.add_handler(CommandHandler(TgCommands.TeamStat, tg_team_stat))
    dp.add_handler(CommandHandler(TgCommands.UserStat, tg_user_stat))
    dp.add_handler(CommandHandler(TgCommands.TeamEggs, tg_team_eggs))
    dp.add_handler(CommandHandler(TgCommands.UserEggs, tg_user_eggs))
    dp.add_handler(CommandHandler(TgCommands.Backup, tg_backup))
    dp.add_handler(CommandHandler(TgCommands.ByTeamStat, tg_team_stat_intt))
    dp.add_handler(CommandHandler(TgCommands.ByTeamEggs, tg_team_eggs_intt))
    dp.add_handler(MessageHandler(Filters.document, tg_document))
    dp.add_handler(MessageHandler(Filters.text, tg_default_txt))
    
    dp.add_error_handler(tg_error)

    updater.start_polling()
    
    updater.idle()


if __name__ == '__main__':
    main()
