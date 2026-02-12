class Account:
    def __init__(self,username: str,password: str):
        self.username = username
        self.password = password
        self.chats = []
    def get_username(self):
        return self.username
    def check_password(self,guesspassword):
        return self.password==guesspassword
    def add_chat(self, chat):
        self.chats.append(chat)

class Message:
    def __init__(self, text: str):
        self.text = text

class Chat:
    def __init__(self,name: str,root: Account):
        self.name = name
        self.root = root
        self.messages = []
    def add_message(self, owner_id: int, message: str):
        self.messages