class FakeUpdate:
    def __init__(self):
        self.message = FakeMessage()

class FakeMessage:
    def __init__(self):
        self.chat = FakeChat()
        self.text = ''

    def reply_text(self, input):
        print(input)

class FakeChat:
    def __init__(self):
        self.id = ''
        
class FakeContext:
    def __init__(self):
        self.bot = FakeBot()

class FakeBot:
    def send_message(self, str1, str2):
        pass