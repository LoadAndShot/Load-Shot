import os
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv
from django.conf import settings

def send_order_notification(username, cart, total_price):
    product_list = "\n".join([f"- {item['product_name']} x{item['quantity']} ({item['delivery_method']})" for item in cart])
    message = f"Nouvelle commande par {username} :\n{product_list}\nPrix total : {total_price:.2f}€"
    payload = {"content": message}
    requests.post(settings.DISCORD_WEBHOOK_URL, json=payload)

# Charge les variables d'environnement depuis .env ou Render
load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
def get_channel_ids():
    try:
        channel_legal = int(os.getenv('CHANNEL_LEGAL_ID'))
        channel_illegal = int(os.getenv('CHANNEL_ILLEGAL_ID'))
        return channel_legal, channel_illegal
    except (TypeError, ValueError):
        raise Exception("Les variables d'environnement CHANNEL_LEGAL_ID ou CHANNEL_ILLEGAL_ID sont manquantes ou incorrectes !")

# Rôles à mentionner
ROLE_LEGAL = '<@&ID_ROLE_TROTRO>'
ROLE_ILLEGAL = '<@&ID_ROLE_ALADIN>'

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')

# Fonction d’envoi des messages depuis Django
async def send_order_notification(catalogue, product_name, quantity, username):
    channel_id = CHANNEL_LEGAL_ID if catalogue == 1 else CHANNEL_ILLEGAL_ID
    role_mention = ROLE_LEGAL if catalogue == 1 else ROLE_ILLEGAL

    channel = bot.get_channel(channel_id)
    if channel:
        message = (
            f"🛒 Nouvelle commande par **{username}**\n"
            f"Produit : **{product_name}**\n"
            f"Quantité : **{quantity}**\n"
            f"{role_mention} tu es concerné !"
        )
        await channel.send(message)

# Lance le bot
if __name__ == '__main__':
    bot.run(TOKEN)

