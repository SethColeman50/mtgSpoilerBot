from bs4 import BeautifulSoup
import requests
import time
from webScrap.card import Card
import re
from datetime import datetime
from webScrap.set import Set
import os
from dotenv import load_dotenv
from src.__main__ import get_logger

header = {
    "User-Agent": "MTG Spoiler Discord Bot for private use",
    "contact": "sethcoleman2003@gmail.com"
}

PLACEHOLDER_CARD = Card("placeholder", "placeholder", "placeholder", "placeholder")

logger = get_logger(__name__, "scrapping.log")

def scrap_for_cards(set: Set, latest_card=PLACEHOLDER_CARD, get_only_latest=False) -> list[Card]:
    load_dotenv("../../.env")
    is_testing = os.getenv("TESTING") is not None

    if is_testing:
        contents = open(f'src/webScrap/testing_html/{set.link.split('/')[-2]}.html', 'r').read()
    else:
        contents = requests.get(set.link, headers=header).text
    
    soup = BeautifulSoup(contents, 'html.parser')

    if get_only_latest:
        cards = soup.find_all("article")[:1]
    else:
        cards = soup.find_all("article")

    output = []
    for card in cards:
        if not is_testing:
            time.sleep(1)

        name = card.find("h4").find("a").text
        if latest_card != None and name == latest_card.name:
            return output

        image_link = card.find("a").find("img").get("src")

        link = card.find("a").get('href')        
        if is_testing:
            card_page = open("src/webScrap/testing_html/cardPageWithDescription.html", "r").read()
        else:
            card_page = requests.get(link, headers=header).text
            
        card_page = BeautifulSoup(card_page, 'html.parser')
        oracle_text = card_page.find("div", attrs={"class": "c-content"}).text.strip()

        card = Card(
            name=name,
            image_link=image_link,
            oracle_text=oracle_text,
            set_name=set.name
        )
        
        output.append(card)

        logger.info(f"Scrapped this card: {card}")
    
    return output

def scrap_for_sets() -> list[Set]: 
    load_dotenv("../../.env")
    is_testing =  os.getenv("TESTING") is not None
    
    if is_testing:
        contents = open("src/webScrap/testing_html/setListPage.html", 'r').read()
    else:
        contents = requests.get("https://www.magicspoiler.com/mtg-spoilers/").text
        
    soup = BeautifulSoup(contents, "html.parser")

    sets = soup.find("div", attrs={"class": "upcoming-sets"}).find_all("a")

    output = []
    for set in sets:
        date_full_text = set.find("p").text
        regex = r'((1[0-2]|0?[1-9])\/(3[01]|[12][0-9]|0?[1-9])\/(?:[0-9]{2})?[0-9]{2})|((Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{1,2},\s+\d{4})'
        date_text = re.search(regex, date_full_text).group() # found here: https://stackoverflow.com/a/56081857
        date = datetime.strptime(date_text, "%B %d, %Y")

        if date.date() < datetime.now().date():
            return output
        
        name = set.find("div", attrs={"class": 'upcoming-set'}).find('div').text
        link = set["href"]

        set = Set(name, link, date)
        output.append(set)
        logger.info(f"Scrapped this set: {set}")

    return output

