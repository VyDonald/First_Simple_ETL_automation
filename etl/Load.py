# etl/load.py
import os
import sys
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import (
    create_engine, Table, Column,
    Integer, String, Float, DateTime, MetaData, text
)
from config.logger import setup_logger

logger = setup_logger()

# =========================
# 1️⃣ Connexion MySQL
# =========================
def get_engine():
    """Crée et retourne un SQLAlchemy engine en lisant les variables d'env au runtime."""
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")  # ✅ Corrigé
    DB_PORT = os.getenv("DB_PORT", "3306")       # ✅ Ajouté

    if not DB_PASSWORD:
        raise RuntimeError("❌ DB_PASSWORD is not set in environment")
    
    if not DB_NAME:
        raise RuntimeError("❌ DB_NAME is not set in environment")

    # ✅ Encode le password pour gérer @, !, espaces, etc.
    safe_password = quote_plus(DB_PASSWORD)

    url = f"mysql+pymysql://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    logger.info(f"[LOAD] Connecting to MySQL at {DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    return create_engine(url, echo=False, pool_pre_ping=True)  # echo=False pour moins de logs

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
    engine = get_engine()
    metadata.create_all(engine)
    logger.info("[LOAD] ✅ Table ready")

# =========================
# 4️⃣ Chargement des données
# =========================
def load_to_db(df: pd.DataFrame, check_duplicates=True):
    try:
        logger.info("[LOAD] Starting load to MySQL")

        if df.empty:
            logger.warning("[LOAD] DataFrame is empty, nothing to load")
            return

        df["scrape_date"] = pd.to_datetime(df["scrape_date"])

        engine = get_engine()
        
        # Vérifie doublons (optionnel)
        if check_duplicates:
            with engine.connect() as conn:
                check_date = df["scrape_date"].iloc[0]
                
                result = conn.execute(
                    text("SELECT COUNT(*) FROM weather_data WHERE DATE(scrape_date) = DATE(:date)"),
                    {"date": check_date}
                )
                count = result.scalar()
                
                if count > 0:
                    logger.warning(f"[LOAD] ⚠️  Found {count} existing rows for {check_date.date()}. Skipping to avoid duplicates.")
                    return
        
        # Insert
        df.to_sql(
            "weather_data",
            con=engine,
            if_exists="append",
            index=False,
            method="multi"
        )

        logger.info(f"[LOAD] ✅ {len(df)} rows inserted successfully")
        
        # Sauvegarde locale
        os.makedirs("data_clean", exist_ok=True)
        df.to_csv("data_clean/loaded_data.csv", index=False)
        df.to_json("data_clean/loaded_data.json", orient="records", lines=True)
        logger.info("[LOAD] ✅ Local backup saved")
        
    except Exception:
        logger.exception("[LOAD] ❌ Error during loading")
        raise


# =========================
# 🔥 TEST LOCAL
# =========================
if __name__ == "__main__":
    logger.info("[LOAD] Running in standalone mode")
    
    create_table()

    csv_path = "data_clean/clean.csv"
    
    if not os.path.exists(csv_path):
        logger.error(f"[LOAD] ❌ File not found: {csv_path}")
        sys.exit(1)
    
    df = pd.read_csv(csv_path)
    logger.info(f"[LOAD] Loaded {len(df)} rows from {csv_path}")
    
    if df.empty:
        logger.warning("[LOAD] DataFrame is empty, nothing to load")
        sys.exit(0)
    
    load_to_db(df)
    logger.info("[LOAD] ✅ Standalone load completed")