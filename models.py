class Word:
    def __init__(self, word_en:str, word_type:str):
        self.word_en = word_en[0:64] 
        self.word_type = word_type[0:4]
    
class Meaning:
    def __init__(self, meaning:str, word_id:int):
        self.meaning = meaning[0:200] 
        self.word_id = word_id

class User:
    def __init__(self, user_id, role, chat_id, status, login_status, username, password):
        self.user_id = user_id
        self.role = role
        self.chat_id = chat_id
        self.status = status
        self.login_status = login_status
        self.username  = username
        self.password = password

class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    

# login status 0 - not logged in, 1 - logged in
# status 0-nothing, 1-reg_info_asked, 2-login_info_asked, 3-test asked