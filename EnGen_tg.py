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
    context.bot.send_message('228485598', err_msg)
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    
Holder = GlobalInfo()

class TgCommands:
    Backup = 'backup'
    Login = 'login'
    Logout = 'logout'
    Info = 'info'
    Stat = 'stat'
    Curse = 'curse'
    Shield = 'shield'
    Chicken = 'chicken'
    Refresh = 'refresh'
    Money = 'money'
    Hand = 'hand'
    Msg = 'msg'
    Msgteam = 'msgteam'
    Log = 'savelog'
    Autobackup = 'autobackup'

#admin commands - common
    
def tg_msg(update, context):
    try:
        if str(update.message.chat.id)!='228485598':
            update.message.reply_text('атата!')
            return
        if len(update.message.text) < len(TgCommands.Msg)+3:
            update.message.reply_text('empty')
            return
        msg_text = Emojies.Info + update.message.text[len(TgCommands.Msg)+2:]
        for player_id in GlobalInfo.registered_players:
            context.bot.send_message(player_id, msg_text)
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

def tg_msgteam(update, context):
    try:
        input = tg_admin_default_command(update, context, TgCommands.Msgteam, 2)
        if len(input)==0:
            return
        munch_id = int(input[0])
        munchkin = GlobalInfo.c_munchkins_by_ids[munch_id]
        tg_send_to_team(update, context, munchkin, Emojies.Info + input[1])
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

#admin commands - persistence and logging

def tg_document(update, context):
    try:
        if str(update.message.chat.id)!='228485598':
            update.message.reply_text('атата!')
            return
        file = update.message.document.get_file()
        input_filedata = file.download_as_bytearray()
        json_data = json.loads(input_filedata)
        output_msg = GlobalInfo.restore(json_data)
        if output_msg is None:
            update.message.reply_text('збс')
        else:
            update.message.reply_text(output_msg)
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

def tg_backup(update, context):
    try:
        if str(update.message.chat.id)!='228485598':
            update.message.reply_text('атата!')
            return
        tg_backup_base(context, '228485598')
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)
        
def tg_log(update, context):
    try:
        if str(update.message.chat.id)!='228485598':
            update.message.reply_text('атата!')
            return
        log_str = json.dumps(GlobalInfo.logs, ensure_ascii=False, indent=2)
        file = open('1234.json', 'w', encoding='utf-8')
        file.truncate(0)
        file.write(log_str)
        file.close()
        file_to_send = open('1234.json','rb')
        context.bot.send_document('228485598', file_to_send)
        file.close()
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

def tg_autobackup(update, context):
    try:
        if str(update.message.chat.id)!='228485598':
            update.message.reply_text('атата!')
            return
        GlobalInfo.autobackup_enabled = not GlobalInfo.autobackup_enabled
        update.message.reply_text('autobackup is ' + str(GlobalInfo.autobackup_enabled))
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

def tg_backup_base(context, id):
        GlobalInfo.backup()
        file = open('123.json','rb')
        context.bot.send_document(id, file)
        file.close()
    
#admin commands - manual control

def tg_send_to_team(update, context, munchkin, msg):
    for player_id in GlobalInfo.registered_players:
        if GlobalInfo.registered_players[player_id].id == munchkin.id:
            context.bot.send_message(player_id, msg)

def tg_admin_default_command(update, context, command, count):
    if str(update.message.chat.id)!='228485598':
        update.message.reply_text('атата!')
        return []
    if len(update.message.text) < len(command)+3:
        update.message.reply_text('empty')
        return []
    input_text = update.message.text[len(command)+2:]
    input = input_text.split(' ')
    if len(input)!=count:
        update.message.reply_text('args')
        return []
    return input

def tg_refresh(update, context):
    try:
        input = tg_admin_default_command(update, context, TgCommands.Refresh, 2)
        if len(input)==0:
            return
        munch_id = int(input[0])
        munchkin = GlobalInfo.c_munchkins_by_ids[munch_id]
        count = int(input[1])
        if count < len(munchkin.applied_curses):
            munchkin.applied_curses = munchkin.applied_curses[:-count]
            update.message.reply_text('+++' + str(count) + ' refreshed')
        else:
            munchkin.applied_curses = []
            update.message.reply_text('+++all refreshed')
        if GlobalInfo.autobackup_enabled:
            tg_backup_base(context, '661294614')
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

def tg_chicken(update, context):
    try:
        input = tg_admin_default_command(update, context, TgCommands.Chicken, 2)
        if len(input)==0:
            return
        munch_id = int(input[0])
        munchkin = GlobalInfo.c_munchkins_by_ids[munch_id]
        dt_now = datetime.now()
        if munchkin.shield_datetime > dt_now:
            update.message.reply_text('---shield')
            return

        value = int(input[1])
        munchkin.chicken_datetime = dt_now + timedelta(0, value)
        update.message.reply_text('+++chicken applied')
        tg_send_to_team(update, context, munchkin, Emojies.Important + 'вас превратили в курицу')
        if GlobalInfo.autobackup_enabled:
            tg_backup_base(context, '661294614')
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

def tg_money(update, context):
    try:
        input = tg_admin_default_command(update, context, TgCommands.Money, 2)
        if len(input)==0:
            return
        munch_id = int(input[0])
        munchkin = GlobalInfo.c_munchkins_by_ids[munch_id]
        value = int(input[1])
        str_money = str(munchkin.current_money)
        if value > munchkin.current_money:
            update.message.reply_text('---money ' + munchkin.name + ' = ' + str_money)
            return
        munchkin.current_money = munchkin.current_money - value
        update.message.reply_text('+++money ' + munchkin.name + ': ' + str_money + '-' + str(value) + '=' + str(munchkin.current_money))
        if GlobalInfo.autobackup_enabled:
            tg_backup_base(context, '661294614')
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

def tg_hand(update, context):
    try:
        input = tg_admin_default_command(update, context, TgCommands.Hand, 1)
        if len(input)==0:
            return
        munch_id = int(input[0])
        munchkin = GlobalInfo.c_munchkins_by_ids[munch_id]
        munchkin.use_three_hands = True
        update.message.reply_text('+++three hands applied')
        if GlobalInfo.autobackup_enabled:
            tg_backup_base(context, '661294614')
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

def tg_shield(update, context):
    try:
        input = tg_admin_default_command(update, context, TgCommands.Shield, 2)
        if len(input)==0:
            return
        munch_id = int(input[0])
        munchkin = GlobalInfo.c_munchkins_by_ids[munch_id]
        dt_now = datetime.now()
        value = int(input[1])
        munchkin.shield_datetime = dt_now + timedelta(0, value)
        update.message.reply_text('+++shield applied')
        if GlobalInfo.autobackup_enabled:
            tg_backup_base(context, '661294614')
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

def tg_curse(update, context):
    try:
        input = tg_admin_default_command(update, context, TgCommands.Curse, 2)
        if len(input)==0:
            return
        munch_id = int(input[0])
        munchkin = GlobalInfo.c_munchkins_by_ids[munch_id]
        dt_now = datetime.now()
        if munchkin.shield_datetime > dt_now:
            update.message.reply_text('---shield')
            return

        source_munch_id = int(input[1])
        source_munchkin = GlobalInfo.c_munchkins_by_ids[source_munch_id]
        target_msg = Emojies.Important + 'На вас кинул проклятье манчкин ' + source_munchkin.name

        curse_time = dt_now + timedelta(0, 1800)
        munchkin.applied_curses.append(curse_time)

        tg_send_to_team(update, context, munchkin, target_msg)
        update.message.reply_text('+++curse applied')
        if GlobalInfo.autobackup_enabled:
            tg_backup_base(context, '661294614')
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

#user commands

def tg_stat(update, context):
    try:
        if not update.message.chat.id in GlobalInfo.registered_players:
            update.message.reply_text('вы не зарегистрированы')
            return
        dt_now = datetime.now()
        munchkin = GlobalInfo.registered_players[update.message.chat.id]
        if munchkin.chicken_datetime > dt_now:
            dt_ck_diff = (munchkin.chicken_datetime - dt_now).total_seconds()
            update.message.reply_text(Emojies.Chicken + 'вас превратили в курицу, просмотр статистики недоступен\n' + Emojies.Result2 + GlobalInfo.sec_to_str(dt_ck_diff))
            return
        if munchkin.stat_datetime > dt_now:
            dt_st_diff = (munchkin.stat_datetime - dt_now).total_seconds()
            update.message.reply_text(Emojies.Result2 + 'просмотр статистики будет доступен через \n' + GlobalInfo.sec_to_str(dt_st_diff))
            return
        munchkin.stat_datetime = dt_now + timedelta(0, 5)
        stat_str = 'Общая статистика:'
        for munch_id in GlobalInfo.c_munchkins_by_ids:
            other_munchkin = GlobalInfo.c_munchkins_by_ids[munch_id]
            stat_str = stat_str + '\n' + other_munchkin.name + ' ' + str(other_munchkin.current_lvl) + ' ур. ' + RaceClassType.CRNames[other_munchkin.current_race] + ', ' + RaceClassType.CRNames[other_munchkin.current_class]
            total_power = other_munchkin.get_total_power()
            stat_str = stat_str + ' ' + Emojies.Power + '=' + str(total_power)
            if other_munchkin.chicken_datetime > dt_now:
                stat_str = stat_str + ' | ' + Emojies.Chicken
        update.message.reply_text(stat_str)
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

def tg_info(update, context):
    try:
        if not update.message.chat.id in GlobalInfo.registered_players:
            update.message.reply_text('вы не зарегистрированы')
            return
        dt_now = datetime.now()
        munchkin = GlobalInfo.registered_players[update.message.chat.id]
        if munchkin.chicken_datetime > dt_now:
            dt_ck_diff = (munchkin.chicken_datetime - dt_now).total_seconds()
            update.message.reply_text(Emojies.Chicken + 'вас превратили в курицу, просмотр инфо недоступен\n' + Emojies.Result2 + GlobalInfo.sec_to_str(dt_ck_diff))
            return
        output_stat = munchkin.name + ', ***' + str(munchkin.current_lvl) + '*** ур., ' + str(munchkin.current_money) + Emojies.Money + '\n'
        output_stat = output_stat + '---------------------------\n'
        output_stat = output_stat + RaceClassType.CREmojies[munchkin.current_race] + ': ' + RaceClassType.CRNames[munchkin.current_race]
        if munchkin.race_change_datetime > dt_now:
            dt_r_diff = (munchkin.race_change_datetime - dt_now).total_seconds()
            output_stat = output_stat + ' ' + Emojies.Result2 + GlobalInfo.sec_to_str(dt_r_diff)
        output_stat = output_stat + '\n' + RaceClassType.CREmojies[munchkin.current_class] + ': ' + RaceClassType.CRNames[munchkin.current_class]
        if munchkin.class_change_datetime > dt_now:
            dt_c_diff = (munchkin.class_change_datetime - dt_now).total_seconds()
            output_stat = output_stat + ' ' + Emojies.Result2 + GlobalInfo.sec_to_str(dt_c_diff)
        output_stat = output_stat + '\n---------------------------\n'
        for tr in munchkin.used_trs:
            output_stat = output_stat + tr.get_small_info() + '\n' 
        output_stat = output_stat + '---------------------------\n'
        if munchkin.shield_datetime > dt_now:
            dt_s_diff = (munchkin.shield_datetime - dt_now).total_seconds()
            output_stat = output_stat + 'Защита от проклятий: ' + Emojies.Result2 + GlobalInfo.sec_to_str(dt_s_diff) + '\n'
        if munchkin.one_shot_bonus > 0:
            output_stat = output_stat + 'Бонус в следующем бою: +' + str(munchkin.one_shot_bonus) + ' силы\n'
        if munchkin.one_shot_bonus < 0:
            output_stat = output_stat + 'Штраф в следующем бою: -' + str(-munchkin.one_shot_bonus) + ' силы\n'
        for curse in munchkin.applied_curses:
            if curse > dt_now:
                dt_curse_diff = (curse - dt_now).total_seconds()
                output_stat = output_stat + '-1: ' + Emojies.Result2 + GlobalInfo.sec_to_str(dt_curse_diff) + '\n'
        output_stat = output_stat + '---------------------------\n'
        total_power = munchkin.get_total_power()
        output_stat = output_stat + Emojies.Power + '=' + str(total_power)
        if munchkin.monster_fight_datetime > dt_now:
            output_stat = output_stat + '\n---------------------------\n'
            dt_m_diff = (munchkin.monster_fight_datetime - dt_now).total_seconds()
            output_stat = output_stat + 'Следующий бой доступен через: ' + Emojies.Result2 + GlobalInfo.sec_to_str(dt_m_diff)

        update.message.reply_text(output_stat)
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

def tg_login(update, context):
    try:
        if len(update.message.text)<len(TgCommands.Login)+3:
            update.message.reply_text('пустое сообщение')
            return
        login_id = update.message.text[len(TgCommands.Login)+2:]
        if not login_id in GlobalInfo.munchkins_logins:
            update.message.reply_text('неверный логин')
            return
        munchkin = GlobalInfo.munchkins_logins[login_id]
        GlobalInfo.registered_players[update.message.chat.id] = munchkin
        update.message.reply_text('регистрация успешна: ' + munchkin.name)
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

#def tg_logout(update, context):
#    try:
#        chat_id = update.message.chat.id
#        if chat_id in GlobalInfo.registered_players:
#            del GlobalInfo.registered_players[chat_id]
#            update.message.reply_text('успешно')
#            return
#        update.message.reply_text('вы не относитесь ни к одной команде')
#    except Exception as e:
#        err_msg = "неизвестная ошибка: {0}".format(str(e))
#        update.message.reply_text(err_msg)
#        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

def tg_default(update, context):
    try:
        if not update.message.chat.id in GlobalInfo.registered_players:
            update.message.reply_text('вы не зарегистрированы')
            return
        munchkin = GlobalInfo.registered_players[update.message.chat.id]
        input_text = update.message.text.strip().lower()
        if len(input_text)==0:
            update.message.reply_text('пустое сообщение')
            return

        #single code
        if input_text in GlobalInfo.c_singlecode_handlers:
            handler = GlobalInfo.c_singlecode_handlers[input_text]
            result = handler(munchkin, input_text)
            tg_check_lv_cheaters(update, context, munchkin, input_text)
            update.message.reply_text(Result.ResultEmojies[result.code] + result.message)
            if result.code==0:
                GlobalInfo.add_log_row(munchkin.name, update.message.chat.id, input_text, 1)
                if GlobalInfo.autobackup_enabled:
                    tg_backup_base(context, '661294614')
            return

        #divine intervention
        if input_text == GlobalInfo.divine_intervention_code:
            if GlobalInfo.is_divine_intervention_passed:
                update.message.reply_text(Result.ResultEmojies[1] + 'Божественное вмешательство уже было использовано')
            else:
                GlobalInfo.is_divine_intervention_passed = True
                dt_now = datetime.now()
                output_str = Emojies.Important + 'Божественное вмешательство применил манчкин ' + munchkin.name + '\nУровень получили: '
                for munch_id in GlobalInfo.c_munchkins_by_ids:
                    tmp_munch = GlobalInfo.c_munchkins_by_ids[munch_id]
                    if tmp_munch.current_class==RaceClassType.Cleric:
                        tmp_munch.current_lvl = tmp_munch.current_lvl + 1
                        output_str = output_str + tmp_munch.name + ', '
                for player_id in GlobalInfo.registered_players:
                    context.bot.send_message(player_id, output_str)
                context.bot.send_message('228485598', output_str + dt_now.strftime("%m/%d/%Y, %H:%M:%S"))
                if GlobalInfo.autobackup_enabled:
                    tg_backup_base(context, '661294614')
            return

        #parse
        parsed_codes = GlobalInfo.split_and_remove_empty(input_text)
        if len(parsed_codes)==0:
            update.message.reply_text('ошибка: пустое сообщение')
            return

        #to team
        if len(parsed_codes)==2:
            if parsed_codes[0] in GlobalInfo.c_toteam_handlers:
                toteam_handler = GlobalInfo.c_toteam_handlers[parsed_codes[0]]
                result_tt = toteam_handler(munchkin, parsed_codes[0], parsed_codes[1])
                update.message.reply_text(Result.ResultEmojies[result_tt.code] + result_tt.message)
                if result_tt.code==0:
                    GlobalInfo.add_log_row(munchkin.name, update.message.chat.id, input_text, 2)
                    tg_send_to_team(update, context, result_tt.target_munchkin, Emojies.Important + result_tt.target_message)
                    if GlobalInfo.autobackup_enabled:
                        tg_backup_base(context, '661294614')
                return

        #treasures
        tg_check_tr_cheaters(update, context, munchkin, parsed_codes)
        result_treasure = GlobalInfo.do_beautiful_with_treasures(munchkin, parsed_codes)
        update.message.reply_text(Result.ResultEmojies[result_treasure.code] + result_treasure.message)
        if result_treasure.code==0:
            GlobalInfo.add_log_row(munchkin.name, update.message.chat.id, input_text, 3)
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

def tg_check_lv_cheaters(update, context, munchkin, lvl_code):
    #return
    if lvl_code in GlobalInfo.c_level_codes:
        if not GlobalInfo.c_check_m_by_lvlc[lvl_code] in munchkin.killed_monsters:
            context.bot.send_message('228485598', Emojies.Important + Emojies.Important + 'lvl cheater found:' + munchkin.name + ',' + lvl_code)

def tg_check_tr_cheaters(update, context, munchkin, tr_codes):
    #return
    for tr_code in tr_codes:
        if tr_code in GlobalInfo.c_treasure_codes:
            if not GlobalInfo.c_check_m_by_trc[tr_code] in munchkin.killed_monsters:
                context.bot.send_message('228485598', Emojies.Important + Emojies.Important + 'treasure cheater found:' + munchkin.name + ',' + tr_code)

def main():
    GlobalInfo.initialize()
    #update = FakeUpdate()
    #context = FakeContext()
    #tg_backup(update, context)
    #update.message.text = '/login 1234'
    #update.message.chat.id = '123'
    #tg_login(update, context)
    #GlobalInfo.registered_players[update.message.chat.id].current_lvl = 3
    #update.message.text = '/login 1234'
    #update.message.chat.id = '456'
    #tg_login(update, context)
    

    #t1 = GlobalInfo.registered_players
    #t2 = GlobalInfo.munchkins_logins

    #t3 = Munchkin('name123')

    updater = Updater("408100374:AAEhMleUbdVH_G1xmKeCAy8MlNfyBwB9AOo", use_context=True)
    #updater = Updater("979411435:AAEHIVLx8L8CxmjIHtitaH4L1GeV_OCRJ7M", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler(TgCommands.Log, tg_log))
    dp.add_handler(CommandHandler(TgCommands.Autobackup, tg_autobackup))
    dp.add_handler(CommandHandler(TgCommands.Msgteam, tg_msgteam))
    dp.add_handler(CommandHandler(TgCommands.Msg, tg_msg))
    dp.add_handler(CommandHandler(TgCommands.Backup, tg_backup))

    dp.add_handler(CommandHandler(TgCommands.Money, tg_money))
    dp.add_handler(CommandHandler(TgCommands.Hand, tg_hand))
    dp.add_handler(CommandHandler(TgCommands.Refresh, tg_refresh))
    dp.add_handler(CommandHandler(TgCommands.Chicken, tg_chicken))
    dp.add_handler(CommandHandler(TgCommands.Shield, tg_shield))
    dp.add_handler(CommandHandler(TgCommands.Curse, tg_curse))

    dp.add_handler(CommandHandler(TgCommands.Info, tg_info))
    dp.add_handler(CommandHandler(TgCommands.Stat, tg_stat))
    dp.add_handler(CommandHandler(TgCommands.Login, tg_login))
    #dp.add_handler(CommandHandler(TgCommands.Logout, tg_logout))
    dp.add_handler(MessageHandler(Filters.text, tg_default))
    dp.add_handler(MessageHandler(Filters.document, tg_document))

    dp.add_error_handler(tg_error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
