import sqlite3
from webScrap.card import Card

# I want a database singleton that combines all the things I've created so far to reduce repeated code
TABLE_NAME = "cards"

class Database():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.connection = sqlite3.connect("previous_cards.db")
        self.cursor = self.connection.cursor()
        self.create_table()
        self.current_id = self.cursor.execute(f"SELECT MAX(rowid) FROM {TABLE_NAME}").fetchone()[0]

    def create_table(self):
        if self.cursor.execute(f"SELECT name FROM sqlite_master WHERE name='{TABLE_NAME}'").fetchone() is None:
            self.cursor.execute(f"CREATE TABLE {TABLE_NAME}(name, image_link, oracle_text)")

    def insert_card(self, card: Card):
        self.cursor.execute(f"""
            INSERT INTO {TABLE_NAME} VALUES
                ('{card.name}', '{card.image_link}', '{card.oracle_text}')
        """)

        self.current_id = self.cursor.execute("SELECT last_insert_rowid()").fetchone()[0]

        self.connection.commit()

    def insert_many_cards(self, cards: list[Card]):
        cards.reverse() # This is because the cards are given to this function as newest to oldest, and I want the newest to be the last card added to the db for latest card to work
        for card in cards:
            self.insert_card(card)

    def get_latest_card(self):
        if self.current_id == None:
            return None
        
        return Card(*self.cursor.execute(f"""
            SELECT * FROM {TABLE_NAME} WHERE rowid={self.current_id}
        """).fetchone())