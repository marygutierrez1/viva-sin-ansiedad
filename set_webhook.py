import requests
from config import TELEGRAM_TOKEN

# Cambia esta URL solo cuando cambie tu ngrok o Render
WEBHOOK_URL = "https://viva-sin-ansiedad.onrender.com/webhook"

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"

respuesta = requests.post(url, json={
    "url": WEBHOOK_URL
})

print(respuesta.json())