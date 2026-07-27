import os
import requests
from playwright.sync_api import sync_playwright

URL = "https://gtaglitches.com/afk-accounts"

def obtener_cuentas():
    cuentas = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(5000)

        texto = page.locator("body").inner_text()

        for linea in texto.splitlines():
            linea = linea.strip()

            if (
                linea
                and "ONLINE" not in linea
                and "Xbox" not in linea
                and "Grand Theft Auto V" not in linea
                and "Assisted Aim" not in linea
                and "Free Aim" not in linea
                and len(linea) > 2
            ):
                if linea[0].isalnum():
                    cuentas.append(linea)

        browser.close()

    # Quitar duplicados
    resultado = []
    for c in cuentas:
        if c not in resultado:
            resultado.append(c)

    return resultado[:20]


cuentas = obtener_cuentas()

mensaje = "🟢 **Cuentas AFK Online**\n\n"

if cuentas:
    for cuenta in cuentas:
        mensaje += f"• {cuenta}\n"
else:
    mensaje += "No se encontraron cuentas."

webhook = os.getenv("DISCORD_WEBHOOK")

if webhook:
    requests.post(webhook, json={"content": mensaje})
    print("Mensaje enviado a Discord.")
else:
    print("No existe DISCORD_WEBHOOK.")
