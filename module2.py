import enum
import re
from urllib import request, parse
import json
from CubraDefinition import *
from RussianWords import *
import random
from datetime import datetime, date, time, timedelta

class RaceClassType():
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

    @staticmethod
    def is_class(type):
        return type==RaceClassType.NoClass or type==RaceClassType.Warrior or type==RaceClassType.Wizard or type==RaceClassType.Thief or type==RaceClassType.Cleric

    #@staticmethod
    #def is_race(type):
    #    return type==RaceClassType.Human or type==RaceClassType.Elf or type==RaceClassType.Halfling or type==RaceClassType.Dwarf
    
class TreasureType():
    Headgear = 1
    Armor = 2
    Footgear = 3
    OneHandWeapon = 4
    TwoHandWeapon = 5
    Jewel = 6
    
class Result():
    def __init__(self, result_code, message):
        self.result_code = result_code
        self.message = message

class Treasure():
    def __init__(self, name, rc_type, tr_type, power, is_big, tr_code):
        self.name = name
        self.rc_type = rc_type
        self.tr_type = tr_type
        self.power = power
        self.is_big = is_big
        self.tr_code = tr_code

class Monster():
    def __init__(self, fightcode, defeatcode, lvl, lvlcodes, bonuses):
        self.monster_fightcode = fightcode
        self.monster_defeatcode = defeatcode
        self.monster_lvlcodes = lvlcodes
        self.monster_lvl = lvl
        self.bonuses_to_mnch = bonuses
        
class Munchkin():
    def __init__(self):
        self.current_lvl = 1
        self.current_race = RaceClassType.Human
        self.current_class = RaceClassType.NoClass
        self.used_trs = []
        self.used_levels_codes = []
        self.use_three_hands = False
        self.race_change_datetime = None
        self.class_change_datetime = None
        self.monster_fight_datetime = None

class GlobalInfo():
    munchkins_logins = {
        '1234': Munchkin(), 
        '2345': Munchkin()
        }
    registered_players = {}#.chat.id-key,Munchkin-value
    monsters = [
        Monster('fa9182','da3927',1,['l1002'],{
            RaceClassType.Warrior: 2
            }),
        Monster('fa5122','da4159',1,['l4146'],{})
        ]
    treasures = [
        Treasure('head name 1', None, TreasureType.Headgear, 1, False, 'tan1'),
        ]
    classes = {
        RaceClassType.NoClass: 'abc1',
        RaceClassType.Warrior: 'abc2',
        RaceClassType.Wizard: 'abc3',
        RaceClassType.Thief: 'abc4',
        RaceClassType.Cleric: 'abc5',
        }
    races = {
        RaceClassType.Human: 'abc6',
        RaceClassType.Elf: 'abc7',
        RaceClassType.Halfling: 'abc8',
        RaceClassType.Dwarf: 'abc9',
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
    
    @staticmethod
    def simple_text_handler_level(munchkin, input_text):
        if not input_text in GlobalInfo.c_level_codes:
            raise Exception('орг косяк, сообщите ему об этом( @sanjjjjok )')

        if input_text in munchkin.used_levels_codes:
            return Result(1, 'вы уже получили уровень по этому коду')

        munchkin.used_levels_codes.append(input_text)
        munchkin.current_lvl = munchkin.current_lvl + 1
        #save lvls
        return Result(0, 'Ура! Ваш новый уровень: ' + munchkin.current_lvl)
    
    @staticmethod
    def simple_text_handler_class(munchkin, input_text):
        if not input_text in GlobalInfo.c_class_codes:
            raise Exception('орг косяк, сообщите ему об этом( @sanjjjjok )')
    
        dt_now = datetime.now()
        new_class = GlobalInfo.c_class_codes[input_text]
        if munchkin.current_class==new_class:
            return Result(1, 'вы уже текущего класса')

        if munchkin.class_change_datetime < dt_now:
            dt_diff = (munchkin.class_change_datetime - dt_now).total_seconds()
            block_msg = 'следующая смена класса возможна через ' + str(round(dt_diff // 60)) + 'мин ' + str(round(dt_diff % 60)) + 'с'
            return Result(2, block_msg)

        munchkin.current_class = new_class
        munchkin.class_change_datetime = dt_now + timedelta(0,300)
        return Result(0, 'Ура! Ваш новый класс: ' + RaceClassType.CRNames[new_class])

    @staticmethod
    def simple_text_handler_race(munchkin, input_text):
        if not input_text in GlobalInfo.c_race_codes:
            raise Exception('орг косяк, сообщите ему об этом( @sanjjjjok )')
    
        dt_now = datetime.now()
        new_race = GlobalInfo.c_race_codes[input_text]
        if munchkin.current_race==new_race:
            return Result(1, 'вы уже текущей расы')

        if munchkin.race_change_datetime < dt_now:
            dt_diff = (munchkin.race_change_datetime - dt_now).total_seconds()
            block_msg = 'следующая смена расы возможна через ' + str(round(dt_diff // 60)) + 'мин ' + str(round(dt_diff % 60)) + 'с'
            return Result(2, block_msg)

        munchkin.current_race = new_race
        munchkin.race_change_datetime = dt_now + timedelta(0,300)
        return Result(0, 'Ура! Ваша новая раса: ' + RaceClassType.CRNames[new_race])

    @staticmethod
    def simple_text_handler_fight(munchkin, input_text):
        if not input_text in GlobalInfo.c_monster_fight_codes:
            raise Exception('орг косяк, сообщите ему об этом( @sanjjjjok )')
    
        dt_now = datetime.now()
        if munchkin.monster_fight_datetime < dt_now:
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

        munchkin.monster_fight_datetime = dt_now + timedelta(0,120)
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
        check_equip_msg = check_equip(munchkin, input_treasures)
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
            return 'нельзя носить более одной большой вещи, если вы не Дварф'
        if headgear_count>1:
            return 'нельзя носить более одного элемента одежды Головняк'
        if armor_count>1:
            return 'нельзя носить более одного элемента одежды Броня'
        if footgear_count>1:
            return 'нельзя носить более одного элемента одежды Ступни'
        return None
        
    @staticmethod
    def split_and_remove_empty(text) -> []:
        arr = text.split(' ')
        return [i for i in arr if i]
    