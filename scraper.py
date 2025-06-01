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

articles_data = []

for link in article_links:
    print(f"Scraping: {link}")
    response = requests.get(link)
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
    