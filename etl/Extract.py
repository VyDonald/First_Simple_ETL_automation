# etl/extract.py
import json
import logging
import os
import requests
import pandas as pd
logger = logging.getLogger("scraper")
from config.logger import setup_logger

setup_logger()
logger.info("Logger configured.")

def extract_data():
    try:
        API_KEY = os.getenv("API_KEY")
        cities = ["Ouagadougou", "New York", "Londres", "Tokyo", "Sydney"]
        print("[EXTRACT] Starting extraction...")
        rows = []
        for city in cities:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            if response.status_code == 200:
                data = response.json()
                with open(f"data/{city}.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                logger.info(f"Data for {city}: {data}")
        
    except requests.RequestException as e:
        logger.error(f"[EXTRACT] Error during extraction: {e}")
        return None

# 🔥 TEST LOCAL UNIQUEMENT
if __name__ == "__main__":
    with open("data/Ouagadougou.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    print("[EXTRACT] Sample data:")    
    print(data)