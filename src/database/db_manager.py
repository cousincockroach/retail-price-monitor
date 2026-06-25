import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS product_prices (
                    id TEXT PRIMARY KEY,
                    store TEXT,
                    product_name TEXT,
                    current_price REAL,
                    old_price REAL,
                    promotion TEXT,
                    last_updated TEXT
                )
            """)
            conn.commit()

    def save_or_update_product(self, product_id, store, name, current_p, old_p, promo):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO product_prices (id, store, product_name, current_price, old_price, promotion, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    current_price = excluded.current_price,
                    old_price = excluded.old_price,
                    promotion = excluded.promotion,
                    last_updated = excluded.last_updated
            """, (product_id, store, name, current_p, old_p, promo, now))
            conn.commit()