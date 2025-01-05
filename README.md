# Crawler for Base URL; only crawl webpages on the base URL

This project is a web crawler designed to scrape and crawl links within a specified base URL. The tool is configured to work on `https://books.toscrape.com/`, a demo website for web scraping practice, ensuring compliance with ethical and permitted scraping.

## Features

- **Multi-threaded crawling**: Efficiently processes multiple URLs concurrently using worker threads.
- **Queue management**: Maintains a list of URLs to crawl (`queue.txt`) and already visited URLs (`crawled.txt`).
- **Domain restriction**: Ensures that only links within the specified base URL are crawled, preventing unintended external requests.
- **Customizable ChromeDriver setup**: Allows flexibility in using Selenium for handling dynamic pages.
- **Static website support**: Efficiently handles crawling for websites with limited dynamic content.

## Requirements

- Python 3.x
- Selenium
- BeautifulSoup4
- ChromeDriver (Update the CHROMEDRIVER_PATH variable in main.py with the path to your ChromeDriver executable).

