from webScrap.card import Card
from webScrap.scrapping import scrap_for_cards, scrap_for_sets
from database import Database

def populate_db():
    # I want this to go out, get the list page, add them all to a set table
    sets = scrap_for_sets()
    db = Database()
    for set in sets:
        db.insert_set(set)
        
        # Then I want to go thru all of the sets, get the top card, and add it to the db
        newest_card = scrap_for_cards(set, get_only_latest=True)

        if newest_card != []:
            db.insert_card(newest_card[0])

if __name__=="__main__":
    populate_db()