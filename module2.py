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
    #Shield = '\ud83e\udd1e'
    Chicken = '\ud83d\udc25'
    Important = '\u2757\ufe0f'
    Info = '\u2139\ufe0f'
    Money = '\ud83d\udcb2'

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

class TreasureType:
    Headgear = 1
    Armor = 2
    Footgear = 3
    OneHandWeapon = 4
    TwoHandWeapon = 5
    TreasureNames = {
        1: 'Головняк',
        2: 'Броник',
        3: 'Обувка',
        4: 'В 1 руку',
        5: 'В 2 руки',
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
        3: Emojies.Chicken,
        }
    def __init__(self, code, message, target_munchkin = None, target_message = None):
        self.code = code
        self.message = message
        self.target_munchkin = target_munchkin
        self.target_message = target_message

class Treasure:
    def __init__(self, id, name, rc_type, tr_type, power, is_big, tr_code, monster_id):
        self.id = id
        self.name = name
        self.rc_type = rc_type
        self.tr_type = tr_type
        self.power = power
        self.is_big = is_big
        self.tr_code = tr_code
        self.monster_id = monster_id
        
    def get_small_info(self):
        info =  TreasureType.TreasureEmojies[self.tr_type] + '+' + str(self.power)
        if not self.rc_type is None:
            info = info + ' [' + RaceClassType.CREmojies[self.rc_type] + ']'
        if self.is_big:
            info = info + ' БОЛЬШАЯ'
        info = info + ' - ' + self.name + '(' + self.tr_code + ')'
        return info

class Monster:
    def __init__(self, id, fightcode, defeatcode, lvl, lvlcodes, bonuses):
        self.id = id
        self.monster_fightcode = fightcode
        self.monster_defeatcode = defeatcode
        self.monster_lvlcodes = lvlcodes
        self.monster_lvl = lvl
        self.bonuses_to_mnch = bonuses
        
class Munchkin:
    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.current_lvl = 1
        self.current_money = 0
        self.one_shot_bonus = 0
        self.current_race = RaceClassType.Human
        self.current_class = RaceClassType.NoClass
        self.used_trs = []
        self.used_levels_codes = []
        self.used_curse_codes = []
        self.used_money_codes = []
        self.used_one_shot_codes = []
        self.killed_monsters = []
        self.use_three_hands = False
        self.race_change_datetime = None
        self.class_change_datetime = None
        self.monster_fight_datetime = None
        self.shield_datetime = None
        self.chicken_datetime = None
        self.stat_datetime = None
        self.applied_curses = []

    def get_total_power(self):
        dt_now = datetime.now()
        total_power = self.current_lvl + self.one_shot_bonus
        for tr in self.used_trs:
            total_power = total_power + tr.power
        for curse in self.applied_curses:
            if curse > dt_now:
                total_power = total_power - 1
        return total_power
    
    @staticmethod
    def converter_datetime_to_json(o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%m/%d/%Y, %H:%M:%S")
        return o.__dict__()
        
    def save(self):
        return {
            'id': self.id,
            'name': self.name,
            'current_lvl': self.current_lvl,
            'current_money': self.current_money,
            'current_race': self.current_race,
            'current_class': self.current_class,
            'used_trs': [i.tr_code for i in self.used_trs],
            'used_levels_codes': self.used_levels_codes,
            'used_curse_codes': self.used_curse_codes,
            'used_money_codes': self.used_money_codes,
            'killed_monsters': self.killed_monsters,
            'use_three_hands': self.use_three_hands,
            'race_change_datetime': self.race_change_datetime.strftime("%m/%d/%Y, %H:%M:%S"),
            'class_change_datetime': self.class_change_datetime.strftime("%m/%d/%Y, %H:%M:%S"),
            'monster_fight_datetime': self.monster_fight_datetime.strftime("%m/%d/%Y, %H:%M:%S"),
            'shield_datetime': self.shield_datetime.strftime("%m/%d/%Y, %H:%M:%S"),
            'chicken_datetime': self.chicken_datetime.strftime("%m/%d/%Y, %H:%M:%S"),
            'stat_datetime': self.stat_datetime.strftime("%m/%d/%Y, %H:%M:%S"),
            'used_one_shot_codes': self.used_one_shot_codes,
            'one_shot_bonus': self.one_shot_bonus,
            'applied_curses': [i.strftime("%m/%d/%Y, %H:%M:%S") for i in self.applied_curses],
            }

    def load(self, input):
         self.name = input['name']
         self.current_lvl = input['current_lvl']
         self.current_money = input['current_money']
         self.current_race = input['current_race']
         self.current_class = input['current_class']
         self.used_trs = [GlobalInfo.c_treasure_codes[i] for i in input['used_trs']]
         self.used_levels_codes = input['used_levels_codes']
         self.used_curse_codes = input['used_curse_codes']
         self.used_money_codes = input['used_money_codes']
         self.killed_monsters = input['killed_monsters']
         self.use_three_hands = input['use_three_hands']
         self.race_change_datetime = datetime.strptime(input['race_change_datetime'], "%m/%d/%Y, %H:%M:%S")
         self.class_change_datetime = datetime.strptime(input['class_change_datetime'], "%m/%d/%Y, %H:%M:%S")
         self.monster_fight_datetime = datetime.strptime(input['monster_fight_datetime'], "%m/%d/%Y, %H:%M:%S")
         self.shield_datetime = datetime.strptime(input['shield_datetime'], "%m/%d/%Y, %H:%M:%S")
         self.chicken_datetime = datetime.strptime(input['chicken_datetime'], "%m/%d/%Y, %H:%M:%S")
         self.stat_datetime = datetime.strptime(input['stat_datetime'], "%m/%d/%Y, %H:%M:%S")
         self.used_one_shot_codes = input['used_one_shot_codes']
         self.one_shot_bonus = input['one_shot_bonus']
         self.applied_curses = [datetime.strptime(i, "%m/%d/%Y, %H:%M:%S") for i in input['applied_curses']]

class GlobalInfo:
    logs = []
    autobackup_enabled = False#todo:return to true
    final_code = 'imfinalcode19482730'
    munchkin_count = 3
    munchkins_logins = {
        'admin': Munchkin('admin', 0),
        'com1': Munchkin('otwt', 1),
        'com2': Munchkin('div', 2),
        'com3': Munchkin('mars', 3),
        }
    registered_players = {}#.chat.id-key,Munchkin-value
    monsters = [
        Monster(1,'мор4','1539',1,['л5321'],{}),
        Monster(2,'муп2','3661',2,['л7669'],{}),
        Monster(3,'мма3','2204',2,['л5656'],{}),
        Monster(4,'мпк6','7652',4,['л3218'],{
            RaceClassType.Wizard: 2
            }),
        Monster(5,'мте4','4071',5,['л4231'],{}),
        Monster(6,'моа8','8029',6,['л0331'],{}),
        Monster(7,'мсу1','5676',8,['л3580'],{
            RaceClassType.Warrior: 1
            }),
        Monster(8,'мех5','3063',9,['л8988'],{
            RaceClassType.Wizard: 1
            }),
        Monster(9,'мхм4','4753',10,['л4815'],{}),
        Monster(10,'мкб7','9982',12,['л1251'],{}),
        Monster(11,'мвя3','1914',13,['л5246'],{
            RaceClassType.Elf: -5
            }),
        Monster(12,'мпо2','3777',15,['л7313'],{
            RaceClassType.Elf: 1,
            RaceClassType.Warrior: 1
            }),
        Monster(13,'мас9','8211',19,['л1181'],{}),
        Monster(14,'мде6','2119',21,['л6369'],{}),
        Monster(15,'мгл2','2183',23,['л2534'],{
            RaceClassType.Warrior: 1
            }),
        ]
    treasures = [
        Treasure(1, 'карнавальная маска', RaceClassType.Wizard, TreasureType.Headgear, 1, False, 'гуп7', 5),#5
        Treasure(2, 'сланцы', RaceClassType.Elf, TreasureType.Footgear, 1, False, 'сан2', 6),#6
        Treasure(3, 'жилетка новичка', RaceClassType.Wizard, TreasureType.Armor, 1, False, 'бор6', 7),#8
        Treasure(4, 'шлем из картона', RaceClassType.Warrior, TreasureType.Headgear, 1, False, 'гус9', 8),#9
        Treasure(5, 'палка', RaceClassType.Warrior, TreasureType.OneHandWeapon, 1, False, 'ора5', 8),#9
        Treasure(6, 'шелковые тапочки', RaceClassType.Wizard, TreasureType.Footgear, 2, False, 'сок7', 9),#10
        Treasure(7, 'длинный лук', RaceClassType.Elf, TreasureType.TwoHandWeapon, 2, True, 'трс3', 9),#10
        Treasure(8, 'бронька', None, TreasureType.Armor, 1, False, 'бас2', 10),#12
        Treasure(9, 'эльфомечик', RaceClassType.Elf, TreasureType.OneHandWeapon, 2, False, 'ому7', 10),#12
        Treasure(10, 'тапки вязаные', None, TreasureType.Footgear, 1, False, 'сыч8', 11),#13
        Treasure(11, 'массивный шлем', RaceClassType.Warrior, TreasureType.Headgear, 2, True, 'гон6', 11),#13
        Treasure(12, 'защитный шлем', None, TreasureType.Headgear, 1, False, 'гав4', 12),#15
        Treasure(13, 'доспех воина', RaceClassType.Warrior, TreasureType.Armor, 2, False, 'бух5', 12),#15
        Treasure(14, 'высокие сапоги', None, TreasureType.Footgear, 2, False, 'сфи4', 13),#19
        Treasure(15, 'божественная тиара', None, TreasureType.Headgear, 2, False, 'гкк2', 13),#19
        Treasure(16, 'великая броня света', RaceClassType.Wizard, TreasureType.Armor, 3, True, 'буа5', 13),#19
        Treasure(17, 'минипосох', RaceClassType.Wizard, TreasureType.OneHandWeapon, 1, False, 'оля2', 14),#21
        Treasure(18, 'нейроботы', RaceClassType.Wizard, TreasureType.Footgear, 3, False, 'сем9', 14),#21
        Treasure(19, 'бронежилет', None, TreasureType.Armor, 2, False, 'бур4', 14),#21
        Treasure(20, 'мегамеч', RaceClassType.Warrior, TreasureType.TwoHandWeapon, 4, True, 'тен3', 15),#23
        Treasure(21, 'леви-кроссы', RaceClassType.Elf, TreasureType.Footgear, 3, False, 'сук2', 15),#23
        Treasure(22, 'крепкие латы', RaceClassType.Warrior, TreasureType.Footgear, 2, False, 'ска5', 15),#23
        ]
    classes = {
        RaceClassType.NoClass: 'ком1',
        RaceClassType.Warrior: 'кан3',
        RaceClassType.Wizard: 'куу7',
        RaceClassType.Thief: 'ком4',
        RaceClassType.Cleric: 'ком5',
        }
    races = {
        RaceClassType.Human: 'раз1',
        RaceClassType.Elf: 'ров9',
        RaceClassType.Halfling: 'раз8',
        RaceClassType.Dwarf: 'раз9',
        }
    curse_codes = [
        'п0000',
        'п0001',
        'п0002',
        'п0003',
        'п0004',
        'п0005',
        'п0006',
        'п0007',
        'п0008',
        'п0009',
        'п0010',
        'п0011',
        'п0012',
        'п0013',
        'п0014',
        'п0015',
        'п0016',
        'п0017',
        'п0018',
        'п0019',
        'п0020',
        'п0021',
        'п0022',
        'п0023',
        'п0024',
        'п0025',
        'п0026',
        'п0027',
        'п0028',
        'п0029',
        'п0030',
        'п0031',
        'п0032',
        'п0033',
        'п0034',
        'п0035',
        'п0036',
        'п0037',
        'п0038',
        'п0039',
        'п0040',
        'п0041',
        'п0042',
        'п0043',
        'п0044',
        'п0045',
        'п0046',
        'п0047',
        'п0048',
        'п0049',
        'п0050',
        'п0051',
        'п0052',
        'п0053',
        'п0054',
        'п0055',
        'п0056',
        'п0057',
        'п0058',
        'п0059',
        'п0060',
        'п0061',
        'п0062',
        'п0063',
        'п0064',
        'п0065',
        'п0066',
        'п0067',
        'п0068',
        'п0069',
        'п0070',
        'п0071',
        'п0072',
        'п0073',
        'п0074',
        'п0075',
        'п0076',
        'п0077',
        'п0078',
        'п0079',
        'п0080',
        'п0081',
        'п0082',
        'п0083',
        'п0084',
        'п0085',
        'п0086',
        'п0087',
        'п0088',
        'п0089',
        'п0090',
        'п0091',
        'п0092',
        'п0093',
        'п0094',
        'п0095',
        'п0096',
        'п0097',
        'п0098',
        'п0099',
        ]
    one_shot_bonus_codes = {
        'ф1111':1,
        'ф1112':1,
        'ф1113':1,
        'ф1114':1,
        'ф1115':1,
        'ф1116':1,
        'ф1117':1,
        'ф1118':1,
        'ф1119':1,
        'ф1120':1,
        'ф1121':1,
        'ф1122':1,
        'ф1123':1,
        'ф1124':1,
        'ф1125':1,
        'ф1126':1,
        'ф1127':1,
        'ф1128':1,
        'ф1129':1,
        'ф1130':1,
        'ф1131':1,
        'ф1132':1,
        'ф1133':1,
        'ф1134':1,
        'ф1135':1,
        'ф1136':1,
        'ф1137':1,
        'ф1138':1,
        'ф1139':1,
        'ф1140':1,
        'ф1141':1,
        'ф1142':1,
        'ф1143':1,
        'ф1144':1,
        'ф1145':1,
        'ф1146':1,
        'ф1147':1,
        'ф1148':1,
        'ф1149':1,
        'ф1150':1,
        'ф1151':1,
        'ф1152':1,
        'ф1153':1,
        'ф1154':1,
        'ф1155':1,
        'ф1156':1,
        'ф1157':1,
        'ф1158':1,
        'ф1159':1,
        'ф1160':1,
        'ф1161':1,
        'ф1162':1,
        'ф1163':1,
        'ф1164':1,
        'ф1165':1,
        'ф1166':1,
        'ф1167':1,
        'ф1168':1,
        'ф1169':1,
        'ф1170':1,
        'ф1171':1,
        'ф1172':1,
        'ф1173':1,
        'ф1174':1,
        'ф1175':1,
        'ф1176':1,
        'ф1177':1,
        'ф1178':1,
        'ф1179':1,
        'ф1180':1,
        'ф1181':1,
        'ф1182':1,
        'ф1183':1,
        'ф1184':1,
        'ф1185':1,
        'ф1186':1,
        'ф1187':1,
        'ф1188':1,
        'ф1189':1,
        'ф1190':1,
        'ф1191':1,
        'ф1192':1,
        'ф1193':1,
        'ф1194':1,
        'ф1195':1,
        'ф1196':1,
        'ф1197':1,
        'ф1198':1,
        'ф1199':1,
        'ф2000':2,
        'ф2001':2,
        'ф2002':2,
        'ф2003':2,
        'ф2004':2,
        'ф2005':2,
        'ф2006':2,
        'ф2007':2,
        'ф2008':2,
        'ф2009':2,
        'ф2010':2,
        'ф2011':2,
        'ф2012':2,
        'ф2013':2,
        'ф2014':2,
        'ф2015':2,
        'ф2016':2,
        'ф2017':2,
        'ф2018':2,
        'ф2019':2,
        }
    money_codes = {
        'г1000':100,
        'г1001':100,
        'г1002':100,
        'г1003':100,
        'г1004':100,
        'г1005':100,
        'г1006':100,
        'г1007':100,
        'г1008':100,
        'г1009':100,
        'г1010':100,
        'г1011':100,
        'г1012':100,
        'г1013':100,
        'г1014':100,
        'г1015':100,
        'г1016':100,
        'г1017':100,
        'г1018':100,
        'г1019':100,
        'г1020':100,
        'г1021':100,
        'г1022':100,
        'г1023':100,
        'г1024':100,
        'г1025':100,
        'г1026':100,
        'г1027':100,
        'г1028':100,
        'г1029':100,
        'г1030':100,
        'г1031':100,
        'г1032':100,
        'г1033':100,
        'г1034':100,
        'г1035':100,
        'г1036':100,
        'г1037':100,
        'г1038':100,
        'г1039':100,
        'г1040':100,
        'г1041':100,
        'г1042':100,
        'г1043':100,
        'г1044':100,
        'г1045':100,
        'г1046':100,
        'г1047':100,
        'г1048':100,
        'г1049':100,
        'г2000':200,
        'г2001':200,
        'г2002':200,
        'г2003':200,
        'г2004':200,
        'г2005':200,
        'г2006':200,
        'г2007':200,
        'г2008':200,
        'г2009':200,
        'г2010':200,
        'г2011':200,
        'г2012':200,
        'г2013':200,
        'г2014':200,
        'г2015':200,
        'г2016':200,
        'г2017':200,
        'г2018':200,
        'г2019':200,
        'г2020':200,
        'г2021':200,
        'г2022':200,
        'г2023':200,
        'г2024':200,
        'г2025':200,
        'г2026':200,
        'г2027':200,
        'г2028':200,
        'г2029':200,
        'г2030':200,
        'г2031':200,
        'г2032':200,
        'г2033':200,
        'г2034':200,
        'г2035':200,
        'г2036':200,
        'г2037':200,
        'г2038':200,
        'г2039':200,
        'г2040':200,
        'г2041':200,
        'г2042':200,
        'г2043':200,
        'г2044':200,
        'г2045':200,
        'г2046':200,
        'г2047':200,
        'г2048':200,
        'г2049':200,
        'г4000':400,
        'г4001':400,
        'г4002':400,
        'г4003':400,
        'г4004':400,
        'г4005':400,
        'г4006':400,
        'г4007':400,
        'г4008':400,
        'г4009':400,
        'г7000':700,
        'г7001':700,
        'г7002':700,
        'г7003':700,
        'г7004':700,
        'г7005':700,
        'г7006':700,
        'г7007':700,
        'г7008':700,
        'г7009':700,
        }
    divine_intervention_code = 'дв01012'
    is_divine_intervention_passed = False
    c_level_codes = {}
    c_monster_fight_codes = {}
    c_class_codes = {}
    c_race_codes = {}
    c_treasure_codes = {}
    c_singlecode_handlers = {}
    c_toteam_handlers = {}
    c_munchkins_by_ids = {}
    c_check_m_by_lvlc = {}
    c_check_m_by_trc = {}

    @staticmethod
    def initialize():
        GlobalInfo.registered_players[-495810366] = GlobalInfo.munchkins_logins['com1']
        GlobalInfo.registered_players[-442872279] = GlobalInfo.munchkins_logins['com2']
        GlobalInfo.registered_players[-456257520] = GlobalInfo.munchkins_logins['com3']
        for monster in GlobalInfo.monsters:
            for lvlcode in monster.monster_lvlcodes:
                GlobalInfo.c_level_codes[lvlcode] = monster
                GlobalInfo.c_singlecode_handlers[lvlcode] = GlobalInfo.simple_text_handler_level
                GlobalInfo.c_check_m_by_lvlc[lvlcode] = monster.id
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
        for curse_code in GlobalInfo.curse_codes:
            GlobalInfo.c_singlecode_handlers[curse_code] = GlobalInfo.simple_text_handler_fail_curse
            GlobalInfo.c_toteam_handlers[curse_code] = GlobalInfo.simple_text_handler_curse
        for one_shot_bonus_code in GlobalInfo.one_shot_bonus_codes:
            GlobalInfo.c_singlecode_handlers[one_shot_bonus_code] = GlobalInfo.simple_text_handler_oneshot
            GlobalInfo.c_toteam_handlers[one_shot_bonus_code] = GlobalInfo.simple_text_handler_oneshotpenalty
        for money_code in GlobalInfo.money_codes:
            GlobalInfo.c_singlecode_handlers[money_code] = GlobalInfo.simple_text_handler_money
        for treasure in GlobalInfo.treasures:
            GlobalInfo.c_treasure_codes[treasure.tr_code] = treasure
            GlobalInfo.c_check_m_by_trc[treasure.tr_code] = treasure.monster_id
        dt_now = datetime.now()
        for login in GlobalInfo.munchkins_logins:
            munchkin = GlobalInfo.munchkins_logins[login]
            munchkin.race_change_datetime = dt_now
            munchkin.class_change_datetime = dt_now
            munchkin.monster_fight_datetime = dt_now
            munchkin.chicken_datetime = dt_now
            munchkin.shield_datetime = dt_now
            munchkin.stat_datetime = dt_now
            GlobalInfo.c_munchkins_by_ids[munchkin.id] = munchkin
        GlobalInfo.munchkins_logins['admin'].current_lvl = 999

    @staticmethod
    def add_log_row(name, chatid, text, flag):
        GlobalInfo.logs.append({
            'datetime': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            'name': name,
            'chatid': chatid,
            'text': text,
            'flag': flag,
            })

    #single or to team handlers ------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def simple_text_handler_level(munchkin, input_text):
        if not input_text in GlobalInfo.c_level_codes:
            raise Exception('орг косяк, сообщите ему об этом( @sanjjjjok )')
        if input_text in munchkin.used_levels_codes:
            return Result(1, 'вы уже получили уровень по этому коду')
        munchkin.used_levels_codes.append(input_text)
        munchkin.current_lvl = munchkin.current_lvl + 1
        if munchkin.current_lvl == 25:
            return Result(0, 'Поздравляю! Вы закончили игру. Код закрытия движка: ' + GlobalInfo.final_code)
        return Result(0, 'Ура! Ваш новый уровень: ' + str(munchkin.current_lvl) + '. Не забудьте ввести этот код ещё и в движке.')

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
            block_msg = 'следующая смена класса возможна через ' + GlobalInfo.sec_to_str(dt_diff)
            return Result(2, block_msg)
        if munchkin.current_class==RaceClassType.Wizard and new_class==RaceClassType.NoClass and len(munchkin.applied_curses)>0:
            munchkin.applied_curses = munchkin.applied_curses[:-1]
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
            block_msg = 'следующая смена расы возможна через ' + GlobalInfo.sec_to_str(dt_diff)
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
        if munchkin.chicken_datetime > dt_now:
            dt_ck_diff = (munchkin.chicken_datetime - dt_now).total_seconds()
            block_msg = 'вас превратили в курицу, битва с монстром невозможна\n' + Emojies.Result2 + GlobalInfo.sec_to_str(dt_ck_diff)
            return Result(3, block_msg)
        if munchkin.monster_fight_datetime > dt_now:
            dt_diff = (munchkin.monster_fight_datetime - dt_now).total_seconds()
            block_msg = 'следующая битва возможна через ' + GlobalInfo.sec_to_str(dt_diff)
            return Result(2, block_msg)
        monster = GlobalInfo.c_monster_fight_codes[input_text]
        if monster.id in munchkin.killed_monsters:
            return Result(1, 'вы уже побеждали монстра, код побежденного монстра:' + monster.monster_defeatcode)
        total_power = munchkin.get_total_power()
        munchkin.one_shot_bonus = 0
        for cr_bonus in monster.bonuses_to_mnch:
            if munchkin.current_class == cr_bonus or munchkin.current_race == cr_bonus:
                total_power = total_power + monster.bonuses_to_mnch[cr_bonus]
        if total_power > monster.monster_lvl or (total_power == monster.monster_lvl and munchkin.current_class == RaceClassType.Warrior):
            munchkin.killed_monsters.append(monster.id)
            return Result(0, 'Ура! Монстр победжен! Код побежденного монстра:' + monster.monster_defeatcode)
        munchkin.monster_fight_datetime = dt_now + timedelta(0,5)
        return Result(1, 'вы не смогли победить монстра =(')
    
    @staticmethod
    def simple_text_handler_oneshot(munchkin, input_text):
        if not input_text in GlobalInfo.one_shot_bonus_codes:
            raise Exception('орг косяк, сообщите ему об этом( @sanjjjjok )')
        if input_text in munchkin.used_one_shot_codes:
            return Result(1, 'вы уже использовали этот код')
        munchkin.used_one_shot_codes.append(input_text)
        added_bonus = GlobalInfo.one_shot_bonus_codes[input_text]
        munchkin.one_shot_bonus = munchkin.one_shot_bonus + added_bonus
        return Result(0, 'Ура! Вы получили +' + str(added_bonus) + ' единиц силы в следующем бою')
    
    @staticmethod
    def simple_text_handler_money(munchkin, input_text):
        if not input_text in GlobalInfo.money_codes:
            raise Exception('орг косяк, сообщите ему об этом( @sanjjjjok )')
        if input_text in munchkin.used_money_codes:
            return Result(1, 'вы уже использовали этот код')
        munchkin.used_money_codes.append(input_text)
        added_money = GlobalInfo.money_codes[input_text]
        munchkin.current_money = munchkin.current_money + added_money
        return Result(0, 'Ура! Вы получили ' + str(added_money) + ' голды')

    @staticmethod
    def simple_text_handler_fail_curse(munchkin, input_text):
        if not input_text in GlobalInfo.curse_codes:
            raise Exception('орг косяк, сообщите ему об этом( @sanjjjjok )')
        return Result(1, 'вы не ввели команду, к которой применить проклятие')
    
    @staticmethod
    def simple_text_handler_oneshotpenalty(munchkin, input_text, munch_id_str):
        if not input_text in GlobalInfo.one_shot_bonus_codes:
            raise Exception('орг косяк, сообщите ему об этом( @sanjjjjok )')
        if not GlobalInfo.is_int(munch_id_str):
            return Result(1, 'неверный номер манчкина: ' + munch_id_str)
        munch_id = int(munch_id_str)
        if munch_id < 1 or munch_id > GlobalInfo.munchkin_count:
            return Result(1, 'неверный номер манчкина: ' + munch_id_str)
        if munch_id == munchkin.id:
            return Result(1, 'нельзя применить штраф на себя')
        if input_text in munchkin.used_one_shot_codes:
            return Result(1, 'вы уже использовали этот код')
        munchkin.used_one_shot_codes.append(input_text)
        added_penalty = GlobalInfo.one_shot_bonus_codes[input_text]
        target_muhcnkin = GlobalInfo.c_munchkins_by_ids[munch_id]
        target_muhcnkin.one_shot_bonus = target_muhcnkin.one_shot_bonus - added_penalty
        return Result(0, 'Ура! Манчкин ' + target_muhcnkin.name + ' получил -' + str(added_penalty) + ' единиц силы в следующем бою', 
                      target_muhcnkin, 'Вы получили -' + str(added_penalty) + ' единиц силы в следующем бою от манчкина ' + munchkin.name)

    @staticmethod
    def simple_text_handler_curse(munchkin, input_text, munch_id_str):
        if not input_text in GlobalInfo.curse_codes:
            raise Exception('орг косяк, сообщите ему об этом( @sanjjjjok )')
        if not GlobalInfo.is_int(munch_id_str):
            return Result(1, 'неверный номер манчкина: ' + munch_id_str)
        munch_id = int(munch_id_str)
        if munch_id < 1 or munch_id > GlobalInfo.munchkin_count:
            return Result(1, 'неверный номер манчкина: ' + munch_id_str)
        if munch_id == munchkin.id:
            return Result(1, 'нельзя применить проклятие на себя')
        if input_text in munchkin.used_curse_codes:
            return Result(1, 'вы уже использовали этот код')
        munchkin.used_curse_codes.append(input_text)
        target_muhcnkin = GlobalInfo.c_munchkins_by_ids[munch_id]
        dt_now = datetime.now()
        if target_muhcnkin.shield_datetime > dt_now:
            return Result(1, 'у манчкина ' + target_muhcnkin.name + ' активирована защита от проклятий, проклятие сгорает', 
                      target_muhcnkin, 'Манчкин ' + munchkin.name + ' попытался кинуть на вас проклятие')
        curse_time = dt_now + timedelta(0, 1800)
        target_muhcnkin.applied_curses.append(curse_time)
        return Result(0, 'Ура! На манчкина ' + target_muhcnkin.name + ' сработало проклятие', 
                      target_muhcnkin, 'Вы получили проклятие от манчкина ' + munchkin.name)

    #single or to team handlers ------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def do_beautiful_with_treasures(munchkin, treasure_codes):
        input_treasures = []
        for tr_code in treasure_codes:
            if not tr_code in GlobalInfo.c_treasure_codes:
                return Result(1, 'не существует такого кода: ' + tr_code)
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
    def is_int(input_str):
        try:
            temp = int(input_str)
            return True
        except:
            return False

    @staticmethod
    def sec_to_str(amount):
        return str(round(amount // 60)) + 'мин ' + str(round(amount % 60)) + 'с'

    @staticmethod
    def split_and_remove_empty(text) -> []:
        arr = text.split(' ')
        return [i for i in arr if i]
    
    @staticmethod
    def backup():
        output_dict = {
            'datetime': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            'is_divine_intervention_passed': GlobalInfo.is_divine_intervention_passed
            }
        for munch_id in GlobalInfo.c_munchkins_by_ids:
            munchkin = GlobalInfo.c_munchkins_by_ids[munch_id]
            output_dict[munch_id] = munchkin.save()
        m_str = json.dumps(output_dict, ensure_ascii=False, indent=2)#todo:remove indent
        file = open('123.json', 'w', encoding='utf-8')
        file.truncate(0)
        file.write(m_str)
        file.close()

    @staticmethod
    def restore(input_data):
        GlobalInfo.is_divine_intervention_passed = input_data['is_divine_intervention_passed']
        for munch_id in GlobalInfo.c_munchkins_by_ids:
            munchkin = GlobalInfo.c_munchkins_by_ids[munch_id]
            if not str(munch_id) in input_data:
                return 'не удалось найти в файле id=' + str(munch_id)
            munchkin.load(input_data[str(munch_id)])
        return None