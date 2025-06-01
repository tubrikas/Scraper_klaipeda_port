# Klaipeda Port News Scraper

This project scrapes news articles from the [Port of Klaipeda Community News](https://portofklaipeda.lt/en/community/news) website and saves them into an Excel file for further analysis.

## Features

- Collects news article URLs across multiple pages
- Extracts each article’s title, date, and full text
- Saves data to Excel (.xlsx) in a /data folder
- Retries failed requests and waits between requests to be polite
- Logs scraping progress and errors to scraper.log for troubleshooting
- Easy configuration via config.py

## Usage

1. Clone the repository or copy the script files

2. Install the required libraries

3. In your terminal go to the root folder and run "python scraper.py"

## Requirements

- bs4==4.12.3
- python==3.13.2
- pandas==2.2.3
- requests==2.32.3
- openpyxl==3.1.5
