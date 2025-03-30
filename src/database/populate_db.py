import sqlite3
from webScrap.card import Card
from webScrap.scrapping import scrap_for_cards, scrap_for_sets

def populate_db():
    # Remove all the old tables
    
    # I want this to go out, get the list page, add a table for each set to the db
    sets = scrap_for_sets()

    # Then I want to go thru all of the sets, get the top card, and add it to the db
    placeholder_card = Card("placeholder", "placeholder", "placeholder") # I hope I never get placeholder back from the website...
    
    # [print(card) for card in scrap_for_cards(placeholder_card, "")]

if __name__=="__main__":
    populate_db()