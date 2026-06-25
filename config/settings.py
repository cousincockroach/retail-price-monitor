import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE_PATH = os.path.join(DATA_DIR, "retail_catalog.db")

os.makedirs(DATA_DIR, exist_ok=True)

PNP_SETTINGS = {
    "url": "https://www.pnp.co.za/online-specials",
    "timeout": 15000,
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}