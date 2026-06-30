from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request
import requests

from config import TELEGRAM_TOKEN
from dialogflow_service import detectar_intencion

app = Flask(__name__)

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


# 🟢 Ruta de prueba
@app.route("/", methods=["GET"])
def home():
    return "Bot activo 🚀"


# 🟢 Webhook principal de Telegram
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    print("\n==============================")
    print("📩 NUEVO MENSAJE RECIBIDO")
    print("==============================")
    print("DATA:", data)

    try:
        if "message" not in data:
            print("⚠️ Update sin mensaje")
            return "ok", 200

        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        print("👤 CHAT ID:", chat_id)
        print("💬 TEXTO:", text)

        if not text:
            print("⚠️ Mensaje vacío")
            return "ok", 200

        # 🧠 Dialogflow
        respuesta = detectar_intencion(text, session_id=str(chat_id))

        print("🤖 RESPUESTA DIAGFLOW:", respuesta)

        # 📤 Enviar a Telegram
        telegram_response = requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": respuesta
            }
        )

        print("📤 TELEGRAM STATUS:", telegram_response.status_code)

    except Exception as e:
        print("❌ ERROR EN WEBHOOK:", e)

    print("==============================\n")

    return "ok", 200


# 🟢 Ejecutar local
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)