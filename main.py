from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from urllib3.exceptions import ProtocolError, NewConnectionError
import requests
import time
import csv
import os

driver = webdriver.Chrome()

# Present itself as a user
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
}

# Crawl through first bunch of sitemaps
sitemap_response = requests.get("https://www.metacritic.com/games.xml", headers=headers)
sitemap_soup = BeautifulSoup(sitemap_response.text, "xml")
sub_sitemap_urls = sitemap_soup.find_all("loc")

# Crawl through second bunch of sitemaps - First sitemap in this case
sub_sitemap_response = requests.get(sub_sitemap_urls[0].text, headers=headers)
sub_sitemap_soup = BeautifulSoup(sub_sitemap_response.text, "xml")
game_urls = sub_sitemap_soup.find_all("loc")

results = []

#### TESTING ####

# test_urls = ["https://www.metacritic.com/game/the-witcher-3-wild-hunt/"]

#################

# Catch up logic
existing_titles = set()
if os.path.exists("metacritic_scores.csv"):
    with open("metacritic_scores.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            existing_titles.add(row[0])


# Main scraping logic
for url in game_urls[:100]:
    game_url = url.text

    try:
        driver.get(game_url)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        title = soup.title.text.replace(" Reviews - Metacritic", "")

        if title in existing_titles:
            print(f"Already scraped {title} - SKIPPED")
            continue
        
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

        #Write to CSV
        metascore = scores.get("Metascore", "N/A") # Use .get instead of just result["scores"]["Metascore"] for crash handling
        user_score = scores.get("User Score", "N/A")

        with open("metacritic_scores.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([title, metascore, user_score])

        existing_titles.add(title)
        print(f"{title}, Metascore - {metascore}, User Score - {user_score}")

    except (WebDriverException, ProtocolError, NewConnectionError, ConnectionResetError) as e:
        print(f"Browser crashed on {game_url}, restarting driver: {e}")
        try:
            driver.quit()
        except Exception:
            pass
        driver = webdriver.Chrome()
        continue
    
    except Exception as e:
        print(f"Failed on {game_url}: {e}")
        
    time.sleep(1)

driver.quit()
print("Scraping complete")



