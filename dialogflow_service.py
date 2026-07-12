import os
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")
print("PROJECT_ID =", PROJECT_ID)

# 🟢 Cargar credenciales desde archivo JSON local
GOOGLE_CREDENTIALS_FILE = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS"
)

credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_CREDENTIALS_FILE
)
print("✅ Credenciales de Google cargadas correctamente")

def detectar_intencion(texto, session_id):
    """
    Envía el mensaje a Dialogflow y obtiene la respuesta del bot
    usando una sesión única por usuario (chat_id de Telegram).
    """

    try:
        # 🟢 Cliente con credenciales de Render
        session_client = dialogflow.SessionsClient(credentials=credentials)

        session = session_client.session_path(PROJECT_ID, session_id)

        text_input = dialogflow.TextInput(
            text=texto,
            language_code="es"
        )

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={
                "session": session,
                "query_input": query_input
            }
        )

        return {
    "mensaje": response.query_result.fulfillment_text,
    "intent": response.query_result.intent.display_name
}

    except Exception as e:
        print("❌ Error Dialogflow:", e)
        return "💙 Lo siento, ocurrió un error interno. Intenta nuevamente."