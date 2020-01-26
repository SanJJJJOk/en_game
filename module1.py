import enum
import requests
import re
from urllib import request, parse
import json

class TgCommands():
    Olymp = 'o'
    Gibrid = 'g'
    Meta = 'm'
    Logo = 'l'
    SwitchMode = 'mode'
    Test = 'test'

class ModeType():
    Disabled = 0
    Special = 1
    Olymp = 2
    Gibrid3 = 3
    Gibrid4 = 4
    Meta = 5
    Logo = 6
    Anag = 7
    Plus = 8
    Matr = 9
    Bruk = 10
    Combined = 11
    
    modes_count = 12
    aliases_by_modes = {
        Disabled: ['disabled', 'выключено'],
        Special: ['special', 'специальный'],
        Olymp: ['olymp', 'олимпийка'],
        Gibrid3: ['gibrid3', 'гибрид3', 'g3', 'г3'],
        Gibrid4: ['gibrid4', 'гибрид4', 'g4', 'г4'],
        Meta: ['meta', 'метаграмма'],
        Logo: ['logo', 'логогриф'],
        Anag: ['anag', 'анаграмма'],
        Plus: ['plus', 'плюсограмма'],
        Matr: ['matr', 'матрица'],
        Bruk: ['bruk', 'брюква'],
        Combined: ['combined', 'комбинированный', 'all']
        }

    @staticmethod
    def get_modes_by_alias(input) -> []:
        result = []
        input_alias = input.lower()
        mapper = ModeType.aliases_by_modes
        for mode in mapper.keys():
            for alias in mapper[mode]:
                if alias.startswith(input_alias):
                    result.append(mode)
                    break
        return result

class GlobalHolder:
    def __init__(self):
        self.settings_by_id = {}
        self.default_text_handlers_by_modes = {
                ModeType.Disabled: None,
                ModeType.Special: None,
                ModeType.Olymp: OlympModeDefaultTextHandler(),
                ModeType.Gibrid3: None,
                ModeType.Gibrid4: None,
                ModeType.Meta: None,
                ModeType.Logo: None,
                ModeType.Anag: None,
                ModeType.Plus: None,
                ModeType.Matr: None,
                ModeType.Bruk: None,
                ModeType.Combined: None
                }

    def add(self, id):
        self.settings_by_id[id] = Settings()

    def get(self, id):
        return self.settings_by_id[id]

class Settings:
    def __init__(self):
        self.current_mode = ModeType.Disabled

    def next_mode(self) -> int:
        self.current_mode = self.current_mode + 1
        if (self.current_mode == ModeType.modes_count):
            self.current_mode = 0
        return self.current_mode

class Result:
    def __init__(self, is_success, message, values):
        self.is_success = is_success
        self.message = message
        self.values = values
        
    @classmethod
    def success(cls, values):
        return cls(True, "", values)

    @classmethod
    def failed(cls, message):
        return cls(False, message, [])


class Utils:
    @staticmethod
    def get_associations(input_word) -> []:
        data = parse.urlencode({
            'word':input_word,
            'back':False,
            'max_count':0
            }).encode()
        req =  request.Request('https://sociation.org/ajax/word_associations/', data=data)
        resp = request.urlopen(req)
        json_resp = json.load(resp)
        if not 'associations' in json_resp:
            return []
        associations = json_resp['associations']
        return [item['name'] for item in associations]

    @staticmethod
    def get_unique(arr) -> []:
        return list(dict.fromkeys(arr))
    
    @staticmethod
    def simple_parse_to_input(text, count = -1) -> Result:
        result = []
        findall = False
        text = text.strip().lower()
        if text[0]=='$':
            text = text[1:]
            findall = True

        if len(text)==0:
            return Result.failed('too short message')
        input = text.strip().split('.')
        if len(input)!=count and count!=-1:
            return Result.failed('invalid groups count, need {0} groups'.format(count))

        if findall:
            result = [ re.findall(r"[\w']+", input_item) for input_item in input ]
        else:
            result = [ Utils.simple_parse_to_words(input_item) for input_item in input ]

        return Result.success(result)

    @staticmethod
    def simple_parse_to_words(text) -> []:
        input = text.strip().split(',')
        result = []
        for input_item in input:
            correct_word = input_item.strip()
            if correct_word.startswith('!') or correct_word.startswith('%'):
                correct_word = correct_word[1:]
            else:
                ass = Utils.get_associations(correct_word)
                result.extend(ass)
            result.append(correct_word)
        return result

class ValuesHandlers:
    @staticmethod
    def dummy_values_handler(values):
        return values
    
    @staticmethod
    def olymp_values_handler(values):
        return list(set(values[0]).intersection(values[1]))
    
    @staticmethod
    def gibrid_3_values_handler(values):
        union = []
        first = values[0]
        second = values[1]
        for i in first:
            for j in second:
                if len(i)<4 and len(j)<4:
                    continue
                if i[-3:] == j[0:3]:
                    if not j + '-' + i in union:
                        union.append(i + '-' + j)
                if i[0:3] == j[-3:]:
                    if not i + '-' + j in union:
                        union.append(j + '-' + i)
        return union
    
    @staticmethod
    def gibrid_4_values_handler(values):
        union = []
        first = values[0]
        second = values[1]
        for i in first:
            for j in second:
                if len(i)<5 and len(j)<5:
                    continue
                if i[-4:] == j[0:4]:
                    if not j + '-' + i in union:
                        union.append(i + '-' + j)
                if i[0:4] == j[-4:]:
                    if not i + '-' + j in union:
                        union.append(j + '-' + i)
        return union

class BaseSimpleModeDefaultTextHandler:
    def __init__(self):
        self.count = -1
        self.values_handler = ValuesHandlers.dummy_values_handler

    def do_action(self, text) -> Result:
        input_result = Utils.simple_parse_to_input(text, self.count)
        if not input_result.is_success:
            return input_result
        
        union = self.values_handler(input_result.values)
        unique_union = Utils.get_unique(union)
        values = [ str(len(unique_union)), '\n'.join(unique_union) ]
        return Result.success(values)

class OlympModeDefaultTextHandler(BaseSimpleModeDefaultTextHandler):
    def __init__(self):
        super().__init__()
        self.count = 2
        self.values_handler = ValuesHandlers.olymp_values_handler