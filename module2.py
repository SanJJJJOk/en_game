import enum
import re
from urllib import request, parse
import json
from CubraDefinition import *
from RussianWords import *
import random
from datetime import datetime, date, time, timedelta

class Emojies:
    OneHandSword = '\ud83d\udde1'
    TwoHandSword = '\u2694\ufe0f'
    Headgear = '\ud83c\udfa9'
    Armor = '\ud83e\udde5'
    Footgear = '\ud83e\udd7e'
    Power = '\ud83d\udcaa'
    NoClass = '\ud83d\udc76'
    Warrior = '\ud83d\udee1'
    Wizard = '\u2728'
    Thief = '\ud83d\udd2a'
    Cleric = '\ud83d\udd2e'
    Human = '\ud83e\uddcd'
    Elf = '\ud83c\udff9'
    Halfling = '\ud83e\udd6a'
    Dwarf = '\ud83e\ude93'
    Result0 = '\u2705'#good
    Result1 = '\u274c'#bad
    Result2 = '\u23f3'#time

class RaceClassType:
    NoClass = 1
    Warrior = 2
    Wizard = 3
    Thief = 4
    Cleric = 5
    Human = 6
    Elf = 7
    Halfling = 8
    Dwarf = 9
    CRNames = {
        1: 'Нет класса',
        2: 'Воин',
        3: 'Волшебник',
        4: 'Вор',
        5: 'Клирик',
        6: 'Человек(без расы)',
        7: 'Эльф',
        8: 'Халфлинг',
        9: 'Дварф',
        }
    CREmojies = {
        1: Emojies.NoClass,
        2: Emojies.Warrior,
        3: Emojies.Wizard,
        4: Emojies.Thief,
        5: Emojies.Cleric,
        6: Emojies.Human,
        7: Emojies.Elf,
        8: Emojies.Halfling,
        9: Emojies.Dwarf,
        }

    @staticmethod
    def is_class(type):
        return type==RaceClassType.NoClass or type==RaceClassType.Warrior or type==RaceClassType.Wizard or type==RaceClassType.Thief or type==RaceClassType.Cleric

    #@staticmethod
    #def is_race(type):
    #    return type==RaceClassType.Human or type==RaceClassType.Elf or type==RaceClassType.Halfling or type==RaceClassType.Dwarf
    
class TreasureType:
    Headgear = 1
    Armor = 2
    Footgear = 3
    OneHandWeapon = 4
    TwoHandWeapon = 5
    #Jewel = 6
    TreasureNames = {
        1: 'Головняк',
        2: 'Броник',
        3: 'Обувка',
        4: 'В 1 руку',
        5: 'В 2 руки',
        #6: 'Украшение',
        }
    TreasureEmojies = {
        1: Emojies.Headgear,
        2: Emojies.Armor,
        3: Emojies.Footgear,
        4: Emojies.OneHandSword,
        5: Emojies.TwoHandSword,
        }
    
class Result:
    ResultEmojies = {
        0: Emojies.Result0,
        1: Emojies.Result1,
        2: Emojies.Result2,
        }
    def __init__(self, result_code, message):
        self.result_code = result_code
        self.message = message

class Treasure:
    def __init__(self, name, rc_type, tr_type, power, is_big, tr_code):
        self.name = name
        self.rc_type = rc_type
        self.tr_type = tr_type
        self.power = power
        self.is_big = is_big
        self.tr_code = tr_code
        
    def get_small_info(self):
        info =  TreasureType.TreasureEmojies[self.tr_type] + '+' + str(self.power)
        if not self.rc_type is None:
            info = info + ' [' + RaceClassType.CREmojies[self.rc_type] + ']'
        if self.is_big:
            info = info + ' БОЛЬШАЯ'
        info = info + ' - ' + self.name + '(' + self.tr_code + ')'
        return info

    #def get_small_info_old(self):
    #    info = self.name + '(' + self.tr_code + '): ' + TreasureType.TreasureEmojies[self.tr_type] + '(+' + str(self.power) + ')'
    #    if not self.rc_type is None:
    #        info = info + ' [' + RaceClassType.CRNames[self.rc_type] + ']'
    #    if self.is_big:
    #        info = info + ' БОЛЬШАЯ'
    #    return info

class Monster:
    def __init__(self, fightcode, defeatcode, lvl, lvlcodes, bonuses):
        self.monster_fightcode = fightcode
        self.monster_defeatcode = defeatcode
        self.monster_lvlcodes = lvlcodes
        self.monster_lvl = lvl
        self.bonuses_to_mnch = bonuses
        
class Munchkin:
    def __init__(self, name):
        self.name = name
        self.current_lvl = 1
        self.current_race = RaceClassType.Human
        self.current_class = RaceClassType.NoClass
        self.used_trs = []
        self.used_levels_codes = []
        self.use_three_hands = False
        self.race_change_datetime = None
        self.class_change_datetime = None
        self.monster_fight_datetime = None

class GlobalInfo:
    munchkins_logins = {
        'iqnsffw': Munchkin('otwt'), 
        'oqofndh': Munchkin('div'),
        'qnoruwd': Munchkin('mars'),
        }
    registered_players = {}#.chat.id-key,Munchkin-value
    monsters = [
        Monster('мор4','1539',1,['л5321'],{}),
        Monster('муп2','3661',2,['л7669'],{}),
        Monster('мма3','2204',2,['л5656'],{}),
        Monster('мпк6','7652',4,['л3218'],{
            RaceClassType.Wizard: 2
            }),
        Monster('мте4','4071',5,['л4231'],{}),
        Monster('моа8','8029',6,['л0331'],{}),
        Monster('мсу1','5676',8,['л3580'],{
            RaceClassType.Warrior: 1
            }),
        Monster('мех5','3063',9,['л8988'],{
            RaceClassType.Wizard: 1
            }),
        Monster('мхм4','4753',10,['л4815'],{}),
        Monster('мкб7','9982',12,['л1251'],{}),
        Monster('мвя3','1914',13,['л5246'],{
            RaceClassType.Elf: -5
            }),
        Monster('мпо2','3777',15,['л7313'],{
            RaceClassType.Elf: 1,
            RaceClassType.Warrior: 1
            }),
        Monster('мас9','8211',19,['л1181'],{}),
        Monster('мде6','2119',21,['л6369'],{}),
        Monster('мгл2','2183',23,['л2534'],{
            RaceClassType.Warrior: 1
            }),
        ]
    treasures = [
        Treasure('карнавальная маска', RaceClassType.Wizard, TreasureType.Headgear, 1, False, 'гуп7'),#5
        Treasure('сланцы', RaceClassType.Elf, TreasureType.Footgear, 1, False, 'сан2'),#6
        Treasure('жилетка новичка', RaceClassType.Wizard, TreasureType.Armor, 1, False, 'бор6'),#8
        Treasure('шлем из картона', RaceClassType.Warrior, TreasureType.Headgear, 1, False, 'гус9'),#9
        Treasure('палка', RaceClassType.Warrior, TreasureType.OneHandWeapon, 1, False, 'ора5'),#9
        Treasure('шелковые тапочки', RaceClassType.Wizard, TreasureType.Footgear, 2, False, 'сок7'),#10
        Treasure('длинный лук', RaceClassType.Elf, TreasureType.TwoHandWeapon, 2, True, 'трс3'),#10
        Treasure('бронька', None, TreasureType.Armor, 1, False, 'бас2'),#12
        Treasure('эльфомечик', RaceClassType.Elf, TreasureType.OneHandWeapon, 2, False, 'ому7'),#12
        Treasure('тапки вязаные', None, TreasureType.Footgear, 1, False, 'сыч8'),#13
        Treasure('массивный шлем', RaceClassType.Warrior, TreasureType.Headgear, 2, True, 'гон6'),#13
        Treasure('защитный шлем', None, TreasureType.Headgear, 1, False, 'гав4'),#15
        Treasure('доспех воина', RaceClassType.Warrior, TreasureType.Armor, 2, False, 'бух5'),#15
        Treasure('высокие сапоги', None, TreasureType.Footgear, 2, False, 'сфи4'),#19
        Treasure('божественная тиара', None, TreasureType.Headgear, 2, False, 'гкк2'),#19
        Treasure('великая броня света', RaceClassType.Wizard, TreasureType.Armor, 3, True, 'буа5'),#19
        Treasure('минипосох', RaceClassType.Wizard, TreasureType.OneHandWeapon, 1, False, 'оля2'),#21
        Treasure('нейроботы', RaceClassType.Wizard, TreasureType.Footgear, 3, False, 'сем9'),#21
        Treasure('бронежилет', None, TreasureType.Armor, 2, False, 'бур4'),#21
        Treasure('мегамеч', RaceClassType.Warrior, TreasureType.TwoHandWeapon, 4, True, 'тен3'),#23
        Treasure('леви-кроссы', RaceClassType.Elf, TreasureType.Footgear, 3, False, 'сук2'),#23
        Treasure('крепкие латы', RaceClassType.Warrior, TreasureType.Footgear, 2, False, 'ска5'),#23
        ]
    classes = {
        RaceClassType.NoClass: 'ком1',
        RaceClassType.Warrior: 'кан3',
        RaceClassType.Wizard: 'куу7',
        RaceClassType.Thief: 'абв4',
        RaceClassType.Cleric: 'абв5',
        }
    races = {
        RaceClassType.Human: 'раз1',
        RaceClassType.Elf: 'ров9',
        RaceClassType.Halfling: 'абв8',
        RaceClassType.Dwarf: 'абв9',
        }
    c_level_codes = {}
    c_monster_fight_codes = {}
    c_class_codes = {}
    c_race_codes = {}
    c_treasure_codes = {}
    c_singlecode_handlers = {}

    @staticmethod
    def initialize():
        for monster in GlobalInfo.monsters:
            for lvlcode in monster.monster_lvlcodes:
                GlobalInfo.c_level_codes[lvlcode] = monster
                GlobalInfo.c_singlecode_handlers[lvlcode] = GlobalInfo.simple_text_handler_level
            GlobalInfo.c_monster_fight_codes[monster.monster_fightcode] = monster
            GlobalInfo.c_singlecode_handlers[monster.monster_fightcode] = GlobalInfo.simple_text_handler_fight
        for clss in GlobalInfo.classes:
            c_code = GlobalInfo.classes[clss]
            GlobalInfo.c_class_codes[c_code] = clss
            GlobalInfo.c_singlecode_handlers[c_code] = GlobalInfo.simple_text_handler_class
        for race in GlobalInfo.races:
            r_code = GlobalInfo.races[race]
            GlobalInfo.c_race_codes[r_code] = race
            GlobalInfo.c_singlecode_handlers[r_code] = GlobalInfo.simple_text_handler_race
        for treasure in GlobalInfo.treasures:
            GlobalInfo.c_treasure_codes[treasure.tr_code] = treasure
        dt_now = datetime.now()
        for login in GlobalInfo.munchkins_logins:
            munchkin = GlobalInfo.munchkins_logins[login]
            munchkin.race_change_datetime = dt_now
            munchkin.class_change_datetime = dt_now
            munchkin.monster_fight_datetime = dt_now
    
    @staticmethod
    def simple_text_handler_level(munchkin, input_text):
        if not input_text in GlobalInfo.c_level_codes:
            raise Exception('орг косяк, сообщите ему об этом( @sanjjjjok )')

        if input_text in munchkin.used_levels_codes:
            return Result(1, 'вы уже получили уровень по этому коду')

        munchkin.used_levels_codes.append(input_text)
        munchkin.current_lvl = munchkin.current_lvl + 1
        #save lvls
        return Result(0, 'Ура! Ваш новый уровень: ' + str(munchkin.current_lvl))
    
    @staticmethod
    def simple_text_handler_class(munchkin, input_text):
        if not input_text in GlobalInfo.c_class_codes:
            raise Exception('орг косяк, сообщите ему об этом( @sanjjjjok )')
    
        dt_now = datetime.now()
        new_class = GlobalInfo.c_class_codes[input_text]
        if munchkin.current_class==new_class:
            return Result(1, 'вы уже текущего класса')

        if munchkin.class_change_datetime > dt_now:
            dt_diff = (munchkin.class_change_datetime - dt_now).total_seconds()
            block_msg = 'следующая смена класса возможна через ' + str(round(dt_diff // 60)) + 'мин ' + str(round(dt_diff % 60)) + 'с'
            return Result(2, block_msg)

        munchkin.current_class = new_class
        munchkin.used_trs = []
        munchkin.class_change_datetime = dt_now + timedelta(0,10)
        return Result(0, 'Ура! Ваш новый класс: ' + RaceClassType.CREmojies[new_class] + RaceClassType.CRNames[new_class])

    @staticmethod
    def simple_text_handler_race(munchkin, input_text):
        if not input_text in GlobalInfo.c_race_codes:
            raise Exception('орг косяк, сообщите ему об этом( @sanjjjjok )')
    
        dt_now = datetime.now()
        new_race = GlobalInfo.c_race_codes[input_text]
        if munchkin.current_race==new_race:
            return Result(1, 'вы уже текущей расы')

        if munchkin.race_change_datetime > dt_now:
            dt_diff = (munchkin.race_change_datetime - dt_now).total_seconds()
            block_msg = 'следующая смена расы возможна через ' + str(round(dt_diff // 60)) + 'мин ' + str(round(dt_diff % 60)) + 'с'
            return Result(2, block_msg)

        munchkin.current_race = new_race
        munchkin.used_trs = []
        munchkin.race_change_datetime = dt_now + timedelta(0,10)
        return Result(0, 'Ура! Ваша новая раса: ' + RaceClassType.CREmojies[new_race] + RaceClassType.CRNames[new_race])

    @staticmethod
    def simple_text_handler_fight(munchkin, input_text):
        if not input_text in GlobalInfo.c_monster_fight_codes:
            raise Exception('орг косяк, сообщите ему об этом( @sanjjjjok )')
    
        dt_now = datetime.now()
        if munchkin.monster_fight_datetime > dt_now:
            dt_diff = (munchkin.monster_fight_datetime - dt_now).total_seconds()
            block_msg = 'следующая битва возможна через ' + str(round(dt_diff // 60)) + 'мин ' + str(round(dt_diff % 60)) + 'с'
            return Result(2, block_msg)

        monster = GlobalInfo.c_monster_fight_codes[input_text]
        total_power = munchkin.current_lvl
        for tr in munchkin.used_trs:
            total_power = total_power + tr.power
        for cr_bonus in monster.bonuses_to_mnch:
            if munchkin.current_class == cr_bonus or munchkin.current_race == cr_bonus:
                total_power = total_power + monster.bonuses_to_mnch[cr_bonus]

        munchkin.monster_fight_datetime = dt_now + timedelta(0,5)
        if total_power > monster.monster_lvl or (total_power == monster.monster_lvl and munchkin.current_class == RaceClassType.Warrior):
            return Result(0, 'Ура! Монстр победжен! Код побежденного монстра:' + monster.monster_defeatcode)
        else:
            return Result(1, 'вы не смогли победить монстра =(')
    
    @staticmethod
    def do_beautiful_with_treasures(munchkin, treasure_codes):
        input_treasures = []
        for tr_code in treasure_codes:
            if not tr_code in GlobalInfo.c_treasure_codes:
                return Result(1, 'нет сокровища с таким кодом: ' + tr_code)
            input_treasures.append(GlobalInfo.c_treasure_codes[tr_code])
        check_equip_msg = GlobalInfo.check_equip(munchkin, input_treasures)
        if check_equip_msg is None:
            munchkin.used_trs = input_treasures
            return Result(0, 'Ура! Вы успешно переоделись')
        return Result(1, check_equip_msg)

    @staticmethod
    def check_equip(munchkin, input_treasures):
        count_big = 0
        headgear_count = 0
        armor_count = 0
        footgear_count = 0
        hand_weapon_count = 0
        for tr in input_treasures:
            if tr.is_big:
                count_big = count_big + 1
            if tr.tr_type == TreasureType.Headgear:
                headgear_count = headgear_count + 1
            if tr.tr_type == TreasureType.Armor:
                armor_count = armor_count + 1
            if tr.tr_type == TreasureType.Footgear:
                footgear_count = footgear_count + 1
            if tr.tr_type == TreasureType.OneHandWeapon:
                hand_weapon_count = hand_weapon_count + 1
            if tr.tr_type == TreasureType.TwoHandWeapon:
                hand_weapon_count = hand_weapon_count + 2
            if not tr.rc_type is None:
                if tr.rc_type!=munchkin.current_class and tr.rc_type!=munchkin.current_race:
                    return tr.name + ' не предназначено для вашей расы/класса'
        if munchkin.use_three_hands and hand_weapon_count > 3:
            return 'нельзя использовать более трёх рук'
        if not munchkin.use_three_hands and hand_weapon_count > 2:
            return 'нельзя использовать более двух рук'
        if count_big>1 and munchkin.current_race!=RaceClassType.Dwarf:
            return 'нельзя носить более одной большой вещи, если вы не ' + RaceClassType.CRNames[RaceClassType.Dwarf]
        if headgear_count>1:
            return 'нельзя носить более одного элемента одежды ' + TreasureType.TreasureNames[TreasureType.Headgear]
        if armor_count>1:
            return 'нельзя носить более одного элемента одежды ' + TreasureType.TreasureNames[TreasureType.Armor]
        if footgear_count>1:
            return 'нельзя носить более одного элемента одежды ' + TreasureType.TreasureNames[TreasureType.Footgear]
        return None
        
    @staticmethod
    def split_and_remove_empty(text) -> []:
        arr = text.split(' ')
        return [i for i in arr if i]
    