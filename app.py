from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, request
import requests

from config import TELEGRAM_TOKEN
from dialogflow_service import detectar_intencion
from sheets_service import guardar_usuario, actualizar_estado
from telegram_service import send_message

app = Flask(__name__)

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
PSICOLOGO_CHAT_ID = os.getenv("PSICOLOGO_CHAT_ID")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")


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
        nombre = data["message"]["chat"].get("first_name", "Sin nombre")
        username = data["message"]["chat"].get("username", "Sin username")

        print("👤 CHAT ID:", chat_id)
        print("💬 TEXTO:", text)
        guardar_usuario(
            chat_id,
            nombre,
            username,
            "Nuevo"
)

        if not text:
            print("⚠️ Mensaje vacío")
            return "ok", 200

        # 🧠 Dialogflow
        respuesta = detectar_intencion(text, session_id=str(chat_id))

        mensaje = respuesta["mensaje"]
        intent = respuesta["intent"]

        print("========================")
        print("RESPUESTA COMPLETA:")
        print(respuesta)
        print("INTENT:", repr(intent))
        print("========================")
        
        print("🤖 RESPUESTA DIALOGFLOW:", mensaje)
        print("🎯 INTENT DETECTADO:", intent)

        if "Psicologo_Online" in intent and "yes" in intent:
         print("🚀 ENTRÓ AL FLUJO DE PSICÓLOGO")
  
         actualizar_estado(chat_id, "Pendiente Psicólogo")
        
         mensaje_psicologo = f"""
        🚨 Nuevo usuario derivado

        👤 Nombre: {nombre}
        🆔 Chat ID: {chat_id}
        📱 Usuario: @{username}

        El usuario ha solicitado atención psicológica.
       """

         mensaje_admin = f"""
        🔔 Nueva solicitud de atención psicológica

        👤 Usuario: {nombre}
        🆔 Telegram ID: {chat_id}
        📱 Username: @{username}

        Estado: Pendiente Psicólogo
        """
         
         send_message(PSICOLOGO_CHAT_ID, mensaje_psicologo)
         send_message(ADMIN_CHAT_ID, mensaje_admin)

         print("📨 Notificación enviada al psicólogo:", PSICOLOGO_CHAT_ID)
         print("📨 Notificación enviada al administrador:", ADMIN_CHAT_ID)
       
        # 📤 Enviar respuesta a Telegram
        telegram_response = requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": mensaje
            }
        )

        print("📤 TELEGRAM STATUS:", telegram_response.status_code)
        print("📤 RESPUESTA TELEGRAM:", telegram_response.text)

    except Exception as e:
        print("❌ ERROR EN WEBHOOK:", e)

    print("==============================\n")

    return "ok", 200


# 🟢 Ejecutar la aplicación
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)