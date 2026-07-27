import os
import requests

API_URL = "https://glitch-garage-api.speedsorcerer0.workers.dev/afk-presence"

def obtener_cuentas():
    r = requests.get(API_URL, timeout=20)
    r.raise_for_status()

    data = r.json()

    cuentas = []

    for cuenta in data.get("accounts", []):
        if not cuenta.get("online", False):
            continue

        if cuenta.get("console") != "Xbox Series":
            continue

        nombre = cuenta.get("onlineId", "Desconocido")
        aim = cuenta.get("aim", "Desconocido")
        uptime = cuenta.get("uptimePct", 0)
        banned = "🚫 Sí" if cuenta.get("banned") else "✅ No"

        cuentas.append(
            f"• **{nombre}**\n"
            f"  🎯 Aim: {aim}\n"
            f"  📈 Uptime: {uptime}%\n"
            f"  🚫 Baneada: {banned}\n"
        )

    return cuentas, data.get("updatedAt", "Desconocido")


cuentas, actualizado = obtener_cuentas()

mensaje = "🟢 **CUENTAS AFK XBOX SERIES ONLINE**\n\n"

if cuentas:
    mensaje += "\n".join(cuentas)
else:
    mensaje += "❌ No hay cuentas Xbox Series online."

mensaje += f"\n\n🕒 **Actualizado:** {actualizado}"

webhook = os.getenv("DISCORD_WEBHOOK")

if webhook:
    respuesta = requests.post(webhook, json={"content": mensaje})

    if respuesta.status_code in (200, 204):
        print("Mensaje enviado correctamente.")
    else:
        print(f"Error al enviar: {respuesta.status_code}")
        print(respuesta.text)
else:
    print("No existe la variable DISCORD_WEBHOOK.")
