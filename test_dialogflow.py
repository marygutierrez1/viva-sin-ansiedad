from dotenv import load_dotenv
load_dotenv()

from dialogflow_service import detectar_intencion

texto = "hola"

respuesta = detectar_intencion(texto)

print("Usuario:", texto)
print("Bot:", respuesta)