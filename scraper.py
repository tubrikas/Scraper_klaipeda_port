import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from config import base_url, max_pages, request_timeout, retry_limit, delay_between_requests

def make_request_with_retries(url, timeout, retries, delay):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except Exception as e:
            print(f"Request failed ({attempt+1}/{retries}) for {url}: {e}")
            attempt += 1
            if attempt < retries:
                time.sleep(delay)
    print(f"Giving up on {url} after {retries} retries.")
    return None

article_links = []

for page_number in range(1, max_pages + 1):
    url = base_url + "/" if page_number == 1 else f"{base_url}/page/{page_number}/"
    print(f"Scraping page {page_number}...")

    response = make_request_with_retries(url, request_timeout, retry_limit, delay_between_requests)
    if response is None:
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", class_="news-card", href=True)

    for link in links:
        article_links.append(link["href"])

    time.sleep(delay_between_requests)

    print(f"\nTotal collected article links: {len(article_links)}")

articles_data = []

for link in article_links:
    print(f"Scraping: {link}")
    response = make_request_with_retries(link, request_timeout, retry_limit, delay_between_requests)
    if response is None:
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    title_tag = soup.find("h1", class_="mb-4")
    title = title_tag.get_text(strip=True) if title_tag else "N/A"

    date_tag = soup.find("div", class_="text-grey mb-5")
    date = date_tag.get_text(strip=True) if date_tag else "N/A"

    text_block = soup.find("div", class_="fs-4")
    if text_block:
        paragraphs = text_block.find_all("p")
        full_text = "\n\n".join([p.get_text(strip=True) for p in paragraphs])
    else:
        full_text = "N/A"

    articles_data.append({"url": link, "title": title, "date": date, "text": full_text})

    time.sleep(delay_between_requests)
    
df = pd.DataFrame(articles_data)
df.to_excel('./data/klaipeda_port_scraper.xlsx', index=False)