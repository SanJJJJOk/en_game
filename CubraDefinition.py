from Crypto.Cipher import AES
import json

class CubraDefinition:
    data = {}

    @staticmethod
    def get(key):
        if CubraDefinition.data.__contains__(key):
            return CubraDefinition.data[key]
        return []

    @staticmethod
    def load_cubra(str_password):
        bytes_password = str_password.encode('utf-8')
        inittext_bytes = CubraDefinition.decrypt(enctext, bytes_password)
        init_text= str(inittext_bytes, 'utf-8')
        CubraDefinition.data = json.loads(init_text)

    @staticmethod
    def encrypt(text, password):
        aes_obj = AES.new(password, AES.MODE_CBC, b'This is an IV456')
        return aes_obj.encrypt(text)

    @staticmethod
    def decrypt(text, password):
        aes_obj = AES.new(password, AES.MODE_CBC, b'This is an IV456')
        return aes_obj.decrypt(text)