import json
import requests
import urllib


TOKEN = "5248347573:AAGxx9NF-SABa_8cFhKZLvdsMtiNIEB8gF4"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
USERNAME_BOT = "wsrtest"


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def send_message(text, chat_id):
    tot = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(tot, chat_id)
    get_url(url)


def send_document(doc, chat_id):
    files = {'document': open(doc, 'rb')}
    requests.post(URL + "sendDocument?chat_id={}".format(chat_id), files=files)


def send_image(doc, chat_id):
    files = {'photo': open(doc, 'rb')}
    requests.post(URL + "sendPhoto?chat_id={}".format(chat_id), files=files)


schedule = {
    '11fm': {
        'monday': ['русс яз', 'математика']
    }
}


def echo_all(updates):
    for update in updates["result"]:
        if update.get("message") != None:
            if update.get("message", {}).get("text") != None:
                # text = "/monday 11fm"
                # /nearest 11fm

                text = update["message"]["text"]
                chat_id = update["message"]["chat"]["id"]

                if text == '/start':
                    pass
                elif text == '/help':
                    pass
                else:
                    send_message(text, chat_id)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if updates is not None:
            if len(updates["result"]) > 0:
                last_update_id = get_last_update_id(updates) + 1
                echo_all(updates)


if __name__ == '__main__':
    main()