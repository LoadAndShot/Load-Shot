import requests
from django.conf import settings

def send_discord_notification(message, webhook_url):
    if webhook_url:
        data = {"content": message}
        try:
            response = requests.post(webhook_url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de l'envoi du message Discord: {e}")
