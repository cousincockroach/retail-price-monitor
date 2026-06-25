import re

def clean_price(price_string):
    """
    Transforms raw currency strings like ' R109.99/kg ' or 'R18.99' 
    into clean float metrics like 109.99 or 18.99.
    """
    if not price_string or price_string == "N/A":
        return None
    
    cleaned = re.sub(r'[^\d.]', '', price_string)
    
    try:
        return float(cleaned)
    except ValueError:
        return None

def clean_text(text):
    if not text:
        return ""
    return " ".join(text.split())