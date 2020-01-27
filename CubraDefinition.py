class CubraDefinition:
    data = {
            'q': ['w','e'],
            'a': ['ppp','кошка'],
            'x': ['1','2','3'],
            'кот': ['1','2','3'],
            }

    @staticmethod
    def get(key):
        if CubraDefinition.data.__contains__(key):
            return CubraDefinition.data[key]
        return []
