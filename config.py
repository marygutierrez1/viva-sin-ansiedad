import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Token del bot de Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Proyecto de Dialogflow
DIALOGFLOW_PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")

# Ruta del archivo de credenciales de Google
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Nombre de la hoja de Google Sheets
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")

# Enlace del libro en Hotmart
HOTMART_LINK = os.getenv("HOTMART_LINK")