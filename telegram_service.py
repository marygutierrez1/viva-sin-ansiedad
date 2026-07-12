import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


def send_message(chat_id, text):
    url = f"{TELEGRAM_URL}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"❌ Error enviando mensaje a Telegram: {e}")
        return None