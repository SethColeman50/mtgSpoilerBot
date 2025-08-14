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

    def insert_card(self, card: Card):
        try:
            self.cursor.execute(f"""
                INSERT OR FAIL INTO {CARD_TABLE_NAME} VALUES
                    ("{card.name}", "{card.set_name}")
            """)
            self.connection.commit()

            logger.info(f"Inserted this card: {card}")
        except:
            logger.warning(f"Failed to insert duplicate card: {card}")

    def insert_many_cards(self, cards: list[Card]):
        for card in cards:
            self.insert_card(card)

    def get_all_cards_in_set(self, set: Set):
        card_names = self.cursor.execute(f'''
            SELECT name FROM {CARD_TABLE_NAME}
            WHERE set_name="{set.name}"              
        ''').fetchall()

        return [Card(name[0], set.name) for name in card_names]
    
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
                ("{set.name}", '{set.link}')
        ''')
        
        self.connection.commit()
        logger.info(f"Inserted this set into the database: {set}")

    
    