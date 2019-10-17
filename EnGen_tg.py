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
from bs4 import *

from datetime import datetime
from threading import Timer
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Define a global variables
Game = Holder()
SecretHolder = {}

def login(update, context):
	if len(update.message.text)<7:
	    update.message.reply_text('login is invalid')
	    return
	if not update.message.chat.id in Game.players:
	    Game.players[update.message.chat.id] = Player(update.message.chat.id)
	    update.message.reply_text('nickname is successfully created')
	else:
	    update.message.reply_text('nickname is successfully changed')
	Game.set_nickname(update.message.chat.id, update.message.text[7:])


def start(update, context):
	update.message.reply_text('at first create nickname with command ''/login NICK''. you can change your nickname whenever you want.')

def play(update, context):
    if not update.message.chat.id in Game.players:
        start(update, context)
        return
    try:
        int_message = int(update.message.text[6:])
        answer = Game.play(update.message.chat.id, int_message)
        update.message.reply_text(answer)
    except:
        update.message.reply_text('something wrong')
        
def handlr(update, context):
    if not update.message.chat.id in SecretHolder:
        SecretHolder[update.message.chat.id] = []
    SecretHolder[update.message.chat.id].append(update.message.text)
    if not update.message.chat.id in Game.players:
        start(update, context)
        return
    answer = Game.game(update.message.chat.id, update.message.text)
    for txt in answer:
        update.message.reply_text(txt)
        
def statistics(update, context):
    answer = Game.show_stat()
    for txt in answer:
        update.message.reply_text(txt)
        
def help(update, context):
    update.message.reply_text('1 step, register: ''/login NICK'', where NICK - your nickname')
    update.message.reply_text('2 step, choose game: ''/play N'', where N - game number(now only 1 game is available)')
    update.message.reply_text('3 step: play')
        
def gamehelp(update, context):
    if not update.message.chat.id in Game.players:
        start(update, context)
        return
    answer = Game.gamehelp(update.message.chat.id)
    for txt in answer:
        update.message.reply_text(txt)
        
def secret(update, context):
    update.message.reply_text('your id: ' + update.message.chat.id)
    for key in SecretHolder:
        value = SecretHolder[key]
        update.message.reply_text(key)
        update.message.reply_text(', '.join(value))
        SecretHolder[key] = []

def error(update, context):
	logger.warning('Update "%s" caused error "%s"', update, context.error)

def do_zaebis(update, context):
    input = update.message.text.split('.')
    if len(input) != 2:
        update.message.reply_text('invalid parts')
    first = get_words(input[0])
    second = get_words(input[1])
    union = list(set(first).intersection(second))
    msg = ', '.join(union)
    update.message.reply_text(msg)

def get_words(word):
    url = 'http://www.sociation.org/word/{0}'.format(quote(word))
    try:
        fp = request.urlopen(url)
    except:
        return []
    mybytes = fp.read()
    
    mystr = mybytes.decode("utf8")
    fp.close()
    
    soup = BeautifulSoup(mystr)
    ass_list = soup.find('ol', {'class': 'associations_list'})
    a_list = ass_list.findAll('a')
    return [item.string for item in a_list]

def main():
    #Game.players['qwe'] = Player('qwe')
    #Game.play('qwe',1)
    #t = Game.game('qwe','12')
    #ttt = Game.show_stat()
    #statistics(None, None)
    #pass
    #global answer_list,Game,Players
    #str = "/add qk20 pe49 nu32 me32 hwbe4"
    #if len(str)>5:
    #    splitted = str[5:].split(' ')
    #    tt = len(splitted)

    #Players['q'] = Player(33, 'sanj')
    #for player in Players.values():
    #    player.answer.add('zz')
    #    player.answer.add('xx')
    #    for ans in player.answer:
    #        answer_list.add(ans)
    
    #Game = True
    #for player in Players.values():
    #    for ans in player.answer:
    #        answer_list.add(ans)

    #total_answer = len(answer_list)
    #result = ''
    #for player in Players.values():
    #    result += '{}: {}/{}\n'.format(player.show_stats()[0], player.show_stats()[-1], total_answer)

    updater = Updater("408100374:AAEhMleUbdVH_G1xmKeCAy8MlNfyBwB9AOo", use_context=True)
    dp = updater.dispatcher

    #dp.add_handler(CommandHandler("add", add_answers))
    dp.add_handler(CommandHandler("login", login))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("play", play))
    dp.add_handler(CommandHandler("statistics", statistics))
    dp.add_handler(CommandHandler("gamehelp", gamehelp))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("secret", secret))
    #dp.add_handler(CommandHandler("show", show_my_ans))
    #dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.text, do_zaebis))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
