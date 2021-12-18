from typing import *
from telegram import *
from telegram.ext import *
from time import sleep
import requests
from bs4 import BeautifulSoup
from lxml import etree 

bot_token = "5042846869:AAGIv4XJ4-aBuUeRKHoJhlar9b7-GmtdIrY"
bot = Bot(bot_token)

__api  = f"https://api.telegram.org/bot{bot_token}/getUpdates"

group_name = "Cricket score"

response = requests.get(url=__api).json()
result = response['result']
print(result)
group_id = None
for update_id in result:
    chat_number = update_id["my_chat_member"] if "my_chat_member" in update_id else None
    if chat_number is None:
        continue
    chat = chat_number['chat']
    if chat['title'] == group_name:
        group_id = chat['id']
        break
    else:
        print("group not found")


updater: Updater = Updater("5042846869:AAGIv4XJ4-aBuUeRKHoJhlar9b7-GmtdIrY",use_context=True)

#group_id : int = -664721777

def overview():
    URL = "https://www.cricbuzz.com"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find_all('li', attrs = {'class': 'cb-col cb-col-25 cb-mtch-blk cb-vid-sml-card-api videos-carousal-item cb-carousal-item-large cb-view-all-ga'})
    
    # replace this with the team initials eg. IND for India
    pref = 'ENG'
    
    for li in table:
        match = li.text.strip()
        # print(match)

        if(match.count(pref)>0):
            # print(match)
            link = li.find('div', attrs = {'class': 'cb-ovr-flo'})
            aus = li.find('div', attrs= {'class': 'cb-hmscg-tm-nm'})
            # print('\n')
            return  match

score = overview()
position = score.find("AUS")
position2 = score.find("ENG")
final_score = ""
for index, val in enumerate(score):
    if index - 3 == position:
        final_score += " "
    if index - 3 == position2:
        final_score += " "
    final_score += val
score = final_score

previous_msg = ""
while group_id is not None and previous_msg != overview():
    previous_msg = overview()
    updater.bot.sendMessage(chat_id=f'{group_id}', text=score)
    sleep(1)
