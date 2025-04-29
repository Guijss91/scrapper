import asyncio
import re
from urllib.parse import urljoin, urlparse
import aiohttp
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Função para extrair informações estáticas
async def scrape_static(session, url, fields):
    try:
        async with session.get(url, timeout=10) as response:
            text = await response.text()
            soup = BeautifulSoup(text, 'html.parser')

            header = soup.title.string if soup.title else ''
            body = soup.get_text(separator=' ', strip=True) if soup.body else ''
            links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]

            result = {}
            if not fields or "header" in fields:
                result["header"] = header
            if not fields or "body" in fields:
                result["body"] = body
            if not fields or "links" in fields:
                result["links"] = links

            result["source"] = url

            return result
    except Exception as e:
        return {"error": str(e), "source": url}

# Função para extrair informações dinâmicas (lidando com Cloudflare)
def scrape_dynamic(url, fields):
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=options, use_subprocess=True)

    try:
        driver.get(url)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(3)
        except Exception as e:
            print(f"Timeout esperando carregamento: {e}")

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        header = soup.title.string if soup.title else ''
        body = soup.get_text(separator=' ', strip=True) if soup.body else ''
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]

        result = {}
        if not fields or "header" in fields:
            result["header"] = header
        if not fields or "body" in fields:
            result["body"] = body
        if not fields or "links" in fields:
            result["links"] = links

        result["source"] = url

        return result
    except Exception as e:
        return {"error": str(e), "source": url}
    finally:
        driver.quit()

# Função principal para orquestrar a raspagem
async def crawl(url, fields=None, follow_links=0, ignore_external=True, depth=1):
    parsed_root = urlparse(url)
    root_domain = parsed_root.netloc

    session = aiohttp.ClientSession()

    main_page = await scrape_static(session, url, fields)

    if 'error' in main_page or "Just a moment" in main_page.get('body', ''):
        main_page = scrape_dynamic(url, fields)

    followed_links = []

    if follow_links > 0 and 'links' in main_page:
        tasks = []
        for link in main_page['links']:
            if ignore_external:
                if urlparse(link).netloc != root_domain:
                    continue
            tasks.append(scrape_static(session, link, fields))
            if len(tasks) >= follow_links:
                break
        followed_links = await asyncio.gather(*tasks)

    await session.close()

    return {
        'main_page': main_page,
        'followed_links': followed_links
    }
