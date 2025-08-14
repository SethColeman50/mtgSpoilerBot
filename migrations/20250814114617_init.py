"""
This module contains a Caribou migration.

Migration Name: init
Migration Version: 20250814114617
"""

CARD_TABLE_NAME = "cards"
CHANNEL_TABLE_NAME = "channels"
SETS_TABLE_NAME = "sets"

def upgrade(connection):
    # add your upgrade step here
    connection.execute(f'''
        CREATE TABLE IF NOT EXISTS {CHANNEL_TABLE_NAME} (
            guild_id    INTEGER,
            channel_id  INTEGER,
            PRIMARY KEY (guild_id)
        )
    ''')

    connection.execute(f"""
        CREATE TABLE IF NOT EXISTS {SETS_TABLE_NAME} (
            name        TEXT,
            link            TEXT,
            release_date    TEXT,
            latest_card_id  INTEGER,
            PRIMARY KEY (name)
        )
    """)

    connection.execute(f'''
        CREATE TABLE IF NOT EXISTS {CARD_TABLE_NAME} (
            name        TEXT, 
            image_link  TEXT, 
            oracle_text TEXT,
            set_name    TEXT,
            FOREIGN KEY(set_name) REFERENCES {SETS_TABLE_NAME}(name),
            PRIMARY KEY (name)
        )
    ''')

    connection.commit()

def downgrade(connection):
    connection.execute(f'''
        DROP TABLE {CARD_TABLE_NAME};
        DROP TABLE {SETS_TABLE_NAME};   
        DROP TABLE {CHANNEL_TABLE_NAME};            
    ''')
