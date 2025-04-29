import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import asyncio

async def scrape_static(url):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, requests.get, url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')

    head = soup.head.get_text(separator=' ', strip=True) if soup.head else ''
    body = soup.body.get_text(separator=' ', strip=True) if soup.body else ''
    links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]

    return {
        'header': head,
        'body': body,
        'links': links
    }
