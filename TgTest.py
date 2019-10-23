class FakeUpdate:
    def __init__(self):
        self.message = FakeMessage()

class FakeMessage:
    def __init__(self):
        self.chat = FakeChat()
        self.text = ''

    def reply_text(input):
        print(input)

class FakeChat:
    def __init__(self):
        self.id = ''