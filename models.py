class Word:
    def __init__(self, word_en:str, word_type:str) -> None:
        self.word_en = word_en[0:64] 
        self.word_type = word_type[0:4]
    
class Meaning:
    def __init__(self, meaning:str, word_id:int) -> None:
        self.meaning = meaning[0:200] 
        self.word_id = word_id

class User:
    def __init__(self, user_id:int, role:str, chat_id:int, status:int) -> None:
        self.user_id = user_id
        self.role = role
        self.chat_id = chat_id
        self.status = status

# user status 0-not signed in, 1 - signed in