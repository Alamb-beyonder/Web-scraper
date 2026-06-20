from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time



driver = webdriver.Chrome()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
}

sitemap_response = requests.get("https://www.metacritic.com/games.xml", headers=headers)
sitemap_soup = BeautifulSoup(sitemap_response.text, "xml")
sub_sitemap_urls = sitemap_soup.find_all("loc")

sub_sitemap_response = requests.get(sub_sitemap_urls[0].text, headers=headers)
sub_sitemap_soup = BeautifulSoup(sub_sitemap_response.text, "xml")
game_urls = sub_sitemap_soup.find_all("loc")

results = []

#### TESTING ####

# test_urls = ["https://www.metacritic.com/game/the-witcher-3-wild-hunt/"]

#################

for url in game_urls:
    game_url = url.text
    driver.get(game_url)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    title = soup.title.text
    scores = {}
    wrappers = soup.find_all(attrs={"data-testid": "global-score-wrapper"})
    
    for wrapper in wrappers:  
        header_element = wrapper.find(attrs={"data-testid": "global-score-header"})
        value_element = wrapper.find(attrs={"data-testid": "global-score-value"})
        
        # handle games with no scores
        if header_element and value_element:
            header = header_element.text
            value = value_element.text
            if header not in scores:
                scores[header] = value

    results.append({"title": title, "score": scores})
    time.sleep(1)




