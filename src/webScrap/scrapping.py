from bs4 import BeautifulSoup
import requests
import time
from webScrap.card import Card

header = {
    "User-Agent": "MTG Spoiler Discord Bot for private use",
    "contact": "sethcoleman2003@gmail.com"
}

def scrap(latest_card: Card):
    contents = requests.get('https://www.magicspoiler.com/mtg-set/tarkir-dragonstorm/', headers=header).text
    # contents = open('src/webScrap/testingContent.html', 'r').read()
    soup = BeautifulSoup(contents, 'html.parser')

    cards = soup.find_all("article")[:20] # I'll hopefully never be more than 20 behind
    output = []
    for card in cards:
        # time.sleep(1)

        name = card.find("h4").find("a").text
        if latest_card != None and name == latest_card.name:
            return output

        image_link = card.find("a").find("img").get("src")

        link = card.find("a").get('href')
        card_page = requests.get(link, headers=header).text
        # card_page = open("src/webScrap/cardPageWithDescription.html", "r").read()
        card_page = BeautifulSoup(card_page, 'html.parser')
        oracle_text = card_page.find("div", attrs={"class": "c-content"}).text

        output.append(Card(
            name=name,
            image_link=image_link,
            oracle_text=oracle_text
        ))
    
    return output

