import discord
from dotenv import load_dotenv
import os
from database.database import Database
from webScrap.scrapping import scrap_for_cards, scrap_for_sets
from webScrap.card import Card
from discord.ext import tasks
import traceback
from database.populate_db import populate_db
from src.__main__ import get_logger

logger = get_logger(__name__, "bot.log")

load_dotenv()
MY_USER_ID = os.getenv("ADMIN_USER_ID")
if MY_USER_ID == None or not MY_USER_ID.isdigit():
    logger.error("Discord user id missing or incorrect in .env")
    exit()

db = Database()

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

            images = [image]
            for link in card.extra_image_links:
                image = discord.Embed(type="image", description="").set_image(url=link)
                images.append(image)

            if not message and not image:
                logger.info(f"Skipping card {card.name} because message and embed are empty")

            for channel_id in channels:
                channel = client.get_channel(channel_id)

                if not channel:
                    logger.warning(f"Channel {channel_id} not found.")
                else:
                    try:
                        await channel.send(message, embeds=images, silent=True)
                        logger.info(f"Sent message for {card.name} to channel {channel_id}")
                    except Exception:
                        logger.error(f"Failed to send {card.name} to {channel_id}: {traceback.format_exc()}")

    @client.event
    async def on_message(message):
        if message.author == client.user or client.user not in message.mentions or message.author.id != MY_USER_ID:
            return
        
        if "shutdown" in message.content.lower():
            logger.warning("Bot shutdown by command")
            exit()
        
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
        current_cards = db.get_all_cards_in_set(set)
        for card in scrap_for_cards(set, current_cards):
            new_cards.append(card)

    db.insert_many_cards(new_cards)
    
    return new_cards


if __name__ == "__main__":
    start_bot()

