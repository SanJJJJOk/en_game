import enum
import requests

class ModeType(enum.Enum):
    Disabled = 0
    Special = 1
    Olymp = 2
    Gibrid = 3
    Meta = 4
    Logo = 5

    def next(self):
        val = self.value + 1
        if (val == 6):
            val = 0
        return ModeType(val)

    def prev(self):
        val = self.value - 1
        if (val == -1):
            val = 5
        return ModeType(val)

    @staticmethod
    def get_well_known_mode_types():
        return {
            ModeType.Disabled: ['disabled', 'выключено'],
            ModeType.Special: ['special', 'специальный'],
            ModeType.Olymp: ['olymp', 'олимпийка'],
            ModeType.Gibrid: ['gibrid', 'гибриды'],
            ModeType.Meta: ['meta', 'метаграммы'],
            ModeType.Logo: ['logo', 'логогрифы']
            }

    @staticmethod
    def get_modes_by_alias(input):
        result = []
        input_alias = input.lower()
        mapper = ModeType.get_well_known_mode_types()
        for mode in mapper.keys():
            for alias in mapper[mode]:
                if alias.startswith(prefix):
                    result.append(mode)
                    break
        return result

class SettingsHolder:
    def __init__(self):
        self.settings_by_id = {}

    def add(self, id):
        self.settings_by_id[id] = Settings()

    def get(self, id):
        return self.settings_by_id[id]

class Settings:
    def __init__(self):
        self.current_mode = ModeType.Disabled
        self.session = requests.session()

    def next_mode(self):
        self.current_mode = self.current_mode.next()
        return self.current_mode