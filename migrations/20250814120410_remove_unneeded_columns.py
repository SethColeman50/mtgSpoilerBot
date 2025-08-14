"""
This module contains a Caribou migration.

Migration Name: remove_unneeded_columns
Migration Version: 20250814120410
"""
CARD_TABLE_NAME = "cards"
CHANNEL_TABLE_NAME = "channels"
SETS_TABLE_NAME = "sets"

def upgrade(connection):
    connection.execute(f'ALTER TABLE {CARD_TABLE_NAME} DROP COLUMN oracle_text;')
    connection.execute(f'ALTER TABLE {CARD_TABLE_NAME} DROP COLUMN image_link;')

    connection.execute(f'ALTER TABLE {SETS_TABLE_NAME} DROP COLUMN release_date;')
    connection.execute(f'ALTER TABLE {SETS_TABLE_NAME} DROP COLUMN latest_card_id;')

    connection.commit()

def downgrade(connection):
    connection.execute(f'ALTER TABLE {CARD_TABLE_NAME} ADD COLUMN oracle_text;')
    connection.execute(f'ALTER TABLE {CARD_TABLE_NAME} ADD COLUMN image_link;')

    connection.execute(f'ALTER TABLE {SETS_TABLE_NAME} ADD COLUMN release_date;')
    connection.execute(f'ALTER TABLE {SETS_TABLE_NAME} ADD COLUMN latest_card_id;')

    connection.commit()
