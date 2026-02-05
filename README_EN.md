# 🌍 First Data Project - Weather ETL Pipeline

> **A complete ETL pipeline to extract, transform and load weather data from 5 cities around the world into a MySQL database**

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [✨ Features](#-features)
- [🏗️ Architecture](#-architecture)
- [📦 Installation](#-installation)
- [🚀 Usage](#-usage)
- [📂 Project Structure](#-project-structure)
- [🔄 ETL Pipeline](#-etl-pipeline)
- [🛠️ Configuration](#-configuration)
- [📊 Data](#-data)
- [🐛 Troubleshooting](#-troubleshooting)
- [📝 License](#-license)

---

## 🎯 Overview

This project implements an automated **ETL (Extract, Transform, Load) pipeline** to:

✅ **Extract** real-time weather data from the OpenWeatherMap API
✅ **Transform** raw data to clean and normalize it
✅ **Load** transformed data into a MySQL database

The pipeline handles errors gracefully, saves data locally in CSV/JSON format, and includes a comprehensive logging system.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🌐 **API Extraction** | Fetches weather data from OpenWeatherMap for 5 major cities |
| 🧹 **Data Cleaning** | Removes duplicates, handles missing values |
| 📊 **Transformation** | Normalizes temperature units, structures data |
| 💾 **Multi-format Storage** | Saves in CSV, JSON and MySQL |
| 📝 **Detailed Logging** | Records all pipeline steps |
| ⚡ **Error Handling** | Graceful fallback if database is unavailable |
| 🔐 **Secure Configuration** | Credentials stored in environment variables |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              MAIN.PY - Orchestrator                 │
└──────────┬──────────────────────────────┬───────────┘
           │                              │
    ┌──────▼────────┐            ┌────────▼──────────┐
    │  EXTRACT      │            │   TRANSFORM       │
    │  - API Call   │            │   - Cleaning      │
    │  - JSON Save  │            │   - Normalization │
    └───────┬───────┘            └────────┬──────────┘
            │                             │
            └─────────────┬───────────────┘
                          │
                    ┌─────▼────────┐
                    │    LOAD      │
                    │  - MySQL DB  │
                    │  - CSV/JSON  │
                    └──────────────┘
```

---

## 📦 Installation

### 📋 Prerequisites

- **Python** 3.8+
- **MySQL Server** 5.7+ (optional for local backup)
- **pip** (Python package manager)

### 🔧 Step 1: Clone the repository

```bash
git clone <your-repo>
cd First_Data_Project
```

### 🔧 Step 2: Create a virtual environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 🔧 Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### 🔧 Step 4: Set up environment variables

Create a `.env` file at the project root (optional):

```env
DB_USER=davy
DB_PASSWORD=password123
DB_HOST=localhost
DB_NAME=First_Data
API_KEY=21df4d73e5dc83ea09d6f0ed3148d2bc
```

### 🔧 Step 5: Configure MySQL (optional)

```bash
# Check MySQL status
sudo systemctl status mysql

# Start MySQL if needed
sudo systemctl start mysql

# Create the database
mysql -u root -p
> CREATE DATABASE First_Data;
```

---

## 🚀 Usage

### ▶️ Run the complete pipeline

```bash
python main.py
```

**Expected output:**
```
2026-02-04 23:31:25,222 - INFO - Logger configured.
[EXTRACT] Starting extraction...
2026-02-04 23:32:14,137 - INFO - Data for Ouagadougou: {...}
...
2026-02-04 23:32:15,357 - INFO - [TRANSFORM] Cleaned data saved to clean.csv
2026-02-04 23:32:15,662 - INFO - Data loaded successfully
```

### ▶️ Run extraction only

```bash
python -m etl.Extract
```

### ▶️ Run transformation only

```bash
python -m etl.Transform
```

### ▶️ Run loading only

```bash
python -m etl.Load
```

---

## 📂 Project Structure

```
First_Data_Project/
│
├── 📄 main.py                 # Main entry point
├── 📄 requirements.txt         # Project dependencies
├── 📄 README.md               # French documentation
├── 📄 README_EN.md            # English documentation
│
├── 📁 config/                 # Configuration
│   ├── __init__.py
│   └── logger.py              # Logging configuration
│
├── 📁 etl/                    # ETL Pipeline
│   ├── __init__.py
│   ├── Extract.py             # Extraction step (API)
│   ├── Transform.py           # Transformation step (cleaning)
│   └── Load.py                # Loading step (Database)
│
├── 📁 data/                   # Raw data (JSON)
│   ├── Ouagadougou.json
│   ├── New York.json
│   ├── Londres.json
│   ├── Tokyo.json
│   └── Sydney.json
│
├── 📁 data_clean/             # Transformed data
│   ├── clean.csv              # Cleaned data (CSV)
│   ├── loaded_data.csv        # Loaded data (CSV)
│   ├── loaded_data.json       # Loaded data (JSON)
│   └── requètes.sql           # Sample SQL queries
│
└── 📁 logs/                   # Log files
    └── app.log                # Pipeline logs
```

---

## 🔄 ETL Pipeline

### **1️⃣ EXTRACT Phase - Data Extraction**

**File:** [etl/Extract.py](etl/Extract.py)

📡 **Fetches weather data** from OpenWeatherMap API for 5 cities:
- 🌍 Ouagadougou (Burkina Faso)
- 🌃 New York (USA)
- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 London (UK)
- 🗾 Tokyo (Japan)
- 🦘 Sydney (Australia)

**Extracted data:**
```json
{
  "name": "Ouagadougou",
  "sys": {"country": "BF"},
  "main": {
    "temp": 300.22,
    "temp_min": 300.22,
    "temp_max": 300.22,
    "humidity": 17
  },
  "weather": [{"description": "clear sky"}],
  "wind": {"speed": 2.57}
}
```

**Actions:**
- ✅ API call with error handling
- ✅ Save to JSON files
- ✅ Detailed logging of each step

---

### **2️⃣ TRANSFORM Phase - Data Transformation**

**File:** [etl/Transform.py](etl/Transform.py)

🧹 **Cleans and normalizes** raw data:

**Process:**
1. **Load** JSON files from `/data`
2. **Extract** relevant fields
3. **Remove duplicates** with `drop_duplicates()`
4. **Handle missing values** with `dropna()`
5. **Convert types** to numeric
6. **Add timestamp** (scrape date)
7. **Save** to CSV for verification

**Transformed data:**
```
     city     country   temp  temp_min  temp_max  humidity           description  wind_speed         scrape_date
0  Ouagadougou   BF  300.22    300.22    300.22        17           clear sky           2.57  2026-02-04 23:32:15
1    New York   US  273.53    271.46    274.13        36           clear sky           4.12  2026-02-04 23:32:15
2     London   GB  281.19    280.32    281.82        84      broken clouds           8.23  2026-02-04 23:32:15
3      Tokyo   JP  278.48    276.82    279.94        56        few clouds           2.57  2026-02-04 23:32:15
4     Sydney   AU  301.61    300.76    303.12        58           clear sky           4.12  2026-02-04 23:32:15
```

**Applied improvements:**
- ✅ Remove rows with missing temperature or humidity
- ✅ Normalize data types
- ✅ Add universal timestamp
- ✅ Data validation

---

### **3️⃣ LOAD Phase - Data Loading**

**File:** [etl/Load.py](etl/Load.py)

💾 **Loads transformed data** into MySQL database

**Database architecture:**
```sql
CREATE TABLE weather_data (
  id INT PRIMARY KEY AUTO_INCREMENT,
  ville VARCHAR(50) NOT NULL,
  pays VARCHAR(5) NOT NULL,
  temp FLOAT,
  temp_min FLOAT,
  temp_max FLOAT,
  humidite INT,
  description VARCHAR(100),
  vitesse_vent FLOAT,
  scrape_date DATETIME NOT NULL
);
```

**Actions:**
- ✅ Create table if it doesn't exist
- ✅ Insert data with `APPEND` mode
- ✅ Backup save to CSV and JSON
- ✅ Handle connection errors

**Fallback:** If MySQL is unavailable, data is saved locally in CSV/JSON

---

## 🛠️ Configuration

### 📝 Logger Configuration

**File:** [config/logger.py](config/logger.py)

```python
import logging

def setup_logger():
    logger = logging.getLogger("etl_pipeline")
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
```

### 📋 Dependencies

**File:** [requirements.txt](requirements.txt)

```
pandas==3.0.0
numpy==2.4.2
requests==2.32.5
sqlalchemy==2.0.46
pymysql==1.1.2
beautifulsoup4==4.14.3
pyyaml==6.0.3
```

Installation:
```bash
pip install -r requirements.txt
```

---

## 📊 Data

### 🗂️ Data Files

| File | Format | Description |
|---------|--------|-------------|
| `data/*.json` | JSON | Raw API data |
| `data_clean/clean.csv` | CSV | Cleaned data |
| `data_clean/loaded_data.csv` | CSV | Data loaded to DB |
| `data_clean/loaded_data.json` | JSON Lines | Data loaded as JSON |

### 📈 Expected Statistics

- **Extracted cities:** 5
- **Fields per city:** 9 (city, country, temp, temp_min, temp_max, humidity, description, wind_speed, scrape_date)
- **Total rows:** 5 (one per city)
- **Data format:** Kelvin (API) → Converted for storage

---

## 🐛 Troubleshooting

### ❌ Error: `ModuleNotFoundError: No module named 'pymysql'`

**Solution:**
```bash
pip install pymysql
```

### ❌ Error: `Connection refused` for MySQL

**Check the MySQL service:**
```bash
# Status
sudo systemctl status mysql

# Start
sudo systemctl start mysql
```

### ❌ Error: `Access denied for user 'davy'`

**Check credentials:**
1. Open [etl/Load.py](etl/Load.py)
2. Verify the connection string
3. Ensure the MySQL user exists:
```sql
CREATE USER 'davy'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON First_Data.* TO 'davy'@'localhost';
FLUSH PRIVILEGES;
```

### ❌ Error: `Request timeout` during extraction

**Solution:**
- Check Internet connection
- Verify OpenWeatherMap API key
- Restart the pipeline

### ⚠️ Warning: `Database driver not available`

**Meaning:** `pymysql` is not installed, data is saved locally
**Solution:** `pip install pymysql`

---

## 📊 Complete Execution Result

```
2026-02-04 23:31:25,222 - INFO - Logger configured.
[EXTRACT] Starting extraction...
2026-02-04 23:32:14,137 - INFO - Data for Ouagadougou: {...}
2026-02-04 23:32:14,450 - INFO - Data for New York: {...}
2026-02-04 23:32:14,730 - INFO - Data for Londres: {...}
2026-02-04 23:32:15,012 - INFO - Data for Tokyo: {...}
2026-02-04 23:32:15,314 - INFO - Data for Sydney: {...}
2026-02-04 23:32:15,314 - INFO - [TRANSFORM] Starting transformation
2026-02-04 23:32:15,324 - INFO - [TRANSFORM] DataFrame created with shape (5, 8)
2026-02-04 23:32:15,341 - INFO - [TRANSFORM] Rows before: 5 → after: 5
2026-02-04 23:32:15,357 - INFO - [TRANSFORM] Cleaned data saved to clean.csv
2026-02-04 23:32:15,662 - INFO - Data loaded successfully
```

---

## 📖 Sample SQL Queries

```sql
-- Average temperature by country
SELECT country, AVG(temp) as avg_temp
FROM weather_data
GROUP BY country
ORDER BY avg_temp DESC;

-- Most humid cities
SELECT city, humidity
FROM weather_data
ORDER BY humidity DESC
LIMIT 3;

-- Latest data
SELECT * FROM weather_data
ORDER BY scrape_date DESC
LIMIT 10;
```

---

## 🤝 Contributing

Contributions are welcome! To propose an improvement:

1. 🍴 Fork the project
2. 🌿 Create a branch (`git checkout -b feature/AmazingFeature`)
3. 📝 Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🔄 Open a Pull Request

---

## 👤 Author

**Davy** - [GitHub](https://github.com/VyDonald) | [Email](mailto:tuwendedavy226@gmail.com)

---

## 🙏 Acknowledgments

- 🌐 [OpenWeatherMap API](https://openweathermap.org/api)
- 🐍 [Pandas Documentation](https://pandas.pydata.org/)
- 🗄️ [SQLAlchemy ORM](https://www.sqlalchemy.org/)

---

## 📞 Support

For any questions or issues, please:
- 📝 Open an **Issue** on GitHub
- 💬 Contact me directly

---

<div align="center">

### ⭐ If this project helped you, feel free to give it a star!

**Last updated:** February 4, 2026

</div>
