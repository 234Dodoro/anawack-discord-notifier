import os
import requests
from bs4 import BeautifulSoup

URL = "https://gtaglitches.com/afk-accounts"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)

print("Estado:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

titulo = soup.title.text if soup.title else "Sin título"
print(titulo)

webhook_url = os.environ.get("DISCORD_WEBHOOK")

if webhook_url:
    mensaje = {
        "content": f"🔔 Monitor AFK\nEstado: {response.status_code}\nTítulo: {titulo}"
    }

    resultado = requests.post(webhook_url, json=mensaje)

    print("Discord:", resultado.status_code)
else:
    print("❌ No se encontró DISCORD_WEBHOOK")
