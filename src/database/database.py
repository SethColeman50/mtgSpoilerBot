import sqlite3
from webScrap.card import Card
from webScrap.set import Set
from src.__main__ import get_logger

# I want a database singleton that combines all the things I've created so far to reduce repeated code
CARD_TABLE_NAME = "cards"
CHANNEL_TABLE_NAME = "channels"
SETS_TABLE_NAME = "sets"

logger = get_logger(__name__, "db.log")

class Database():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.connection = sqlite3.connect("previous_cards.db")
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {CHANNEL_TABLE_NAME} (
                guild_id    INTEGER,
                channel_id  INTEGER,
                PRIMARY KEY (guild_id)
            )
        ''')

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {SETS_TABLE_NAME} (
            name        TEXT,
            link            TEXT,
            release_date    TEXT,
            latest_card_id  INTEGER,
            PRIMARY KEY (name)
        )""")

        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {CARD_TABLE_NAME} (
                name        TEXT, 
                image_link  TEXT, 
                oracle_text TEXT,
                set_name    TEXT,
                FOREIGN KEY(set_name) REFERENCES {SETS_TABLE_NAME}(name),
                PRIMARY KEY (name)
            )
        ''')

        logger.info("created tables")

    def insert_card(self, card: Card):
        self.cursor.execute(f"""
            INSERT OR IGNORE INTO {CARD_TABLE_NAME} VALUES
                ("{card.name}", "{card.image_link}", "{card.oracle_text}", "{card.set_name}")
        """)

        row_id = self.cursor.execute("SELECT last_insert_rowid()").fetchone()[0]

        if row_id != 0:
            self.cursor.execute(f'''
                UPDATE {SETS_TABLE_NAME}
                SET "latest_card_id" = ?
                WHERE "name" = ?         
            ''', (row_id, card.set_name))
            logger.info(f"Inserted this card: {card}")
        else:
            logger.warning(f"Failed to insert duplicate card: {card}")

        self.connection.commit()

    def insert_many_cards(self, cards: list[Card]):
        cards.reverse() # This is because the cards are given to this function as newest to oldest, and I want the newest to be the last card added to the db for latest card to work
        for card in cards:
            self.insert_card(card)

    def get_latest_card(self, set: Set):
        rowid = self.cursor.execute(f'''
            SELECT latest_card_id FROM {SETS_TABLE_NAME}
            WHERE name=?                           
        ''', (set.name, )).fetchone()[0]

        if rowid == -1:
            return None
        
        return Card(*self.cursor.execute(f"""
            SELECT * FROM {CARD_TABLE_NAME} WHERE rowid=?
        """, (rowid, )).fetchone())
    
    def insert_channel(self, guild_id: int, channel_id: int):
        self.cursor.execute(f'''
            REPLACE INTO {CHANNEL_TABLE_NAME} VALUES
                ({guild_id}, {channel_id})
        ''')

        self.connection.commit()
        logger.info(f"Inserted channel {channel_id} in guild {guild_id} into database")
    
    def get_all_channels(self):
        guilds_and_channels = self.cursor.execute(f'''
            SELECT channel_id FROM {CHANNEL_TABLE_NAME}
        ''').fetchall()
        return [guild_and_channel[0] for guild_and_channel in guilds_and_channels]
    
    def insert_set(self, set: Set):
        self.cursor.execute(f'''
            INSERT OR IGNORE INTO {SETS_TABLE_NAME} VALUES
                ("{set.name}", '{set.link}', '{set.release_date}', -1)
        ''')
        
        self.connection.commit()
        logger.info(f"Inserted this set into the database: {set}")

    def get_all_sets(self):
        query_result = self.cursor.execute(f'SELECT * FROM {SETS_TABLE_NAME}').fetchall()
        
        return [Set(name, link, release_date) for name, link, release_date, _ in query_result]
    