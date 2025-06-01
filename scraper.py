import requests
from bs4 import BeautifulSoup

base_url = "https://portofklaipeda.lt/en/community/news"
max_pages = 5
article_links = []

for page_number in range(1, max_pages + 1):
    url = base_url + "/" if page_number == 1 else f"{base_url}/page/{page_number}/"
    print(f"Scraping page {page_number}...")

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a", class_="news-card", href=True)

    for link in links:
        article_links.append(link["href"])

print(f"\nTotal collected article links: {len(article_links)}")
