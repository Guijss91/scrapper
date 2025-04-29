def scrape_dynamic(url, fields):
    import time
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import undetected_chromedriver as uc

    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=options, use_subprocess=True)

    try:
        driver.get(url)

        # Espera o carregamento real da página (não o challenge)
        try:
            # Espera até que um elemento que indique que a página carregou apareça
            # Você pode ajustar isso dependendo do site que está raspando
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(3)  # Espera adicional para estabilizar a página
        except Exception as e:
            print(f"Timeout esperando carregamento real: {e}")

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        header = soup.title.string if soup.title else ''
        body = soup.get_text(separator=' ', strip=True) if soup.body else ''
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]

        return {
            'url': url,
            'header': header,
            'body': body,
            'links': links
        }
    except Exception as e:
        return {'error': str(e), 'url': url}
    finally:
        driver.quit()
