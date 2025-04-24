import os
import requests

def get_channel_ids():
    try:
        channel_legal = int(os.getenv('CHANNEL_LEGAL_ID'))
        channel_illegal = int(os.getenv('CHANNEL_ILLEGAL_ID'))
        return channel_legal, channel_illegal
    except (TypeError, ValueError):
        raise Exception("❌ Les variables d'environnement CHANNEL_LEGAL_ID ou CHANNEL_ILLEGAL_ID sont manquantes ou incorrectes !")

def send_order_notification(order, is_illegal=False, total_price=0):
    webhook_url = os.getenv('DISCORD_WEBHOOK_LEGAL') if not is_illegal else os.getenv('DISCORD_WEBHOOK_ILLEGAL')
    mention = "@TroTro" if not is_illegal else "@AladindeAuCurry"
    
    if not webhook_url:
        raise Exception("❌ Le webhook Discord n'est pas configuré correctement dans les variables d'environnement.")

    product_name = order.product.name
    quantity = order.quantity
    delivery_method = order.delivery_method
    phone_number = order.phone_number

    message = (
        f"📦 Nouvelle commande {'ILLÉGALE' if is_illegal else 'légale'} !\n"
        f"👤 Client : {order.user.username}\n"
        f"🛒 Produit : {product_name}\n"
        f"🔢 Quantité : {quantity}\n"
        f"🚚 Méthode : {delivery_method}\n"
        f"📱 Numéro IG : {phone_number}\n"
        f"💶 Prix total : {total_price} €\n"
        f"🔔 Mention : {mention}"
    )

    payload = {
        "content": message
    }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"❌ Erreur lors de l'envoi du message Discord : {e}")
