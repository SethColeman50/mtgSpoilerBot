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
    
    # I want this to go out, get the list page, add them all to a set table
    sets = scrap_for_sets()
    for set in sets:
        db.insert_set(set)
        
        # Then I want to go thru all of the sets, get the top card, and add it to the db
        if os.getenv("TESTING") is not None:
            newest_card = scrap_for_cards(set)[1:2]
        else:
            newest_card = scrap_for_cards(set, get_only_latest=True)

        if newest_card != []:
            db.insert_card(newest_card[0])

    logger.info("Populated database")

if __name__=="__main__":
    populate_db()