import json
import os
import pandas as pd
from config.logger import setup_logger
from datetime import datetime
logger = setup_logger()

RAW_DIR = "data"

def load_data():
    logger.info("[TRANSFORM] Starting transformation")

    rows = []

    for file in os.listdir(RAW_DIR):
        if not file.endswith(".json"):
            continue

        with open(os.path.join(RAW_DIR, file), "r") as f:
            data = json.load(f)

        try:
            rows.append({
                "ville": data["name"],
                "pays": data["sys"]["country"],
                "temp": data["main"]["temp"],
                "temp_min": data["main"]["temp_min"],
                "temp_max": data["main"]["temp_max"],
                "humidite": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "vitesse_vent": data["wind"]["speed"]
            })
        except KeyError as e:
            logger.error(f"[TRANSFORM] Missing key in {file}: {e}")

    df = pd.DataFrame(rows)
    logger.info(f"[TRANSFORM] DataFrame created with shape {df.shape}")

    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        logger.info("[TRANSFORM] Starting transformation")

        before = df.shape[0]

        df = df.drop_duplicates()
        df = df.dropna(subset=["temp", "humidite"])

        numeric_cols = [
            "temp", "temp_min", "temp_max",
            "humidite", "vitesse_vent"
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df["scrape_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        after = df.shape[0]
        logger.info(f"[TRANSFORM] Rows before: {before} → after: {after}")

        df.to_csv("data_clean/clean.csv", index=False)
        logger.info("[TRANSFORM] Cleaned data saved to clean.csv")
        return df

    except Exception as e:
        logger.exception("[TRANSFORM] Error during transformation")
        raise

# 🔥 TEST LOCAL UNIQUEMENT
if __name__ == "__main__":
    df_raw = load_data()
    df_clean = transform_data(df_raw)
    print(df_clean.head())
    