# bot.py - Bot Discord pour envoyer les nouvelles commandes dans les channels appropriés
import os
import django
import discord
from discord.ext import tasks

# Configuration de Django pour accéder aux modèles depuis ce script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loadshot.settings')
django.setup()
from orders.models import Order

# Récupération des informations sensibles depuis les variables d'environnement
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
DISCORD_GUILD_ID = int(os.environ.get('DISCORD_GUILD_ID', 0))
DISCORD_LEGAL_CHANNEL_ID = int(os.environ.get('DISCORD_LEGAL_CHANNEL_ID', 0))
DISCORD_ILLEGAL_CHANNEL_ID = int(os.environ.get('DISCORD_ILLEGAL_CHANNEL_ID', 0))

# Initialisation du client Discord avec les intents nécessaires
intents = discord.Intents.default()
intents.guilds = True  # avoir accès aux informations des guildes (serveurs)
client = discord.Client(intents=intents)

# Tâche périodique pour vérifier les nouvelles commandes et les envoyer sur Discord
@tasks.loop(seconds=5)
async def send_new_orders():
    # Récupérer les commandes non encore envoyées sur Discord
    unsent_orders = Order.objects.filter(sent_to_discord=False)
    for order in unsent_orders:
        try:
            # Sélectionner le channel en fonction du type de produit
            if order.product_type == 'legal':
                channel_id = DISCORD_LEGAL_CHANNEL_ID
            else:
                channel_id = DISCORD_ILLEGAL_CHANNEL_ID
            channel = client.get_channel(channel_id)
            if channel is None:
                # Si le channel n'est pas en cache, on le récupère via l'API Discord
                channel = await client.fetch_channel(channel_id)
            # Construire le message décrivant la commande
            message = (
                f"**Nouvelle commande #{order.id}**\n"
                f"Utilisateur: {order.user.username}\n"
                f"Type: {order.get_product_type_display()}\n"
                f"Méthode: {order.get_method_display()}\n"
                f"Date: {order.created_at.strftime('%d/%m/%Y %H:%M')}"
            )
            # Envoyer le message sur le channel Discord approprié
            await channel.send(message)
            # Marquer la commande comme envoyée
            order.sent_to_discord = True
            order.save(update_fields=['sent_to_discord'])
            print(f"Commande #{order.id} envoyée sur Discord.")
        except Exception as e:
            print(f"Erreur lors de l'envoi de la commande #{order.id} : {e}")

@client.event
async def on_ready():
    # Cette fonction est appelée quand le bot a réussi à se connecter à Discord
    print(f"Bot connecté en tant que {client.user}")
    # Vérifier la connexion au serveur Discord spécifié
    if DISCORD_GUILD_ID:
        guild = client.get_guild(DISCORD_GUILD_ID)
        if guild:
            print(f"Connecté au serveur : {guild.name} (ID: {guild.id})")
        else:
            print("Attention : le bot n'est pas présent dans la guilde spécifiée.")
    # Démarrer la boucle de vérification des commandes
    send_new_orders.start()

if __name__ == '__main__':
    if not DISCORD_TOKEN:
        print("ERREUR : Le token du bot Discord (DISCORD_TOKEN) n'est pas défini dans les variables d'environnement.")
    else:
        client.run(DISCORD_TOKEN)
