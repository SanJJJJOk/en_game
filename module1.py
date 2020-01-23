import enum
import requests

class TgCommands():
    ReloadSession = 'reconnect'
    EnAuth = 'en'
    LoadImgs = 'load'
    ImgReq = 'find'
    PrintWords = 'print'
    ImgsAction = 'do'
    Olymp = 'o'
    Gibrid = 'g'
    Meta = 'm'
    Logo = 'l'
    SwitchMode = 'mode'
    Test = 'test'

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
    def __init__(self, is_success, message, value):
        self.is_success = is_success
        self.message = message
        self.value = value
        
    @classmethod
    def success(cls, value):
        return cls(True, "", value)

    @classmethod
    def failed(cls, message):
        return cls(False, message, [])

class ParseHelper:
    def __init__(self):
        pass

    @staticmethod
    def simple_parse_to_input(text, count):
        if text[0]=='$':
            parsed = special_parse(input_text[1:])
            output_messages = do_special_search(parsed[0], parsed[1], [mode])
            for msg in output_messages:
                print_long(update, msg)
            return