# etl/load.py
import os
import pandas as pd
from sqlalchemy import (
    create_engine, Table, Column,
    Integer, String, Float, DateTime, MetaData
)
from config.logger import setup_logger

logger = setup_logger()

# =========================
# 1️⃣ Connexion MySQL
# =========================
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST", "mysql")
engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
    echo=True  # affiche les requêtes SQL (debug)
)

metadata = MetaData()

# =========================
# 2️⃣ Définition de la table
# =========================
weather_table = Table(
    "weather_data",
    metadata,

    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("ville", String(50), nullable=False),
    Column("pays", String(5), nullable=False),

    Column("temp", Float),
    Column("temp_min", Float),
    Column("temp_max", Float),
    Column("humidite", Integer),
    Column("description", String(100)),
    Column("vitesse_vent", Float),

    Column("scrape_date", DateTime, nullable=False)
)

# =========================
# 3️⃣ Création de la table
# =========================
def create_table():
    logger.info("[LOAD] Creating table if not exists")
    metadata.create_all(engine)
    logger.info("[LOAD] Table ready")

# =========================
# 4️⃣ Chargement des données
# =========================
def load_to_db(df: pd.DataFrame):
    try:
        logger.info("[LOAD] Starting load to MySQL")

        df["scrape_date"] = pd.to_datetime(df["scrape_date"])

        df.to_sql(
            "weather_data",
            con=engine,
            if_exists="append",
            index=False,
            method="multi"
        )

        logger.info(f"[LOAD] {len(df)} rows inserted successfully")
        df.to_csv("data_clean/loaded_data.csv", index=False)
        df.to_json("data_clean/loaded_data.json", orient="records", lines=True)
    except Exception:
        logger.exception("[LOAD] Error during loading")
        raise


# =========================
# 🔥 TEST LOCAL UNIQUEMENT
# =========================
if __name__ == "__main__":
    create_table()

    df = pd.read_csv("data_clean/clean.csv")
    load_to_db(df)
