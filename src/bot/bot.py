import discord
from dotenv import load_dotenv
import os
from database.database import Database
from webScrap.scrapping import scrap
from webScrap.card import Card
from discord.ext import tasks
import traceback

CHANNEL_ID = 1353775520826916917
MY_USER_ID = 453325432658460685

def start_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        send_new_cards.start()

    @tasks.loop(minutes=20)
    async def send_new_cards():
        try:
            new_cards = get_new_cards()
        except Exception:
            await client.get_user(MY_USER_ID).send(f"An exception happened :(\n```\n{traceback.format_exc()}\n```")

        for card in new_cards:
            message = card.oracle_text if '\n' in card.oracle_text else ""
            image = discord.Embed(type="image", description=card.name).set_image(url=card.image_link)

            await client.get_channel(CHANNEL_ID).send(message, embed=image, silent=True)
            print(f"sent message for {card.name}")
    
    load_dotenv()
    client.run(os.getenv("TOKEN"))

def get_new_cards():
    db = Database()
    new_cards = scrap(latest_card=db.get_latest_card())
    db.insert_many_cards(new_cards)
    return new_cards

        


if __name__=="__main__":
    start_bot()

