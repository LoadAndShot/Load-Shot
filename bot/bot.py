import os
import discord
from discord import SyncWebhook
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # Si tu utilises un .env en local

# Récupération des variables d'environnement
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))
CHANNEL_LEGAL_ID = int(os.getenv('DISCORD_LEGAL_CHANNEL_ID'))
CHANNEL_ILLEGAL_ID = int(os.getenv('DISCORD_ILLEGAL_CHANNEL_ID'))
LEGAL_WEBHOOK = os.getenv('DISCORD_LEGAL_WEBHOOK')
ILLEGAL_WEBHOOK = os.getenv('DISCORD_ILLEGAL_WEBHOOK')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def send_order_notification(is_legal, username, product, quantity, delivery_method, phone_number, total_price):
    webhook_url = LEGAL_WEBHOOK if is_legal else ILLEGAL_WEBHOOK
    webhook = SyncWebhook.from_url(webhook_url)

    content = (
        f"**Nouvelle commande**\n"
        f"👤 Client : {username}\n"
        f"📦 Produit : {product}\n"
        f"🔢 Quantité : {quantity}\n"
        f"🚚 Livraison : {delivery_method}\n"
        f"📱 Numéro IG : {phone_number}\n"
        f"💸 Prix total : {total_price} €"
    )

    webhook.send(content=content)
