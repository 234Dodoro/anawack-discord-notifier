import os
import json
import requests

API_URL = "https://glitch-garage-api.speedsorcerer0.workers.dev/afk-presence"
STATE_FILE = "estado.json"


def cargar_estado():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {"accounts": []}
    return {"accounts": []}


def guardar_estado(accounts):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"accounts": accounts}, f, indent=2)


def obtener_cuentas():
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

    return cuentas, ids


estado = cargar_estado()
anteriores = set(estado.get("accounts", []))

cuentas, actuales = obtener_cuentas()
actuales_set = set(actuales)

nuevas = [c for c in cuentas if c["id"] not in anteriores]
eliminadas = anteriores - actuales_set

webhook = os.getenv("DISCORD_WEBHOOK")

if webhook:

    # Avisar cuentas nuevas
    for cuenta in nuevas:
        requests.post(webhook, json={"content": cuenta["mensaje"]})

    # Avisar cuentas eliminadas
    for cuenta in eliminadas:
        requests.post(
            webhook,
            json={
                "content": f"🔴 **La cuenta ya no aparece online:**\n\n👤 **{cuenta}**"
            }
        )

    if nuevas or eliminadas:
        print("Cambios detectados.")
    else:
        print("No hubo cambios.")

else:
    print("No existe la variable DISCORD_WEBHOOK.")

guardar_estado(actuales)
