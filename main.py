from bs4 import BeautifulSoup
import requests

url = "https://www.metacritic.com/game/sawi-the-voidbuster/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

content = response.text
index = content.find("1290")
print(content[index-100:index+300])