from database.database import Database
from webScrap.card import Card
from webScrap.scrapping import scrap

# I want this to check what the last new card was, call the function in scraping with that card, which will return any new cards, then add those to the database, then tell the bot to send a message
def main():
    db = Database()
    new_cards = scrap(latest_card=db.get_latest_card())
    db.insert_many_cards(new_cards)
    # call bot

if __name__ == "__main__":
    main()