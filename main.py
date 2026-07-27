import requests
from bs4 import BeautifulSoup

URL = "https://gtaglitches.com/afk-accounts"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)

print("Estado:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print(soup.title.text)
