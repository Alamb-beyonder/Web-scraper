from bs4 import BeautifulSoup
from selenium import webdriver
import requests


driver = webdriver.Chrome()
url = "https://www.metacritic.com/game/the-witcher-3-wild-hunt/"
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
wrappers = soup.find_all(attrs={"data-testid": "global-score-wrapper"})
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
}

scores = {}

# response = requests.get(url, headers=headers)
# content = response.text
# index = content.find("1290")

for wrapper in wrappers:
    header = wrapper.find(attrs={"data-testid": "global-score-header"}).text
    value = wrapper.find(attrs={"data-testid": "global-score-value"}).text
    
    if header not in scores:
        scores[header] = value
    
print(scores)


