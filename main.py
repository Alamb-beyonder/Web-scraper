from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import csv

driver = webdriver.Chrome()

# Present itself as a user
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
}

# Crawl through first bunch of sitemaps
sitemap_response = requests.get("https://www.metacritic.com/games.xml", headers=headers)
sitemap_soup = BeautifulSoup(sitemap_response.text, "xml")
sub_sitemap_urls = sitemap_soup.find_all("loc")

# Crawl through second bunch of sitemaps - First in this case
sub_sitemap_response = requests.get(sub_sitemap_urls[0].text, headers=headers)
sub_sitemap_soup = BeautifulSoup(sub_sitemap_response.text, "xml")
game_urls = sub_sitemap_soup.find_all("loc")

results = []

#### TESTING ####

# test_urls = ["https://www.metacritic.com/game/the-witcher-3-wild-hunt/"]

#################

for url in game_urls[10:20]:
    game_url = url.text

    try:
        driver.get(game_url)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        title = soup.title.text.replace(" Reviews - Metacritic", "")
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
    except Exception as e:
        print(f"Failed on {game_url}: {e}")
        
    time.sleep(1)


# Write to CSV

with open("metacritic_scores.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Metascore", "User Score"])

    for result in results:
        title = result["title"]
        metascore = result["score"].get("Metascore", "N/A") # Use .get instead of just result["scores"]["Metascore"] for crash handling
        user_score = result["score"].get("User Score", "N/A")
        writer.writerow([title, metascore, user_score])


