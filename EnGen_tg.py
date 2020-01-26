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
from urllib import request, parse
from bs4 import *
from urllib.parse import quote
import random
import re
import json
import time

from datetime import datetime
from threading import Timer
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Define a global variables
Holder = GlobalHolder()

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

def tg_start(update, context):
    try:
        bot_authorize(update.message.chat.id)
        update.message.reply_text('для того, чтобы работать с ботом, нужно выбрать определенный режим(решение олимпиек, решени гибридов, специальный режим и т д.)')
        update.message.reply_text('режимы созданы для того, чтобы обрабатывать текст без ввода команды. в каждом режиме бот обрабатывает сообщения определенным образом.')
        update.message.reply_text('переключить режим на следующий в списке можно командой /mode. введя через пробел название(или часть названия) режима - можно переключить конкретно на выбранных режим(например, /mode olymp или просто /mode o).')
        update.message.reply_text('после переключения на режим, можно вводить боту текст для решения выбранной задачи, подробности в /modes')
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))


def tg_modes(update, context):
    try:
        bot_authorize(update.message.chat.id)
        update.message.reply_text('режим disabled:')
        update.message.reply_text('отключены ответы бота на какой-либо текст без команды')
        update.message.reply_text('режим special:')
        update.message.reply_text('постоянно меняется, что в данный момент он делает и работает ли вообще - надо спрашивать')
        update.message.reply_text('режимы olymp, gibrid3, gibrid4, meta, logo, bruk, plus, matr, anag:')
        update.message.reply_text('режимы для помощи в решении заданий: олимпийка, гибриды из трех, гибриды из четырех, метаграмма, логогриф, буква-брюква, плюсограмма, матрица, анаграмма')
        update.message.reply_text('к заданным словам ищутся ассоциации на sociation.org и дальше сравниваются результаты по правилам каждого режима(например, для гибридов это пересечение по трем буквам)')
        update.message.reply_text('формат ввода(простой): вводите первое слово, вводите точку, вводите второе слово. например, если в режиме олимпиек ввести "кошка.полка", то бот возьмет синонимы к слову кошка(плюс само слово кошка), синонимы к слову полка(плюс само слово полка), и будет искать по эти спискам общие слова')
        update.message.reply_text('формат ввода(посложнее): также можно вводить не одно слово, а несколько - и для каджого из них бот будет искать синонимы. вводить нужно через запятую(можно с пробелами). например, если в режиме олимпийка ввести "кошка, собака . дом, кровать, окно", то бот возьмет синонимы к словам кошка и собака(плюс сами слова) и запишет их в первый список, потом возьмет синонимы к словам дом, кровать и окно(аналогично плюс сами эти слова) и запишет их во второй список, и потом выведет общие слова между первым и вторым списками.')
        update.message.reply_text('формат ввода(исключение ассоциаций): если перед словом поставить восклицательный знак либо знак процента, то бот не будет брать к этому слову ассоциации. например, "!окно,дом.сарай": бот возьмет для первого списка слова окно, дом и ассоциации к слову дом, для второго списка - слово сарай и ассоциации к слову сарай')
        update.message.reply_text('формат ввода(накуй ассоциации): если первым символом в сообщении поставить занк доллара, то формат ввода будет совсем другой: все слова будут браться не через запятую, а через любые знаки(кроме точки)/пробел/перенос строки, а также к этим словам не будут браться ассоциации. например, "$корова день окно мышь овал" в режиме гибридов вернет один ответ: корОВАл. то есть бот возьмет только те слова которые указаны, без ассоциаций')
        update.message.reply_text('формат ввода(накуй ассоциации: расширенный): если поставить точку между группами слов, то слова в первой группе не будут сравниваться между собой. например, если у вас есть большой список слов и вы хотите сравнить его на наличие гибридов со словами кошка и овал, можно ввести "$слово1 слово2 тут докуя слов слово100.кошка овал", слово1..слово100 между собой сравниваться не будут, будут сравниваться кошка и овал между собой и кошка и овал с первым списком')
        update.message.reply_text('общая инфа по формату ввода: во всех вышеописанных форматах неважно сколько вы поставите пробелов между словами. валидные варианты: " корова,   дичь   .  место", "стол, %  ум,уж.  %дерево,мост  ", "$  евро  рубль,,,;;;*** сон.карета"')
        update.message.reply_text('формат ввода для матриц(в матрицах, очевидно, нужно сравнивать слова из трех списков, а не из двух): для формата ввода "накуй ассоциации" точки в принципе не нужны, для формата ввода "накуй ассоциации: расширенный" ещё одна точка не нужна, третий список будет дублировать второй, для остальных - точка также является разделителем списков(то есть их должны быть две штуки). например, "кошка.собака,дом.печка,стол"')
        update.message.reply_text('режим combined')
        update.message.reply_text('пока не работает')
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_olymp(update, context):
    try:
        bot_authorize(update.message.chat.id)
        input_text = simple_message_handler(update.message.text, TgCommands.Olymp, True)
        msg = default_input(input_text, ModeType.Olymp)
        update.message.reply_text(msg)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_gibrid(update, context):
    try:
        bot_authorize(update.message.chat.id)
        input_text = simple_message_handler(update.message.text, TgCommands.Gibrid, True)
        msg = default_input(input_text, ModeType.Gibrid3)
        update.message.reply_text(msg)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_meta(update, context):
    try:
        bot_authorize(update.message.chat.id)
        input_text = simple_message_handler(update.message.text, TgCommands.Meta, True)
        msg = default_input(input_text, ModeType.Meta)
        update.message.reply_text(msg)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_logo(update, context):
    try:
        bot_authorize(update.message.chat.id)
        input_text = simple_message_handler(update.message.text, TgCommands.Logo, True)
        msg = default_input(input_text, ModeType.Logo)
        update.message.reply_text(msg)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_switch_mode(update, context):
    global Holder
    try:
        bot_authorize(update.message.chat.id)
        input_text = simple_message_handler(update.message.text, TgCommands.SwitchMode, False)
        settings = Holder.get(update.message.chat.id)
        mode = settings.current_mode
        if input_text is None:
            mode = settings.next_mode()
        else:
            newmodes = ModeType.get_modes_by_alias(input_text)
            if len(newmodes)==0:
                update.message.reply_text('mode not found')
                return
            else:
                if len(newmodes)>1:
                    found_modes = [ModeType.aliases_by_modes[mode_int] for mode_int in newmodes]
                    str_found_modes = [found_mode[0] + '(' + ','.join(found_mode[1:]) + ')' for found_mode in found_modes]
                    update.message.reply_text('more than one mode found:\n' + '\n'.join(str_found_modes))
                    return
                else:
                    mode = newmodes[0]
                    settings.current_mode = mode
        update.message.reply_text('switched to ' + ModeType.aliases_by_modes[mode][0])
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def tg_default(update, context):
    try:
        bot_authorize(update.message.chat.id)
        settings = Holder.get(update.message.chat.id)
        mode = settings.current_mode
        if mode == ModeType.Disabled:
            return
        result = default_input(update.message.text, mode)
        if not result.is_success:
            print_long(update, "failed:\n" + result.message)
            return
        for msg in result.values:
            print_long(update, msg)
    except Exception as e:
        update.message.reply_text("Error: {0}".format(str(e)))

def print_long(update, input_text):
    if len(input_text) > 4096:
        for x in range(0, len(input_text), 4096):
            update.message.reply_text(input_text[x:x+4096])
    else:
        update.message.reply_text(input_text)

#----------

def bot_authorize(id):
    global Holder
    if not id in Holder.settings_by_id:
        Holder.add(id)
        return
        #raise Exception('you are not authorized, please call /start')

def default_input(text, mode):
    text_handler = Holder.default_text_handlers_by_modes[mode]
    if text_handler is None:
        return Result.failed("current mode is not supported yet")
    return text_handler.do_action(text)

def simple_message_handler(full_text, command, empty_is_invalid = False):
    if len(full_text)<len(command)+3:
        if empty_is_invalid:
            raise Exception('command should contains arguments')
        return None
    return full_text[len(command)+2:]

def main():
    # handler = Holder.default_text_handlers_by_modes[ModeType.Olymp]
    # start = time.time()
    # result = handler.do_action('кошка.собака,копыто')
    # end = time.time()
    # print(end - start)

    # updater = Updater("408100374:AAEhMleUbdVH_G1xmKeCAy8MlNfyBwB9AOo", use_context=True)
    updater = Updater("979411435:AAEHIVLx8L8CxmjIHtitaH4L1GeV_OCRJ7M", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler(TgCommands.Modes, tg_modes))
    dp.add_handler(CommandHandler(TgCommands.Start, tg_start))
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
