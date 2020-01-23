import enum
import requests
from module1 import *

class ValuesHandlers:
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
                    union.append(i + '-' + j)
                    #output.append(i)
                    #output.append(j)
                if i[0:3] == j[-3:]:
                    union.append(j + '-' + i)
                    #output.append(i)
                    #output.append(j)
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
                    union.append(i + '-' + j)
                    #output.append(i)
                    #output.append(j)
                if i[0:4] == j[-4:]:
                    union.append(j + '-' + i)
                    #output.append(i)
                    #output.append(j)
        return union

class SimpleTwoListsDefaultTextHandler:
    def __init__(self):
        pass
    
    def do_action(self, text, values_handlers) -> Result:
        return Utils.do_actions(text, 2, values_handlers, WordHandlers.get_associations_word_handler)
