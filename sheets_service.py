import gspread
from google.oauth2.service_account import Credentials

# Permisos necesarios
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Ruta del archivo JSON de la cuenta de servicio
SERVICE_ACCOUNT_FILE = "vidasinansiedadbot-n9fd-56ae7cd5437d.json"  # Cambia el nombre si tu archivo tiene otro

# Autenticación
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

client = gspread.authorize(credentials)

# Abrir la hoja por nombre
spreadsheet = client.open("Viva sin Ansiedad - Desarrollo")

# Seleccionar la primera pestaña
sheet = spreadsheet.sheet1

print("✅ Conexión con Google Sheets exitosa")
print(sheet.title)
def buscar_usuario(telegram_id):
    """
    Busca un usuario por su Telegram ID.
    Devuelve el número de fila si existe.
    Devuelve None si no existe.
    """

    registros = sheet.get_all_values()

    # Empezamos desde la fila 2 porque la fila 1 es el encabezado
    for fila in range(2, len(registros) + 1):

        if str(registros[fila - 1][1]) == str(telegram_id):
            return fila

    return None

def guardar_usuario(telegram_id, nombre, username, estado):

    from datetime import datetime

    # Verificar si el usuario ya existe
    fila = buscar_usuario(telegram_id)

    if fila:
        print("ℹ️ Usuario ya registrado")
        return False

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    datos = [
        fecha,
        telegram_id,
        nombre,
        username,
        estado
    ]

    sheet.append_row(datos)

    print("✅ Usuario registrado por primera vez")
    print("📄 DATOS ENVIADOS A SHEET:", datos)

    return True

def actualizar_estado(telegram_id, nuevo_estado):
    """
    Actualiza el estado de un usuario existente.
    """

    fila = buscar_usuario(telegram_id)

    if fila:
        sheet.update_cell(fila, 5, nuevo_estado)
        print("✅ Estado actualizado:", nuevo_estado)
        return True

    print("⚠️ Usuario no encontrado")
    return False



