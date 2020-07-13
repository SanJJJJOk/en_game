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

def tg_stat(update, context):
    try:
        if not update.message.chat.id in GlobalInfo.registered_players:
            update.message.reply_text('вы не зарегистрированы')
            return
        munchkin = GlobalInfo.registered_players[update.message.chat.id]
        output_stat = munchkin.name + ', ***' + str(munchkin.current_lvl) + '*** ур.\n'
        output_stat = output_stat + '---------------------------\n'
        output_stat = output_stat + RaceClassType.CREmojies[munchkin.current_race] + ': ' + RaceClassType.CRNames[munchkin.current_race] + '\n'
        output_stat = output_stat + RaceClassType.CREmojies[munchkin.current_class] + ': ' + RaceClassType.CRNames[munchkin.current_class] + '\n'
        output_stat = output_stat + '---------------------------\n'
        for tr in munchkin.used_trs:
            output_stat = output_stat + tr.get_small_info() + '\n' 

        total_power = munchkin.current_lvl
        for tr in munchkin.used_trs:
            total_power = total_power + tr.power
        output_stat = output_stat + '---------------------------\n'
        output_stat = output_stat + Emojies.Power + '=' + str(total_power)

        update.message.reply_text(output_stat)
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

def tg_login(update, context):
    try:
        if len(update.message.text)<8:
            update.message.reply_text('неверный логин')
            return
        login_id = update.message.text[7:]
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

def tg_logout(update, context):
    try:
        chat_id = update.message.chat.id
        if chat_id in GlobalInfo.registered_players:
            del GlobalInfo.registered_players[chat_id]
            update.message.reply_text('неверный логин')
        update.message.reply_text('вы не относитесь ни к одной команде')
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

def tg_default(update, context):
    try:
        if not update.message.chat.id in GlobalInfo.registered_players:
            update.message.reply_text('вы не зарегистрированы')
            return
        munchkin = GlobalInfo.registered_players[update.message.chat.id]
        input_text = update.message.text.strip()
        if len(input_text)==0:
            update.message.reply_text('ошибка: пустое сообщение')
            return
        if input_text in GlobalInfo.c_singlecode_handlers:
            handler = GlobalInfo.c_singlecode_handlers[input_text]
            result = handler(munchkin, input_text)
            update.message.reply_text(Result.ResultEmojies[result.result_code] + result.message)
            return
        parsed_codes = GlobalInfo.split_and_remove_empty(input_text)
        if len(parsed_codes)==0:
            update.message.reply_text('ошибка: пустое сообщение')
            return
        result_treasure = GlobalInfo.do_beautiful_with_treasures(munchkin, parsed_codes)
        update.message.reply_text(Result.ResultEmojies[result_treasure.result_code] + result_treasure.message)
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + update.message.chat.id)

def main():
    GlobalInfo.initialize()
    #update = FakeUpdate()
    #context = FakeContext()
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

    dp.add_handler(CommandHandler('stat', tg_stat))
    dp.add_handler(CommandHandler('login', tg_login))
    dp.add_handler(CommandHandler('logout', tg_logout))
    dp.add_handler(MessageHandler(Filters.text, tg_default))

    dp.add_error_handler(tg_error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
