# 🌍 First Data Project - Pipeline ETL Météo

> **Un pipeline ETL complet pour extraire, transformer et charger les données météorologiques de 5 villes du monde dans une base de données MySQL**

---

## 📋 Table des matières

- [🎯 Vue d'ensemble](#-vue-densemble)
- [✨ Fonctionnalités](#-fonctionnalités)
- [🏗️ Architecture](#-architecture)
- [📦 Installation](#-installation)
- [🚀 Utilisation](#-utilisation)
- [📂 Structure du projet](#-structure-du-projet)
- [🔄 Pipeline ETL](#-pipeline-etl)
- [🛠️ Configuration](#-configuration)
- [📊 Données](#-données)
- [🐛 Dépannage](#-dépannage)
- [📝 Licence](#-licence)

---

## 🎯 Vue d'ensemble

Ce projet implémente un **pipeline ETL (Extract, Transform, Load)** automatisé pour :

✅ **Extraire** les données météorologiques en temps réel depuis l'API OpenWeatherMap
✅ **Transformer** les données brutes pour les nettoyer et normaliser
✅ **Charger** les données transformées dans une base de données MySQL

Le pipeline gère gracieusement les erreurs, sauvegarde localement en CSV/JSON, et inclut un système de logging complet.

---

## ✨ Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| 🌐 **Extraction API** | Récupère les données météorologiques de 5 villes majeures via OpenWeatherMap |
| 🧹 **Nettoyage des données** | Supprime les doublons, traite les valeurs manquantes |
| 📊 **Transformation** | Normalise les unités de température, structure les données |
| 💾 **Stockage multi-format** | Sauvegarde en CSV, JSON et MySQL |
| 📝 **Logging détaillé** | Enregistre toutes les étapes du pipeline |
| ⚡ **Gestion d'erreurs** | Fallback gracieux si la base de données est indisponible |
| 🔐 **Configuration sécurisée** | Crédentiels stockés dans les variables d'environnement |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                  MAIN.PY - Orchestrateur            │
└──────────┬──────────────────────────────┬───────────┘
           │                              │
    ┌──────▼────────┐            ┌────────▼──────────┐
    │  EXTRACT      │            │   TRANSFORM       │
    │  - API Call   │            │   - Nettoyage     │
    │  - JSON Save  │            │   - Normalisation │
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

### 📋 Prérequis

- **Python** 3.8+
- **MySQL Server** 5.7+ (optionnel pour la sauvegarde locale)
- **pip** (gestionnaire de paquets Python)

### 🔧 Étape 1 : Cloner le repository

```bash
git clone <votre-repo>
cd First_Data_Project
```

### 🔧 Étape 2 : Créer un environnement virtuel

```bash
# Sur Windows
python -m venv venv
venv\Scripts\activate

# Sur macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 🔧 Étape 3 : Installer les dépendances

```bash
pip install -r requirements.txt
```

### 🔧 Étape 4 : Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet (optionnel) :

```env
DB_USER=davy
DB_PASSWORD=password123
DB_HOST=localhost
DB_NAME=First_Data
API_KEY=21df4d73e5dc83ea09d6f0ed3148d2bc
```

### 🔧 Étape 5 : Configurer MySQL (optionnel)

```bash
# Vérifier le statut de MySQL
sudo systemctl status mysql

# Démarrer MySQL si nécessaire
sudo systemctl start mysql

# Créer la base de données
mysql -u root -p
> CREATE DATABASE First_Data;
```

---

## 🚀 Utilisation

### ▶️ Exécuter le pipeline complet

```bash
python main.py
```

**Résultat attendu :**
```
2026-02-04 23:31:25,222 - INFO - Logger configured.
[EXTRACT] Starting extraction...
2026-02-04 23:32:14,137 - INFO - Data for Ouagadougou: {...}
...
2026-02-04 23:32:15,357 - INFO - [TRANSFORM] Cleaned data saved to clean.csv
2026-02-04 23:32:15,662 - INFO - Data loaded successfully
```

### ▶️ Exécuter uniquement l'extraction

```bash
python -m etl.Extract
```

### ▶️ Exécuter uniquement la transformation

```bash
python -m etl.Transform
```

### ▶️ Exécuter uniquement le chargement

```bash
python -m etl.Load
```

---

## 📂 Structure du projet

```
First_Data_Project/
│
├── 📄 main.py                 # Point d'entrée principal
├── 📄 requirements.txt         # Dépendances du projet
├── 📄 README.md               # Cette documentation
│
├── 📁 config/                 # Configuration
│   ├── __init__.py
│   └── logger.py              # Configuration du logging
│
├── 📁 etl/                    # Pipeline ETL
│   ├── __init__.py
│   ├── Extract.py             # Étape d'extraction (API)
│   ├── Transform.py           # Étape de transformation (nettoyage)
│   └── Load.py                # Étape de chargement (BD)
│
├── 📁 data/                   # Données brutes (JSON)
│   ├── Ouagadougou.json
│   ├── New York.json
│   ├── Londres.json
│   ├── Tokyo.json
│   └── Sydney.json
│
├── 📁 data_clean/             # Données transformées
│   ├── clean.csv              # Données nettoyées (CSV)
│   ├── loaded_data.csv        # Données chargées (CSV)
│   ├── loaded_data.json       # Données chargées (JSON)
│   └── requètes.sql           # Requêtes SQL d'exemple
│
└── 📁 logs/                   # Fichiers de log
    └── app.log                # Log du pipeline
```

---

## 🔄 Pipeline ETL

### **1️⃣ Phase EXTRACT - Extraction des données**

**Fichier :** [etl/Extract.py](etl/Extract.py)

📡 **Récupère les données météorologiques** depuis l'API OpenWeatherMap pour 5 villes :
- 🌍 Ouagadougou (Burkina Faso)
- 🌃 New York (USA)
- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Londres (UK)
- 🗾 Tokyo (Japon)
- 🦘 Sydney (Australie)

**Données extraites :**
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

**Actions :**
- ✅ Appel API avec gestion des erreurs
- ✅ Sauvegarde en fichiers JSON
- ✅ Logging détaillé de chaque étape

---

### **2️⃣ Phase TRANSFORM - Transformation des données**

**Fichier :** [etl/Transform.py](etl/Transform.py)

🧹 **Nettoie et normalise** les données brutes :

**Processus :**
1. **Chargement** des fichiers JSON depuis `/data`
2. **Extraction** des champs pertinents
3. **Suppression des doublons** avec `drop_duplicates()`
4. **Gestion des valeurs manquantes** avec `dropna()`
5. **Conversion des types** en numériques
6. **Ajout du timestamp** (date de scrape)
7. **Sauvegarde** en CSV pour vérification

**Données transformées :**
```
     ville     pays   temp  temp_min  temp_max  humidite           description  vitesse_vent         scrape_date
0  Ouagadougou   BF  300.22    300.22    300.22        17           clear sky           2.57  2026-02-04 23:32:15
1    New York   US  273.53    271.46    274.13        36           clear sky           4.12  2026-02-04 23:32:15
2     London   GB  281.19    280.32    281.82        84      broken clouds           8.23  2026-02-04 23:32:15
3      Tokyo   JP  278.48    276.82    279.94        56        few clouds           2.57  2026-02-04 23:32:15
4     Sydney   AU  301.61    300.76    303.12        58           clear sky           4.12  2026-02-04 23:32:15
```

**Améliorations appliquées :**
- ✅ Suppression des lignes avec température ou humidité manquante
- ✅ Normalisation des types de données
- ✅ Ajout d'un timestamp universel
- ✅ Validation des données

---

### **3️⃣ Phase LOAD - Chargement des données**

**Fichier :** [etl/Load.py](etl/Load.py)

💾 **Charge les données transformées** dans la base de données MySQL

**Architecture BD :**
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

**Actions :**
- ✅ Création de la table si elle n'existe pas
- ✅ Insertion des données avec mode `APPEND`
- ✅ Sauvegarde CSV et JSON en secours
- ✅ Gestion des erreurs de connexion

**Fallback :** Si MySQL est indisponible, les données sont sauvegardées localement en CSV/JSON

---

## 🛠️ Configuration

### 📝 Configuration du logger

**Fichier :** [config/logger.py](config/logger.py)

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

### 📋 Dépendances

**Fichier :** [requirements.txt](requirements.txt)

```
pandas==3.0.0
numpy==2.4.2
requests==2.32.5
sqlalchemy==2.0.46
pymysql==1.1.2
beautifulsoup4==4.14.3
pyyaml==6.0.3
```

Installation :
```bash
pip install -r requirements.txt
```

---

## 📊 Données

### 🗂️ Fichiers de données

| Fichier | Format | Description |
|---------|--------|-------------|
| `data/*.json` | JSON | Données brutes de l'API |
| `data_clean/clean.csv` | CSV | Données nettoyées |
| `data_clean/loaded_data.csv` | CSV | Données chargées dans BD |
| `data_clean/loaded_data.json` | JSON Lines | Données chargées en JSON |

### 📈 Statistiques attendues

- **Villes extraites :** 5
- **Champs par ville :** 9 (ville, pays, temp, temp_min, temp_max, humidite, description, vitesse_vent, scrape_date)
- **Lignes totales :** 5 (une par ville)
- **Format données :** Kelvin (API) → Converti pour stockage

---

## 🐛 Dépannage

### ❌ Erreur : `ModuleNotFoundError: No module named 'pymysql'`

**Solution :**
```bash
pip install pymysql
```

### ❌ Erreur : `Connection refused` pour MySQL

**Vérifier le service MySQL :**
```bash
# Status
sudo systemctl status mysql

# Démarrer
sudo systemctl start mysql
```

### ❌ Erreur : `Access denied for user 'davy'`

**Vérifier les crédentiels :**
1. Ouvrir [etl/Load.py](etl/Load.py)
2. Vérifier la chaîne de connexion
3. S'assurer que l'utilisateur MySQL existe :
```sql
CREATE USER 'davy'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON First_Data.* TO 'davy'@'localhost';
FLUSH PRIVILEGES;
```

### ❌ Erreur : `Request timeout` lors de l'extraction

**Solution :**
- Vérifier la connexion Internet
- Vérifier la clé API OpenWeatherMap
- Relancer le pipeline

### ⚠️ Avertissement : `Database driver not available`

**Signification :** `pymysql` n'est pas installé, les données sont sauvegardées localement
**Solution :** `pip install pymysql`

---

## 📊 Résultat d'exécution complet

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

## 📖 Exemple de requête SQL

```sql
-- Température moyenne par pays
SELECT pays, AVG(temp) as temp_moyenne
FROM weather_data
GROUP BY pays
ORDER BY temp_moyenne DESC;

-- Villes les plus humides
SELECT ville, humidite
FROM weather_data
ORDER BY humidite DESC
LIMIT 3;

-- Dernières données (plus récentes)
SELECT * FROM weather_data
ORDER BY scrape_date DESC
LIMIT 10;
```

---

## 🤝 Contribution

Les contributions sont bienvenues ! Pour proposer une amélioration :

1. 🍴 Fork le projet
2. 🌿 Créer une branche (`git checkout -b feature/AmazingFeature`)
3. 📝 Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. 📤 Push vers la branche (`git push origin feature/AmazingFeature`)
5. 🔄 Ouvrir une Pull Request

---

## 📝 Licence

Ce projet est sous licence **MIT**. Voir le fichier `LICENSE` pour plus de détails.

---

## 👤 Auteur

**Davy** - [GitHub](https://github.com) | [Email](mailto:davy@example.com)

---

## 🙏 Remerciements

- 🌐 [OpenWeatherMap API](https://openweathermap.org/api)
- 🐍 [Pandas Documentation](https://pandas.pydata.org/)
- 🗄️ [SQLAlchemy ORM](https://www.sqlalchemy.org/)

---

## 📞 Support

Pour toute question ou problème, veuillez :
- 📝 Ouvrir une **Issue** sur GitHub
- 💬 Me contacter directement

---

<div align="center">

### ⭐ Si ce projet vous a aidé, n'hésitez pas à lui donner une star !

**Dernière mise à jour :** 4 février 2026

</div>
