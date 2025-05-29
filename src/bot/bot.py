import discord
from dotenv import load_dotenv
import os
from database.database import Database
from webScrap.scrapping import scrap_for_cards, scrap_for_sets
from webScrap.card import Card
from discord.ext import tasks
import traceback
from database.populate_db import populate_db
import logging
import sys
from src.__main__ import get_logger

MY_USER_ID = 453325432658460685

load_dotenv("../../.env")
db = Database()

logger = get_logger(__name__, "bot.log")

def start_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        logger.info(f'We have logged in as {client.user}')
        if os.getenv("TESTING") is not None:
            logger.info("Running in dev mode")

        populate_db()
        send_new_cards.start()

    @tasks.loop(minutes=20)
    async def send_new_cards():
        try:
            new_cards = get_new_cards()
            if not new_cards:
                logger.info("No new cards to post")
        except Exception:
            exception_string = f"An exception happened :(\n```\n{traceback.format_exc()}\n```"
            await client.get_user(MY_USER_ID).send(exception_string)
            logger.error(exception_string)
            return

        channels = db.get_all_channels()
        if channels == []:
            logger.warning("No channels configured to send messages")
        
        for card in new_cards:
            message = card.oracle_text if '\n' in card.oracle_text or "SRC" not in card.oracle_text else ""
            image = discord.Embed(type="image", description=card.name).set_image(url=card.image_link)

            if not message and not image:
                logger.info(f"Skipping card {card.name} because message and embed are empty")

            for channel_id in channels:
                channel = client.get_channel(channel_id)

                if not channel:
                    logger.warning(f"Channel {channel_id} not found.")
                else:
                    try:
                        await channel.send(message, embed=image, silent=True)
                        logger.info(f"Sent message for {card.name} to channel {channel_id}")
                    except Exception as e:
                        logger.error(f"Failed to send {card.name} to {channel_id}: {e}")

    @client.event
    async def on_message(message):
        if message.author == client.user or client.user not in message.mentions or message.author.id != MY_USER_ID:
            return
        
        guild_id = message.guild.id
        channel_id = message.channel_mentions[0].id
        db.insert_channel(guild_id, channel_id)

        await message.channel.send(f"Set channel as <#{channel_id}>")
        logger.info(f"Set channel in {message.guild.name} to {message.channel_mentions[0]}")
    
    client.run(os.getenv("TOKEN"))

def get_new_cards():
    sets = scrap_for_sets()
    
    new_cards = []
    for set in sets:
        for card in scrap_for_cards(set, latest_card=db.get_latest_card(set)):
            new_cards.append(card)

    db.insert_many_cards(new_cards)
    
    return new_cards


if __name__ == "__main__":
    start_bot()

