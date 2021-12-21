from typing import *
from telegram import *
from telegram.ext import *
from time import sleep
import requests
from bs4 import BeautifulSoup
from lxml import etree 

bot_token = "5049973042:AAG--t9oSTHxO3DE30PyxXTItj98np26kls"
bot = Bot(bot_token)

__api  = f"https://api.telegram.org/bot{bot_token}/getUpdates"
print(__api)

group_name = "Cricket score"

response = requests.get(url=__api).json()
print("response")
result = response['result']
print(result)
group_id = None
def chat(update_id):
    if update_id['message']['chat']:
        if update_id['message']['chat']['title'] == group_name:
            group_id = update_id['message']['chat']['id']
            print(group_id)
            return group_id
        else:
            return None
    else:
        return None

for update_id in result:
    chat_number = update_id["my_chat_member"] if "my_chat_member" in update_id else chat(update_id)
    if type(chat_number) is int:
        group_id = chat_number
        print("loop breaked")
        break
    print(chat_number)
    if chat_number is None:
        continue
    chat = chat_number['chat']
    if chat['title'] == group_name:
        group_id = chat['id']
        break
    else:
        print("group not found")


updater: Updater = Updater(bot_token,use_context=True)

#group_id : int = -664721777

def overview():
    URL = "https://www.cricbuzz.com"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find_all('li', attrs = {'class': 'cb-col cb-col-25 cb-mtch-blk cb-vid-sml-card-api videos-carousal-item cb-carousal-item-large cb-view-all-ga'})
    
    # replace this with the team initials eg. IND for India
    pref = 'JKS'
    match = None
    for li in table:
        match = li.text.strip()
        # print(match)

        if(match.count(pref)>0):
            # print(match)
            link = li.find('div', attrs = {'class': 'cb-ovr-flo'})
            aus = li.find('div', attrs= {'class': 'cb-hmscg-tm-nm'})
            # print('\n')
            match =  match
            break
    position = match.find("JKS")
    position2 = match.find("DMG")
    final_score = ""
    for index, val in enumerate(match):
        if index - 3 == position:
            final_score += " "
        if index - 3 == position2:
            final_score += " "
        final_score += val
    score = final_score
    return score




previous_msg = ""
print(True) if group_id is not None else print(False)
while group_id is not None:
    score = overview()
    print(score)
    print(overview())
    if score != previous_msg:
        updater.bot.sendMessage(chat_id=f'{group_id}', text=score)
        print("Message is updated")
        previous_msg = score
    sleep(1)
