import os
import json
import requests

API_URL = "https://glitch-garage-api.speedsorcerer0.workers.dev/afk-presence"
STATE_FILE = "estado.json"


def cargar_estado():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            print("Error leyendo estado.json")
            return {"accounts": []}

    return {"accounts": []}


def guardar_estado(accounts):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {"accounts": accounts},
            f,
            indent=2,
            ensure_ascii=False
        )

    print("Estado guardado correctamente.")


def obtener_cuentas():
    print("Consultando cuentas...")

    r = requests.get(API_URL, timeout=20)
    r.raise_for_status()

    data = r.json()

    cuentas = []
    ids = []

    for cuenta in data.get("accounts", []):

        if not cuenta.get("online", False):
            continue

        if cuenta.get("console") != "Xbox Series":
            continue

        nombre = cuenta.get("onlineId", "Desconocido")
        aim = cuenta.get("aim", "Desconocido")
        uptime = cuenta.get("uptimePct", 0)

        banned = "🚫 Sí" if cuenta.get("banned") else "✅ No"

        ids.append(nombre)

        cuentas.append({
            "id": nombre,
            "mensaje":
                f"🟢 **Nueva cuenta detectada**\n\n"
                f"👤 **{nombre}**\n"
                f"🎯 Aim: {aim}\n"
                f"📈 Uptime: {uptime}%\n"
                f"🚫 Baneada: {banned}"
        })

    print(f"Cuentas online encontradas: {len(ids)}")

    return cuentas, ids


def enviar_discord(mensaje):
    webhook = os.getenv("DISCORD_WEBHOOK")

    if not webhook:
        print("ERROR: No existe DISCORD_WEBHOOK")
        return

    try:
        respuesta = requests.post(
            webhook,
            json={"content": mensaje},
            timeout=10
        )

        print(
            "Discord respuesta:",
            respuesta.status_code
        )

        if respuesta.status_code not in [200, 204]:
            print(respuesta.text)

    except Exception as e:
        print("Error enviando a Discord:", e)


# -------- PROGRAMA PRINCIPAL --------

estado = cargar_estado()

anteriores = set(
    estado.get("accounts", [])
)

print(
    "Cuentas guardadas anteriormente:",
    len(anteriores)
)

cuentas, actuales = obtener_cuentas()

actuales_set = set(actuales)

nuevas = [
    c for c in cuentas
    if c["id"] not in anteriores
]

eliminadas = anteriores - actuales_set


print("Nuevas:", len(nuevas))
print("Eliminadas:", len(eliminadas))


for cuenta in nuevas:
    enviar_discord(cuenta["mensaje"])


for cuenta in eliminadas:
    enviar_discord(
        f"🔴 **La cuenta ya no aparece online:**\n\n"
        f"👤 **{cuenta}**"
    )


if not nuevas and not eliminadas:
    print("No hubo cambios.")


guardar_estado(actuales)
