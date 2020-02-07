import enum
import requests
import re
from urllib import request, parse
import json
from CubraDefinition import *
from RussianWords import *
import random

class TgCommands():
    SwitchMode = 'mode'
    Test = 'test'
    Help = 'help'
    Modes = 'modes'
    Load = 'load'

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
    Scepka = 9
    Matr = 10
    Bruk = 11
    Cubra = 12
    Combined = 13
    
    modes_count = 14
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
        Scepka: ['scepka', 'сцепка'],
        Matr: ['matr', 'матрица'],
        Bruk: ['bruk', 'брюква'],
        Cubra: ['cubra', 'кубрая'],
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
                ModeType.Special: SpecialModeDefaultTextHandler(),
                ModeType.Olymp: OlympModeDefaultTextHandler(),
                ModeType.Gibrid3: Gibrid3ModeDefaultTextHandler(),
                ModeType.Gibrid4: Gibrid4ModeDefaultTextHandler(),
                ModeType.Meta: MetaModeDefaultTextHandler(),
                ModeType.Logo: LogoModeDefaultTextHandler(),
                ModeType.Anag: AnagModeDefaultTextHandler(),
                ModeType.Plus: PlusModeDefaultTextHandler(),
                ModeType.Scepka: ScepkaModeDefaultTextHandler(),
                ModeType.Matr: MatrModeDefaultTextHandler(),
                ModeType.Bruk: BrukModeDefaultTextHandler(),
                ModeType.Cubra: CubraModeDefaultTextHandler(),
                ModeType.Combined: CombinedModeDefaultTextHandler()
                }

    def add(self, id):
        self.settings_by_id[id] = Settings()

    def get(self, id):
        return self.settings_by_id[id]

class Settings:
    def __init__(self):
        self.current_mode = ModeType.Disabled
        self.mem_values = None
        self.mem_mode = ModeType.Disabled

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
    def remove_empty(arr) -> []:
        return [i for i in arr if i]
    
    @staticmethod
    def simple_parse_to_input(text, count = -1) -> Result:
        result = []
        findall = False
        text = text.strip().lower()
        if text.startswith('$'):
            text = text[1:].strip()
            findall = True

        if len(text)==0:
            return Result.failed('too short message')
        input = text.split('.')

        if findall:
            if len(input)>2:
                return Result.failed('invalid groups count, need less than 3 groups')
            sub_result = [ re.findall(r"[\w']+", input_item) for input_item in input ]
            unique_sub_result = [ Utils.get_unique(sub_res_item) for sub_res_item in sub_result]
            if len(input)==1:
                for i in range(count):
                    result.append(unique_sub_result[0])
            else:
                full_sub_result = unique_sub_result[0]
                full_sub_result.extend(unique_sub_result[1])
                result.append(full_sub_result)
                for i in range(count - 1):
                    result.append(unique_sub_result[1])
        else:
            if len(input)!=count and count!=-1:
                return Result.failed('invalid groups count, need {0} groups'.format(count))
            result = [ Utils.simple_parse_to_words(input_item) for input_item in input ]

        return Result.success(result)

    @staticmethod
    def simple_parse_to_words(text) -> []:
        input = text.strip().split(',')
        result = []
        for input_item in input:
            correct_word = input_item.strip()
            if correct_word.startswith('!') or correct_word.startswith('%'):
                correct_word = correct_word[1:].strip()
            else:
                ass = Utils.get_associations(correct_word)
                result.extend(ass)
            result.append(correct_word)
        return Utils.get_unique(result)

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

    @staticmethod
    def meta_values_handler(values):
        union = []
        first = values[0]
        second = values[1]
        for word1 in first:
            for word2 in second:
                if len(word1) != len(word2):
                    continue
                counter = 0
                for i in range(0, len(word1)):
                    if word1[i]!=word2[i]:
                        counter+=1
                if counter != 1:
                    continue
                if word2 + '-' + word1 in union:
                    continue
                union.append(word1 + '-' + word2)
        return union
    
    @staticmethod
    def logo_values_handler(values):
        union = []
        first = values[0]
        second = values[1]
        for word1 in first:
            for word2 in second:
                long_word = ''
                short_word = ''
                if len(word1) == len(word2) + 1:
                    long_word = word1
                    short_word = word2
                else:
                    if len(word2) == len(word1) + 1:
                        long_word = word2
                        short_word = word1
                    else:
                        continue
                diff_index = 0
                for i in range(0, len(short_word)):
                    if long_word[i]!=short_word[i]:
                        diff_index = i
                        break
                for i in range(diff_index, len(short_word)):
                    if long_word[i + 1]!=short_word[i]:
                        diff_index = -1
                        break
                if diff_index==-1 and not long_word.startswith(short_word):
                    continue
                if word2 + '-' + word1 in union:
                    continue
                union.append(word1 + '-' + word2)
        return union
        
    @staticmethod
    def bruk_values_handler(values):
        union = []
        first = values[0]
        second = values[1]
        for word1 in first:
            for word2 in second:
                if len(word1)==1 or len(word2)==1:
                    continue
                long_word = ''
                short_word = ''
                if len(word1) == len(word2) + 1:
                    long_word = word1
                    short_word = word2
                else:
                    if len(word2) == len(word1) + 1:
                        long_word = word2
                        short_word = word1
                    else:
                        continue
                diff_index = 0
                for i in range(0, len(short_word)):
                    if long_word[i]!=short_word[i]:
                        diff_index = i
                        break
                diff_index+=1
                if diff_index<len(short_word):
                    for i in range(diff_index, len(short_word)):
                        if long_word[i + 1]!=short_word[i]:
                            diff_index = -1
                            break
                if diff_index==-1 and not long_word.startswith(short_word[:-1]):
                    continue
                if word2 + '-' + word1 in union:
                    continue
                union.append(word1 + '-' + word2)
        return union

    @staticmethod
    def anag_values_handler(values):
        union = []
        first = values[0]
        second = values[1]
        for i in first:
            for j in second:
                if i==j or len(i)!=len(j):
                    continue
                list1 = list(i)
                list2 = list(j)
                list1.sort()
                list2.sort()
                if list1 != list2:
                    continue
                if j + '-' + i in union:
                    continue
                union.append(i + '-' + j)
        return union
        
    @staticmethod
    def plus_values_handler(values):
        union = []
        first = values[0]
        second = values[1]
        for word1 in first:
            for word2 in second:
                long_word = ''
                short_word = ''
                if len(word1) == len(word2) + 1:
                    long_word = word1
                    short_word = word2
                else:
                    if len(word2) == len(word1) + 1:
                        long_word = word2
                        short_word = word1
                    else:
                        continue
                long_list = list(long_word)
                short_list = list(short_word)
                long_list.sort()
                short_list.sort()
                diff_index = -2
                for i in range(0, len(short_list)):
                    if long_list[i]!=short_list[i]:
                        diff_index = i
                        break
                if diff_index==-2:
                    diff_index = -1
                else:
                    for i in range(diff_index, len(short_list)):
                        if long_list[i + 1]!=short_list[i]:
                            diff_index = -2
                            break
                if diff_index==-2:
                    continue
                if long_list[diff_index] + ': ' + word2 + '-' + word1 in union:
                    continue
                union.append(long_list[diff_index] + ': ' + word1 + '-' + word2)
        union.sort()
        return union

        
    @staticmethod
    def scepka_values_handler(values):
        union = []
        first = values[0]
        second = values[1]
        for word1 in first:
            for word2 in second:
                if word1 + word2 in RussianWords.data:
                    scepka = word1 + '+' + word2
                    if not scepka in union:
                        union.append(scepka)
                if word2 + word1 in RussianWords.data:
                    scepka = word2 + '+' + word1
                    if not scepka in union:
                        union.append(scepka)
        return union

    @staticmethod
    def matr_values_handler(values):
        union = []
        first = values[0]
        second = values[1]
        third = values[2]
        for i in first:
            for j in second:
                if i==j:
                    continue
                for index in range(0, len(i)-2):
                    the_matr = i[index:index+3]
                    if not the_matr in j:
                        continue
                    for k in third:
                        if i==k or j==k:
                            continue
                        if not the_matr in k:
                            continue
                        is_matr_exist = (the_matr + ': ' + j + '-' + i + '-' + k in union
                                        or the_matr + ': ' + k + '-' + i + '-' + j in union
                                        or the_matr + ': ' + i + '-' + k + '-' + j in union
                                        or the_matr + ': ' + j + '-' + k + '-' + i in union
                                        or the_matr + ': ' + k + '-' + j + '-' + i in union)
                        if is_matr_exist:
                            continue
                        union.append(the_matr + ': ' + i + '-' + j + '-' + k)
        return union

class BaseSimpleModeDefaultTextHandler:
    def __init__(self):
        self.count = -1
        self.values_handler = ValuesHandlers.dummy_values_handler

    def do_action(self, text, settings) -> Result:
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
        
class Gibrid3ModeDefaultTextHandler(BaseSimpleModeDefaultTextHandler):
    def __init__(self):
        super().__init__()
        self.count = 2
        self.values_handler = ValuesHandlers.gibrid_3_values_handler
        
class Gibrid4ModeDefaultTextHandler(BaseSimpleModeDefaultTextHandler):
    def __init__(self):
        super().__init__()
        self.count = 2
        self.values_handler = ValuesHandlers.gibrid_4_values_handler
        
class MetaModeDefaultTextHandler(BaseSimpleModeDefaultTextHandler):
    def __init__(self):
        super().__init__()
        self.count = 2
        self.values_handler = ValuesHandlers.meta_values_handler
        
class LogoModeDefaultTextHandler(BaseSimpleModeDefaultTextHandler):
    def __init__(self):
        super().__init__()
        self.count = 2
        self.values_handler = ValuesHandlers.logo_values_handler
        
class BrukModeDefaultTextHandler(BaseSimpleModeDefaultTextHandler):
    def __init__(self):
        super().__init__()
        self.count = 2
        self.values_handler = ValuesHandlers.bruk_values_handler
        
class AnagModeDefaultTextHandler(BaseSimpleModeDefaultTextHandler):
    def __init__(self):
        super().__init__()
        self.count = 2
        self.values_handler = ValuesHandlers.anag_values_handler
        
class PlusModeDefaultTextHandler(BaseSimpleModeDefaultTextHandler):
    def __init__(self):
        super().__init__()
        self.count = 2
        self.values_handler = ValuesHandlers.plus_values_handler
        
class ScepkaModeDefaultTextHandler(BaseSimpleModeDefaultTextHandler):
    def __init__(self):
        super().__init__()
        self.count = 2
        self.values_handler = ValuesHandlers.scepka_values_handler
        
class MatrModeDefaultTextHandler(BaseSimpleModeDefaultTextHandler):
    def __init__(self):
        super().__init__()
        self.count = 3
        self.values_handler = ValuesHandlers.matr_values_handler
        
class CombinedModeDefaultTextHandler():
    def __init__(self):
        self.combined_values_handlers = [
            ValuesHandlers.olymp_values_handler,
            ValuesHandlers.gibrid_3_values_handler,
            ValuesHandlers.gibrid_4_values_handler,
            ValuesHandlers.meta_values_handler,
            ValuesHandlers.logo_values_handler,
            ValuesHandlers.bruk_values_handler,
            ValuesHandlers.anag_values_handler,
            ValuesHandlers.plus_values_handler,
            ValuesHandlers.scepka_values_handler
        ]
        
    def do_action(self, text, settings) -> Result:
        input_result = Utils.simple_parse_to_input(text, 2)
        if not input_result.is_success:
            return input_result

        values = []
        for values_handler in self.combined_values_handlers:
            union = values_handler(input_result.values)
            unique_union = Utils.get_unique(union)
            values.append(str(len(unique_union)))
            values.append('\n'.join(unique_union))
        return Result.success(values)

class CubraModeDefaultTextHandler():
    def __init__(self):
        pass
        
    def do_action(self, text, settings) -> Result:
        if text=='+':
            settings.mem_mode = ModeType.Cubra
            settings.mem_values = text
            return Result.success(['ok, send me full task text'])
        if settings.mem_mode == ModeType.Cubra and settings.mem_values == '+':
            settings.mem_values = None
            text = text.lower()
            lines = Utils.remove_empty(text.replace('\r','\n').split('\n'))
            output = []
            output_count = 0
            for line in lines:
                is_cubra = True
                if 'бонус' in line or 'кубрая' in line or 'задание' in line:
                    is_cubra = False
                if not '_' in line and not ' ' in line:
                    is_cubra = False
                if '_' in line:
                    is_cubra = True
                if not is_cubra:
                    continue
                line_result = self.internal_do_action(line)
                output.extend(line_result.values)
                output_count = output_count + 1
            output.append('{0}/{1} lines are identified as cubra'.format(output_count, len(lines)))
            return Result.success(output)
        return self.internal_do_action(text)

    def internal_do_action(self, text):
        text = text.strip().lower()
        input_values = []
        output_notfound = []

        if text.startswith('?'):
            text = text[1:].strip()
            self.parse(text, input_values, output_notfound)
            cubra_def_values = []
            for word_list in input_values:
                if len(word_list)!=0:
                    cubra_def_values.append(', '.join(word_list))
                else:
                    cubra_def_values.append('-')
            return Result.success(['\n'.join(cubra_def_values)])

        if text.startswith('+'):
            text = text[1:].strip()
            self.parse(text, input_values, output_notfound)
            values = []
            if len(output_notfound) > 0:
                values.append('not found cubra for: ' + ', '.join(output_notfound))
            for i in range(len(input_values)):
                new_input_values = []
                for j in range(len(input_values)):
                    if i==j:
                        new_input_values.append([])
                    else:
                        new_input_values.append(input_values[j])
                part_values = self.do_search(new_input_values, [])
                values.extend(part_values)
            return Result.success(values)

        self.parse(text, input_values, output_notfound)
        values = self.do_search(input_values, output_notfound)
        return Result.success(values)

    def do_search(self, input_values, output_notfound):
        str_pattern = self.create_str_pattern(input_values)
        pattern = re.compile(str_pattern)
        union = [ output_word for output_word in RussianWords.data if pattern.search(output_word) ]

        values = []
        values.append(str(len(union)))
        if len(union)>200:
            values.append('there are too many words')
        else:
            values.append('\n'.join(union))
        if len(output_notfound) > 0:
            values.append('not found cubra for: ' + ', '.join(output_notfound))
        values.append('used pattern:\n' + str_pattern)
        return values

    def create_str_pattern(self, input_values):
        str_pattern = ''
        for word_list in input_values:
            if len(word_list)!=0:
                str_pattern = str_pattern + '(?:' + '|'.join(word_list) + ')'
            else:
                str_pattern = str_pattern + '.+'
        return '^' + str_pattern + '$'

    def parse(self, text, input_values, output_notfound):
        input = []
        if '_' in text:
            input = Utils.remove_empty(text.split('_'))
        else:
            input = Utils.remove_empty(text.split(' '))
        for input_word in input:
            input_word = input_word.strip()
            input_values_item = []
            if input_word.startswith('.'):
                exact_input = Utils.remove_empty(input_word.split('.'))
                input_values_item = [word.strip() for word in exact_input]
                input_values.append(input_values_item)
                continue
            if input_word.startswith(','):
                exact_input = Utils.remove_empty(input_word.split(','))
                for input_word in exact_input:
                    input_values_item.extend(CubraDefinition.get(input_word.strip()))
            else:
                if input_word.startswith('%'):
                    input_word = input_word[1:].strip()
                    ass = Utils.get_associations(input_word)
                    input_values_item.extend(ass)
                input_values_item.extend(CubraDefinition.get(input_word))
            input_values.append(input_values_item)
            if len(input_values_item) == 0:
                output_notfound.append(input_word)

    #def search_with_strings_3_performance_test(self, values):
    #    first = values[0]
    #    second = values[1]
    #    third = values[2]
    #    result = []
    #    for word1 in first:
    #        for word2 in second:
    #            for word3 in third:
    #                value = word1+word2+word3
    #                if value in RussianWords.data or True:
    #                    result.append(value+' = '+word1+' + '+word2+' + '+word3)
    #    return result
    
    #def search_with_regex(self, values):
    #    str_pattern = '^'
    #    for word_list in values:
    #        if len(word_list)!=0:
    #            str_pattern = str_pattern + '(?:' + '|'.join(word_list) + ')'
    #        else:
    #            str_pattern = str_pattern + '.+'
    #    str_pattern = str_pattern + '$'
    #    pattern = re.compile(str_pattern)
    #    return [ word for word in RussianWords.data if pattern.search(word) ]

    #def search_with_strings(self, values):
    #    output = []
    #    self.search_with_strings_internal(values, '', 0, len(values) - 1, output)
    #    return output

    #def search_with_strings_internal(self, values, result_word, index, maxindex, output):
    #    if index>maxindex:
    #        if result_word in RussianWords.data or True:
    #            output.append(result_word)
    #        return
    #    for word in values[index]:
    #        self.search_with_strings_internal(values, result_word+word,index+1,maxindex,output)

    
class SpecialModeDefaultTextHandler():
    def __init__(self):
        self.fake_settings = Settings()
        self.cubra_solver = CubraModeDefaultTextHandler()
        
    def do_action(self, text, settings) -> Result:
        if text=='+':
            for i in range(100):
                count = random.randint(2,4)
                if count == 2:
                    t = 1
                values = []
                for i in range(count):
                    rand_key = random.choice(list(CubraDefinition.data.keys()))
                    values.append(rand_key)
                text_cubra = '_'.join(values)
                result = self.cubra_solver.do_action(text_cubra, self.fake_settings)
                if not result.is_success:
                    continue
                if result.values[0] == '0' or result.values[1] == 'there are too many words':
                    continue
                settings.mem_mode = ModeType.Special
                settings.mem_values = text_cubra
                return Result.success([text_cubra])
            return Result.failed('it needs more time, send ''+'' again')
        if settings.mem_mode == ModeType.Special:
            expected = self.cubra_solver.do_action(settings.mem_values)
            if text in expected.values[1]:
                return Result.success('congratulations!')
            else:
                return Result.failed('no')
        else:
            return Result.failed('you are not generate any cubra')


