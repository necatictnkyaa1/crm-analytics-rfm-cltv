"""
CRM Analytics Projesi - Konfigürasyon Dosyası
"""

import os
from pathlib import Path

# Proje ana dizini
BASE_DIR = Path(__file__).parent.parent

# Data dizinleri
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Output dizinleri
OUTPUT_DIR = BASE_DIR / "outputs"
REPORTS_DIR = OUTPUT_DIR / "reports"
FIGURES_DIR = OUTPUT_DIR / "figures"

# Model parametreleri
RFM_CONFIG = {
    "recency_bins": 5,
    "frequency_bins": 5,
    "monetary_bins": 5,
    "segment_map": {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }
}

CLTV_CONFIG = {
    "bgf_penalizer_coef": 0.001,
    "ggf_penalizer_coef": 0.01,
    "discount_rate": 0.01,
    "freq": "W",  # Weekly
    "outlier_quantiles": (0.01, 0.99)
}

# Veri dosya isimleri
DATA_FILES = {
    "flo_data": "flo_data_20k.csv",
    "online_retail": "online_retail_II.xlsx"
}

# Klasörleri oluştur
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, 
                  OUTPUT_DIR, REPORTS_DIR, FIGURES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Logging ayarları
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': str(OUTPUT_DIR / 'crm_analytics.log'),
            'mode': 'a'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
