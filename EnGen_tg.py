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

from datetime import datetime
from threading import Timer
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Define a global variables
answer_list = set()
Game = False
Players = {}
BestResults = {}
Time_timer = 7200.0
#Time_timer = 30.0

# Define a class for players in game
class Player (object):
	"""docstring"""

	def __init__(self, id, nickname):
		"""Constructor"""
		self.id = id
		self.nickname = nickname
		self.answer = set()
		self.answer_completed = set()

	def set_answer(self, answer_in):
		self.answer_completed.add(answer_in)
		if not self.answer_completed.__contains__(answer_in):
			self.answer_completed.add(answer_in)

	def show_stats(self):
		score = len(self.answer_completed) - len(self.answer)
		return([self.nickname,self.answer,score])


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#def rewrite_file(filename):
#	f = open(filename, "w")
#	f.close()

#def write_to_file(filename, string):
#	f = open(filename, "w")
#	f.write(string + '\n')
#	f.close()

#def append_to_file(filename, string):
#	f = open(filename, "a")
#	f.write(string + '\n')
#	f.close()

#def add_to_file(filename, string):
#	if os.path.isfile(filename):
#		append_to_file(filename, string)
#	else:
#		write_to_file(filename, string)

#def load_game(filename):
#	f = open(filename, "r")
#	content = f.readlines()
#	f.close()
#	content = [x.strip() for x in content]
#	return content

#def game_of_on():
#	#print("hello, world")
#	global Game
#	if Game == True:
#		Game = False
#	else:
#		Game = True


## Define a few command handlers. These usually take the two arguments bot and
## update. Error handlers also receive the raised TelegramError object in error.
#def start(update, context):
#	"""Send a message when the command /start is issued."""
#	global Time_timer
#	if update.message.chat.id == 64798180:
#		update.message.reply_text('Game started')
#		game_of_on()
#		t = Timer(Time_timer, game_of_on)
#		t.start()

#def finish(update, context):
#	if update.message.chat.id == "64798180":
#		game_of_on()
#		update.message.reply_text('Game over')

#def help(update, context):
#	"""Send a message when the command /help is issued."""
#	help_mes = '''
#    hello
#    huiza'''
#	if os.path.isfile('game_answers') :
#		text = file_read('game_answers')
#		update.message.reply_text(text)
#	file_add('game_answers', r'qwerty')

#	t = 1
#	update.message.reply_text(help_mes)

#def add(update, context):
#	In_str = update.message.text[4:].strip()
#	add_to_file('game_answer', In_str)
#	update.message.reply_text('Answer:' + In_str)

#def addlist(update, context):
#	In_str = update.message.text[8:].split(' ')
#	for item in In_str:
#		add_to_file('game_answer', item)
#	update.message.reply_text(len(answer_list))

#def load(update, context):
#	global answer_list
#	answer_list = load_game('game_answer')
#	update.message.reply_text(len(answer_list))


#def resetanswer(update, context):
#	global answer_list
#	if update.message.chat.id == 64798180:
#		rewrite_file('game_answer')
#		answer_list = load_game('game_answer')
#		update.message.reply_text(len(answer_list))

#def resetgame(update, context):
#	global Players
#	if update.message.chat.id == 64798180:
#		for player in Players.keys():
#			rewrite_file(player)
#		Players.clear()
#		update.message.reply_text('Game reseted!')

#------------------------------------------------------------------------------------------------------------------------------------------------------------

def cheat(update, context):
	global answer_list,Game,Players
	update.message.reply_text(len(answer_list))
	update.message.reply_text(Game)
	update.message.reply_text(len(Players))
	for player in Players.values():
		update.message.reply_text('_______________')
		update.message.reply_text(player.nickname)
		for ans in player.answer:
			update.message.reply_text(ans)
		update.message.reply_text('---')
		for ans in player.answer_completed:
			update.message.reply_text(ans)

def error(update, context):
	logger.warning('Update "%s" caused error "%s"', update, context.error)

def login(update, context):
	global answer_list,Game,Players
	if len(update.message.text)>7:
	    Players[update.message.chat.id] = [True, True, True, True, True, True, True]#Player(update.message.chat.id, update.message.text[7:])
	    #update.message.reply_text(update.message.chat.id)
        
def add_answers(update, context):
	global answer_list,Game,Players
	if not Game and len(update.message.text) > 5 and Players.__contains__(update.message.chat.id):
		splitted = update.message.text[5:].split(' ')
		str_answer = 'added:'
		for code_answer in splitted :
			if not Players[update.message.chat.id].answer.__contains__(code_answer) :
				Players[update.message.chat.id].answer.add(code_answer)
				Players[update.message.chat.id].answer_completed.add(code_answer)
				str_answer+='\n'+code_answer
		update.message.reply_text(str_answer)

def show_my_ans(update, context):
	global answer_list,Game,Players
	if not Game and Players.__contains__(update.message.chat.id):
		str_answer = 'full list:'
		for ans in Players[update.message.chat.id].answer :
			str_answer+='\n'+ans
		update.message.reply_text(str_answer)

def start_game(update, context):
	global answer_list,Game,Players
	Game = True
	for player in Players.values():
		for ans in player.answer:
			answer_list.add(ans)
	update.message.reply_text('success')

def echo(update, context):
	global answer_list,Game,Players
	if Game and update.message.text.startswith('.') and update.message.chat.id > 0:
			answer_for_check = update.message.text[1:].strip()
			if answer_for_check in answer_list:
				update.message.reply_text('+')
				Players[update.message.chat.id].set_answer(answer_for_check)
			else:
				update.message.reply_text('-')

def stats(update, context):
	total_answer = len(answer_list)
	result = ''
	for player in Players.values():
		result += '{}: {}/{}\n'.format(player.show_stats()[0], player.show_stats()[-1], total_answer - len(player.answer))
	update.message.reply_text(result)

def handlr(update, context):
    if not update.message.chat.id in Players:
        Players[update.message.chat.id] = [True, True, True, True, True, True, True]
    update.message.reply_text('d1')
    id = update.message.chat.id
    vals = Players[id]
    text = update.message.text
    if not len(text)==2:
        if text=="0":
            for i in range(7):
                vals[i] = True
        show(update, id)
        update.message.reply_text('d11')
        return
    update.message.reply_text('d2')
    try:
        update.message.reply_text(text[0])
        update.message.reply_text(text[1])
        update.message.reply_text('d3')
        i1 = int(text[0])
        i2 = int(text[1])
        vals[i1-1]=False
        vals[i2-1]=False
        show(update, id)
        update.message.reply_text('d4')
        tmp = [False, False, False, False, False, False, False]
        for i in range(7):
            if vals[i]:
                if i == 0:
                    tmp[1]=True
                    tmp[6]=True
                    continue
                if i == 6:
                    tmp[0]=True
                    tmp[5]=True
                    continue
                tmp[i-1]=True
                tmp[i+1]=True
        update.message.reply_text('d5')
        show(update, id)
    except:
        update.message.reply_text('not valid input')


def show(update, id):
    strr = ''
    for i in range(7):
        if Players[id][i]:
            strr=strr+str(i+1)
        else:
            strr=strr+'x'
    update.message.reply_text(strr)


def main():
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
    #dp.add_handler(CommandHandler("go", start_game))
    #dp.add_handler(CommandHandler("stats", stats))
    ##dp.add_handler(CommandHandler("cheat123", cheat))
    #dp.add_handler(CommandHandler("show", show_my_ans))
    #dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.text, handlr))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
