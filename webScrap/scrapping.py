from bs4 import BeautifulSoup
import requests
import time

header = {
    "User-Agent": "MTG Spoiler Discord Bot for private use",
    "contact": "sethcoleman2003@gmail.com"
}

def main():
    contents = requests.get('https://www.magicspoiler.com/mtg-set/tarkir-dragonstorm/', headers=header).text
    # contents = open('testingContent.html', 'r').read()
    soup = BeautifulSoup(contents, 'html.parser')

    cards = soup.find_all("article")[:20]
    output = []
    for card in cards:
        time.sleep(1)
        link = card.find("a").get('href')
        card_page = requests.get(link, headers=header).text
        # card_page = open("cardPageWithDescription.html", "r").read()
        card_page = BeautifulSoup(card_page, 'html.parser')
        oracle_text = card_page.find("div", attrs={"class": "c-content"}).text

        output.append({
            "name": card.find("h4").find("a").text,
            "image": card.find("a").find("img").get("src"),
            "oracle_text": oracle_text
        })
    
    return output

if __name__=="__main__":
    print(main())