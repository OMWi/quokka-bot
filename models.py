class Word:
    def __init__(self, word_en:str, word_type:str) -> None:
        self.word_en = word_en[0:20] #?
        self.word_type = word_type[0:3]
    
class Meaning:
    def __init__(self, meaning:str, word_id:int) -> None:
        self.meaning = meaning #?
        self.word_id = word_id

class Users:
    def __init__(self, user_id:str, role:str, status:str) -> None:
        self.user_id = user_id
        self.role = role
        self.status = status