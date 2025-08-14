from webScrap.card import Card
from webScrap.scrapping import scrap_for_cards, scrap_for_sets
from database.database import Database
from dotenv import load_dotenv
import os
from src.__main__ import get_logger

load_dotenv("../../.env")
logger = get_logger(__name__, "db.log")

def populate_db():
    db = Database()

    if os.getenv("TESTING") is not None:
        db.cursor.execute('''
            DELETE FROM cards;     
        ''')
    
    # I want this to go out, get the list page, add them all to a set table
    sets = scrap_for_sets()
    for set in sets:
        db.insert_set(set)
        
        # Then I want to go thru all of the sets, get the top card, and add it to the db
        if os.getenv("TESTING") is not None:
            cards = scrap_for_cards(set)[2:]
        else:
            cards = scrap_for_cards(set)
        
        if cards != []:
            db.insert_many_cards(cards)

    logger.info("Populated database")

if __name__=="__main__":
    populate_db()