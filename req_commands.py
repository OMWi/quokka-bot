import requests
import config

def send_message(chat_id, text):
    method = "sendMessage"
    url = "{tg_api}{token}/{method}".format(tg_api=config.TG_API, token=config.TOKEN, method=method)
    data = {"chat_id" : chat_id, "text" : text}
    requests.post(url, data=data)