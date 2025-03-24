import sqlite3
from webScrap.card import Card

# I want a database singleton that combines all the things I've created so far to reduce repeated code
class Database():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.connection = sqlite3.connect("previous_cards.db")
        self.cursor = self.connection.cursor()
        self.current_id = None
        self.create_table()

    def create_table(self):
        if self.cursor.execute("SELECT name FROM sqlite_master WHERE name='cards'").fetchone() is None:
            self.cursor.execute("CREATE TABLE cards(name, image_link, oracle_text)")

    def insert_card(self, card: Card):
        self.cursor.execute(f"""
            INSERT INTO cards VALUES
                ('{card.name}', '{card.image_link}', '{card.oracle_text}')
        """)

        self.current_id = self.cursor.execute("SELECT last_insert_rowid()").fetchone()[0]

        self.connection.commit()

    def get_newest_card(self):
        return Card(*self.cursor.execute(f"""
            SELECT * FROM cards WHERE rowid={self.current_id}
        """).fetchone())