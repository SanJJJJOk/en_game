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


def tg_add_symbol(update, context, word, symbol):
    GlobalMonopoly.added_items[update.message.message_id] = Item(word, symbol)
    if word in GlobalMonopoly.holder:
        symbols = [i.symbol for i in GlobalMonopoly.holder[word]]
        if symbol in symbols:
            update.message.reply_text(EmojiesMegakod.GrayMark + 'было уже')
            return
        else:
            GlobalMonopoly.holder[word].append(Answer(str(update.message.from_user.id), symbol))
    else:
        GlobalMonopoly.holder[word] = [Answer(str(update.message.from_user.id), symbol)]
    count = len(GlobalMonopoly.holder[word])
    new_symbols = [i.symbol for i in GlobalMonopoly.holder[word]]
    new_symbols.sort()
    update.message.reply_text(EmojiesMegakod.GreenMark + 'опачки, ' + get_small_info(word))
    if count == GlobalMonopoly.count_card_on_street - 1:
        update.message.reply_text(EmojiesMegakod.Important + 'ещё один ' + word + ' и всё')
        return
    if count == GlobalMonopoly.count_card_on_street:
        update.message.reply_text(EmojiesMegakod.Important + EmojiesMegakod.Important + EmojiesMegakod.Important + 'ЕБАШЬ ЗА ОТЕЛЕМ ' + word)
        return

def tg_rem_sym(update, context, word, symbol):
    if not word in GlobalMonopoly.holder:
        update.message.reply_text(EmojiesMegakod.NotFound + word + ' не найден')
        return
    for i in GlobalMonopoly.holder[word]:
        if i.symbol == symbol:
            GlobalMonopoly.holder[word].remove(i)
            count = len(GlobalMonopoly.holder[word])
            new_symbols = [i.symbol for i in GlobalMonopoly.holder[word]]
            new_symbols.sort()
            update.message.reply_text(EmojiesMegakod.GreenCross + 'удалил. ' + get_small_info(word))
            return
    update.message.reply_text(EmojiesMegakod.NotFound + symbol + ' из ' + word + ' не найден')
    return

def tg_def_act_base(update, context, text, action):
    input = text.split(' ')
    if len(input)>2:
        update.message.reply_text(EmojiesMegakod.RedCross + 'чёт дохера пробелов')
        return None
    if len(input[0].strip()) == 0:
        update.message.reply_text(EmojiesMegakod.RedCross + 'пустая строка')
        return None
    if len(input)==2:
        return Item(input[0], input[1])
    else:
        return Item(text[:-1], str(text[-1]))

def tg_def_act_two(update, context, text, action):
    item = tg_def_act_base(update, context, text, action)
    if item is None:
        return
    really_input_words = [word for word in GlobalMonopoly.holder if word.startswith(item.word)]
    if len(really_input_words) == 0:
        update.message.reply_text(EmojiesMegakod.RedCross + 'пошел нахуй')
        return
    if len(really_input_words) > 1:
        update.message.reply_text(EmojiesMegakod.RedCross + 'нашел дохуя, выбери чёт одно:\n' + '\n'.join(really_input_words))
        return
    action(update, context, really_input_words[0], item.symbol)

def tg_def_act_one(update, context, text, action):
    item = tg_def_act_base(update, context, text, action)
    if item is None:
        return
    action(update, context, item.word, item.symbol)

def tg_m_default(update, context):
    try:
        text = update.message.text.lower()
        reply_msg = update.message.reply_to_message
        if not reply_msg is None:
            if not reply_msg.message_id in GlobalMonopoly.added_items:
                return
            item = GlobalMonopoly.added_items[reply_msg.message_id]
            if text == '-':
                tg_rem_sym(update, context, item.word, item.symbol)
                return

            if text.startswith('--') or text.startswith('—'):
                if item.word in GlobalMonopoly.holder:
                    del GlobalMonopoly.holder[item.word]
                    update.message.reply_text(item.word + ' - удалено, збс')
                    return
                update.message.reply_text(item.word + ' - нет такого слова, вращайте барабан')
                return
            
            if text.startswith(',,'):
                tg_rem_sym(update, context, item.word, item.symbol)
                tg_def_act_two(update, context, tg_add_symbol)
                return

            if text.startswith(','):
                tg_rem_sym(update, context, item.word, item.symbol)
                tg_def_act_one(update, context, tg_add_symbol)
                return


            update.message.reply_text(EmojiesMegakod.RedCross + 'так писать нельзя')
            return

        if text.startswith('+++'):
            input = text[3:].split(' ')
            for i in input:
                GlobalMonopoly.holder[i] = []
            update.message.reply_text(text[3:] + ' - добавлено/очищено, збс')
            return

        if text.startswith('++'):
            word = text[2:]
            GlobalMonopoly.holder[word] = []
            update.message.reply_text(word + ' - очищено, збс')
            return

        if text.startswith('--') or text.startswith('—'):
            word = text[1:]
            if text.startswith('--'):
                word = text[2:]
            if word in GlobalMonopoly.holder:
                del GlobalMonopoly.holder[word]
                update.message.reply_text(word + ' - удалено, збс')
                return
            update.message.reply_text(word + ' - нет такого слова, вращайте барабан')
            return
        
        if text.startswith('!!'):
            tg_def_act_two(update, context, text[2:], tg_rem_sym)
            return

        if text.startswith(',,'):
            tg_def_act_two(update, context, text[2:], tg_add_symbol)
            return

        if text.startswith('!'):
            int_value = get_int(text[1:])
            if not int_value is None:
                GlobalMonopoly.money = GlobalMonopoly.money - int_value
                update.message.reply_text(EmojiesMegakod.MoneyMinus + 'вычтено ' + str(int_value) + ', осталось ' + str(GlobalMonopoly.money))
                GlobalMonopoly.money_history.append(-int_value)
                return
            tg_def_act_one(update, context, text[1:], tg_rem_sym)
            return
        
        if text.startswith(','):
            int_value = get_int(text[1:])
            if not int_value is None:
                GlobalMonopoly.money = GlobalMonopoly.money + int_value
                update.message.reply_text(EmojiesMegakod.MoneyPlus + 'добавлено ' + str(int_value) + ', осталось ' + str(GlobalMonopoly.money))
                GlobalMonopoly.money_history.append(int_value)
                return
            tg_def_act_one(update, context, text[1:], tg_add_symbol)
            return
        
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
        
def tg_m_add(update, context):
    try:
        text = update.message.text[len(TgCommands.Add)+2:]
        tg_def_act_one(update, context, text, tg_add_symbol)
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
        
def tg_m_del(update, context):
    try:
        text = update.message.text[len(TgCommands.Del)+2:]
        tg_def_act_one(update, context, text, tg_rem_sym)
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
        
def tg_m_fastadd(update, context):
    try:
        text = update.message.text[len(TgCommands.FastAdd)+2:]
        tg_def_act_two(update, context, text, tg_add_symbol)
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
        
def tg_m_quickdel(update, context):
    try:
        text = update.message.text[len(TgCommands.QuickDel)+2:]
        tg_def_act_two(update, context, text, tg_rem_sym)
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
        
#def tg_m_stat(update, context):
#    try:
#        output = []
#        for word in GlobalMonopoly.holder:
#            strtr = str(len(GlobalMonopoly.holder[word])) + ' - ' + word
#            output.append(strtr)
#        output.sort()
#        update.message.reply_text('money=' + str(GlobalMonopoly.money) + '\n' + '\n'.join(output))
#    except Exception as e:
#        err_msg = "неизвестная ошибка: {0}".format(str(e))
#        update.message.reply_text(err_msg)
#        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
        
def tg_m_stat(update, context):
    try:
        output = []
        for word in GlobalMonopoly.holder:
            word_data = GlobalMonopoly.holder[word]
            players = [GlobalMonopoly.get_user(i.user_id) for i in word_data]
            symbols = [i.symbol for i in word_data]
            strtr = str(len(word_data)) + ' - ' + word + ' (' + ','.join(symbols) + ')' + ' (' + ','.join(players) + ')'
            output.append(strtr)
        output.sort()
        update.message.reply_text('money=' + str(GlobalMonopoly.money) + '\n' + '\n'.join(output))
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
        
def tg_m_set_count(update, context):
    try:
        GlobalMonopoly.count_card_on_street = int(update.message.text[len(TgCommands.Count)+2:])
        update.message.reply_text('збс')
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
         
def tg_m_money(update, context):
    try:
        update.message.reply_text('money=' + str(GlobalMonopoly.money) + '\n' + '\n'.join([str(i) for i in GlobalMonopoly.money_history]))
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
          
def tg_m_help(update, context):
    try:
        update.message.reply_text(',синий1 или ,синий 1 или /add синий1 - добавить на улицу "СИНИЙ" дом "1"\n'
        +',синий 123нахуй - добавить на улицу "СИНИЙ" дом "123нахуй"\n'
        +'!синий1 или !синий 1 или /del синий1 - удалить с улицы "СИНИЙ" дом "1"\n'
        +'!синий 123нахуй - удалить с улицы "СИНИЙ" дом "123нахуй"\n'
        +'---------------------\n'
        +'"-" на реплаенное сообщение ",синий1" удаляет с улицы "СИНИЙ" дом "1"\n'
        +'",красный3" на реплаенное сообщение ",синий1" удаляет с улицы "СИНИЙ" дом "1" и добавляет на улицу "КРАСНЫЙ" дом "3"\n'
        +'---------------------\n'
        +',100 - добавить 100 бабла\n'
        +'!100 - убрать 100 бабла\n'
        +'---------------------\n'
        +',,с1 или ,,с 1 или /fastadd c1 - бот находит улицу "СИНИЙ" и добавляет дом "1"\n'
        +',,с1 или ,,с 1 или /fastadd c1 - бот находит улицу "СИНИЙ" и "СИРЕНЕВЫЙ" и не может определиться\n'
        +',,с1 или ,,с 1 или /fastadd c1 - бот не находит улицу "СИНИЙ" и посылает вас нахуй\n'
        +'!!с1 или !!c 1 или /quickdel c1 - всё то же самое для удаления\n'
        )
    except Exception as e:
        err_msg = "неизвестная ошибка: {0}".format(str(e))
        update.message.reply_text(err_msg)
        context.bot.send_message('228485598', err_msg + 'id:' + str(update.message.chat.id))
        
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

def main():
    #GlobalInfo.initialize()
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
    
    dp.add_handler(CommandHandler(TgCommands.Del, tg_m_del))
    dp.add_handler(CommandHandler(TgCommands.Add, tg_m_add))
    dp.add_handler(CommandHandler(TgCommands.FastAdd, tg_m_fastadd))
    dp.add_handler(CommandHandler(TgCommands.QuickDel, tg_m_quickdel))
    dp.add_handler(CommandHandler(TgCommands.Money, tg_m_money))
    dp.add_handler(CommandHandler(TgCommands.Help, tg_m_help))
    dp.add_handler(CommandHandler(TgCommands.Count, tg_m_set_count))
    dp.add_handler(CommandHandler(TgCommands.Stat, tg_m_stat))
    dp.add_handler(MessageHandler(Filters.text, tg_m_default))

    dp.add_error_handler(tg_error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
