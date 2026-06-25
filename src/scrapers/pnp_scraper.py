import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

class PnpScraper:
    def __init__(self, config):
        self.url = config["url"]
        self.timeout = config["timeout"]
        self.user_agent = config["user_agent"]

    def fetch_raw_html(self):
        """Launches browser instance and returns structural HTML source."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=self.user_agent, viewport={"width": 1440, "height": 900})
            page = context.new_page()
            
            try:
                page.goto(self.url, wait_until="domcontentloaded")
                page.wait_for_selector("cx-page-slot", timeout=self.timeout)
                time.sleep(5)  # Await component assembly completion
                return page.content()
            except Exception as e:
                print(f"[Scraper Error] Connection failure or timeout on target page: {e}")
                return None
            finally:
                browser.close()
    def parse_specials(self, html_content):
        """Transforms standard HTML source into structured data nodes."""
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 🌟 FIX: Look for product item cards anywhere on the rendered layout!
        cards = soup.find_all('div', class_='product-grid-item')
        
        # Fallback if class names use a different format
        if not cards:
            cards = soup.find_all(class_=lambda x: x and 'product-grid-item' in x.lower())

        products_data = []
        print(f"[Scraper Debug] Extracted {len(cards)} raw cards from HTML layout payload.")

        for card in cards:
            name_tag = card.find('a', class_=lambda x: x and 'name' in x.lower()) or card.find('a')
            name = name_tag.get('title') or name_tag.get_text(strip=True) if name_tag else None
            
            if not name or name == "Unknown Product":
                continue

            # Capture unique identifier
            item_link = name_tag.get('href', '') if name_tag else ''
            product_id = item_link.split('/p/')[-1] if '/p/' in item_link else str(hash(name))

            # Price processing logic
            current_price = "N/A"
            old_price = "N/A"
            price_container = card.find('div', class_=lambda x: x and 'price' in x.lower())
            
            if price_container:
                old_tag = price_container.find('span', class_='old')
                if old_tag:
                    old_price = old_tag.get_text(strip=True)
                    current_price = price_container.get_text(strip=True).replace(old_price, "").strip()
                else:
                    current_price = price_container.get_text(strip=True)

            promo_tag = card.find('a', id='promotion') or card.find(class_=lambda x: x and 'promo' in x.lower())
            promotion = promo_tag.get_text(strip=True) if promo_tag else "None"

            products_data.append({
                "id": product_id,
                "name": name,
                "current_price_raw": current_price,
                "old_price_raw": old_price,
                "promotion": promotion
            })
            
        return products_data