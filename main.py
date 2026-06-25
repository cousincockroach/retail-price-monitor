import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import DATABASE_PATH, PNP_SETTINGS
from src.database.db_manager import DatabaseManager
from src.scrapers.pnp_scraper import PnpScraper
from src.utils.helpers import clean_price, clean_text

def run_pipeline():
    print("=== [1] Starting Retail Price Monitor Pipeline ===")
    db = DatabaseManager(DATABASE_PATH)
    scraper = PnpScraper(PNP_SETTINGS)
    
    print("\n=== [2] Executing Browser Scraping Routine ===")
    raw_html = scraper.fetch_raw_html()
    raw_products = scraper.parse_specials(raw_html)
    
    if not raw_products:
        print("Pipeline halted: No data items resolved during scrape extraction.")
        return

    print(f"\n=== [3] Processing and Cleansing {len(raw_products)} Items ===")
    for item in raw_products:
        clean_name = clean_text(item["name"])
        curr_p = clean_price(item["current_price_raw"])
        old_p = clean_price(item["old_price_raw"])
        promo = clean_text(item["promotion"])
        
        db.save_or_update_product(
            product_id=item["id"],
            store="Pick n Pay",
            name=clean_name,
            current_p=curr_p,
            old_p=old_p,
            promo=promo
        )
        print(f"Upserted database record: {clean_name} | Price: R{curr_p}")

    print("\n=== [4] Data Ingestion Sequence Completed Successfully! ===")

if __name__ == "__main__":
    run_pipeline()