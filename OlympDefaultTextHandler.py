import enum
import requests
from module1 import *

class OlympDefaultTextHandler:
    def __init__(self):
        pass

    def do_action(self, text) -> Result:
        try:
            parse_result = ParseHelper.default_parse_to_input(text, 2, WordHandlers.get_associations_word_handler)
            if not parse_result.is_success:
                return parse_result
            first = parse_result.values[0]
            second = parse_result.values[1]
            union = list(set(first).intersection(second))
            unique_union = Utils.get_unique(union)
            result = [ str(len(unique_union)), '\n'.join(unique_union) ]
            return Result.success(result)
        except Exception as e:
            return Result.failed("Exception: {0}".format(str(e)))