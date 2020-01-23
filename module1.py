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
    #ReloadSession = 'reconnect'
    #EnAuth = 'en'
    #LoadImgs = 'load'
    #ImgReq = 'find'
    #PrintWords = 'print'
    #ImgsAction = 'do'

class ModeType(enum.Enum):
    Disabled = 0
    Special = 1
    Olymp = 2
    Gibrid = 3
    Meta = 4
    Logo = 5
    Anag = 6
    Plus = 7
    Matr = 8
    Bruk = 9

    def next(self):
        val = self.value + 1
        if (val == ModeType.get_modes_count()):
            val = 0
        return ModeType(val)

    def prev(self):
        val = self.value - 1
        if (val == -1):
            val = ModeType.get_modes_count() - 1
        return ModeType(val)

    @staticmethod
    def get_modes_count():
        return 10

    @staticmethod
    def get_well_known_mode_types():
        return {
            ModeType.Disabled: ['disabled', 'выключено'],
            ModeType.Special: ['special', 'специальный'],
            ModeType.Olymp: ['olymp', 'олимпийка'],
            ModeType.Gibrid: ['gibrid', 'гибрид'],
            ModeType.Meta: ['meta', 'метаграмма'],
            ModeType.Logo: ['logo', 'логогриф'],
            ModeType.Anag: ['anag', 'анаграмма'],
            ModeType.Plus: ['plus', 'плюсограмма'],
            ModeType.Matr: ['matr', 'матрица'],
            ModeType.Bruk: ['bruk', 'брюква']
            }

    @staticmethod
    def get_modes_by_alias(input):
        result = []
        input_alias = input.lower()
        mapper = ModeType.get_well_known_mode_types()
        for mode in mapper.keys():
            for alias in mapper[mode]:
                if alias.startswith(input_alias):
                    result.append(mode)
                    break
        return result

class GlobalHolder:
    def __init__(self):
        self.settings_by_id = {}
        self.modes_actions = {
            ModeType.Disabled: ['disabled', 'выключено'],
            ModeType.Special: ['special', 'специальный'],
            ModeType.Olymp: ['olymp', 'олимпийка'],
            ModeType.Gibrid: ['gibrid', 'гибрид'],
            ModeType.Meta: ['meta', 'метаграмма'],
            ModeType.Logo: ['logo', 'логогриф'],
            ModeType.Anag: ['anag', 'анаграмма'],
            ModeType.Plus: ['plus', 'плюсограмма'],
            ModeType.Matr: ['matr', 'матрица'],
            ModeType.Bruk: ['bruk', 'брюква']
            }

    def add(self, id):
        self.settings_by_id[id] = Settings()

    def get(self, id):
        return self.settings_by_id[id]

class Settings:
    def __init__(self):
        self.current_mode = ModeType.Disabled
        self.session = requests.session()
        self.game_imgs = []
        self.yandex_tags_filtered = []
        self.yandex_tags_all = []
        self.not_found_imgs = []

    def next_mode(self):
        self.current_mode = self.current_mode.next()
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

class WordHandlers:
    @staticmethod
    def default_word_handler(value) -> []:
        return [value]

    @staticmethod
    def get_associations_word_handler(value) -> []:
        if value.startswith('!') or value.startswith('%'):
            return [ value[1:] ]
        result = Utils.get_associations(value)
        result.append(value)
        return result

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
    def get_unique(arr):
        return list(dict.fromkeys(arr))
    
    @staticmethod
    def do_actions(text, count, values_handlers, word_handler) -> Result:
        input_result = Utils.default_parse_to_input(text, count, word_handler)
        if not input_result.is_success:
            return input_result
        result = []
        for values_handler in values_handlers:
            union = values_handler(input_result.values)
            unique_union = Utils.get_unique(union)
            result.append(str(len(unique_union)))
            result.append('\n'.join(unique_union))
        return Result.success(result)

    @staticmethod
    def default_parse_to_input(text, count = -1, word_handler_method = None) -> []:
        result = []
        findall_mode = False
        text = text.lower()
        if text[0]=='$':
            text = text[1:]
            findall_mode = True
        if len(text)==0:
            return Result.failed('too short message')
        input = text.strip().split('.')
        if len(input)!=count and count!=-1:
            return Result.failed('invalid groups count, need {0} groups'.format(count))

        if findall_mode:
            for input_item in input:
                result.append(re.findall(r"[\w']+", input_item))
            return Result.success(result)

        if word_handler_method is None:
            word_handler_method = WordHandlers.default_word_handler
        for input_item in input:
            sub_result = input_item.strip().split(',')
            sub_result_parsed = []
            for word in sub_result:
                handled_words = word_handler_method(word.strip())
                sub_result_parsed.extend(handled_words)
            result.append(sub_result_parsed)
        return Result.success(result)