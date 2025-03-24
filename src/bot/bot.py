import discord
from dotenv import load_dotenv
import os
from database.database import Database
from webScrap.scrapping import scrap
from webScrap.card import Card
from discord.ext import tasks
import traceback

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
        new_cards = []
        try:
            new_cards = get_new_cards()
            if new_cards == []:
                print("No new cards to post")
        except Exception:
            await client.get_user(MY_USER_ID).send(f"An exception happened :(\n```\n{traceback.format_exc()}\n```")
            print(traceback.format_exc(), flush=True)

        for card in new_cards:
            message = card.oracle_text if '\n' in card.oracle_text or "SRC" not in card.oracle_text else ""
            image = discord.Embed(type="image", description=card.name).set_image(url=card.image_link)

            for channel_id in Database().get_all_channels():
                await client.get_channel(channel_id).send(message, embed=image, silent=True)
                print(f"sent message for {card.name}", flush=True)

    @client.event
    async def on_message(message):
        if message.author == client.user or client.user not in message.mentions or message.author.id != MY_USER_ID:
            return
        
        guild_id = message.guild.id
        channel_id = message.channel_mentions[0].id
        Database().insert_channel(guild_id, channel_id)

        await message.channel.send(f"Set channel as <#{channel_id}>")
        print(f"Set channel in {message.guild.name} to {message.channel_mentions[0]}", flush=True)
    
    load_dotenv()
    client.run(os.getenv("TOKEN"))



def get_new_cards():
    db = Database()
    new_cards = scrap(latest_card=db.get_latest_card())
    db.insert_many_cards(new_cards)
    return new_cards

        


if __name__=="__main__":
    start_bot()

