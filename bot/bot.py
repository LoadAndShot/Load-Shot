import discord
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD = os.getenv('DISCORD_GUILD_ID')
LEGAL_CHANNEL_ID = int(os.getenv('DISCORD_LEGAL_CHANNEL_ID'))
ILLEGAL_CHANNEL_ID = int(os.getenv('DISCORD_ILLEGAL_CHANNEL_ID'))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
