# 📊 CRM Analytics Project

RFM Analizi ve CLTV Prediction ile Müşteri Segmentasyonu

## 🚀 Hızlı Başlangıç

### 1. Projeyi İndir

```bash
# Eğer Git kullanıyorsan
git clone <https://github.com/necatictnkyaa1/crm-analytics-rfm-cltv>
cd crm_analytics_project

# Veya zip olarak indirdiysen
unzip crm_analytics_project.zip
cd crm_analytics_project
```

### 2. Virtual Environment Oluştur (PyCharm'da)

**Yöntem 1: PyCharm GUI ile**
1. File → Settings (veya Ctrl+Alt+S)
2. Project: crm_analytics_project → Python Interpreter
3. Sağ üstteki ⚙️ (ayarlar) → Add
4. "New environment" seç
5. Location: `venv` (proje klasörü içinde)
6. Base interpreter: Python 3.8 veya üzeri
7. ✅ "Make available to all projects" (isteğe bağlı)
8. OK

**Yöntem 2: Terminal ile**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Gereksinimleri Yükle

**PyCharm Terminal'de:**
```bash
pip install -r requirements.txt
```

**Veya PyCharm GUI'de:**
1. requirements.txt dosyasını aç
2. Üstte çıkan "Install requirements" banner'ına tıkla

### 4. Veri Dosyasını Yerleştir

Veri dosyanı (`flo_data_20k.csv`) şu konumlardan birine koy:
- `data/flo_data_20k.csv` (önerilen)
- `datasets/flo_data_20k.csv`
- Proje ana dizinine

### 5. Çalıştır! 🎉

**PyCharm'da:**
1. `main.py` dosyasını aç
2. Sağ tık → Run 'main'
3. Veya: Üstteki yeşil ▶️ play butonuna tıkla

**Terminal'de:**
```bash
python main.py
```

## 📁 Proje Yapısı

```
crm_analytics_project/
│
├── data/                      # Veri dosyaları
│   ├── raw/                  # Ham veri
│   └── processed/            # İşlenmiş veri
│
├── src/                       # Kaynak kodlar
│   ├── __init__.py
│   ├── flo_rfm_analysis.py   # RFM analizi
│   ├── flo_cltv_prediction.py # CLTV tahmini
│   └── config.py             # Konfigürasyon
│
├── outputs/                   # Çıktı dosyaları
│   ├── reports/              # Raporlar
│   └── figures/              # Grafikler
│
├── notebooks/                 # Jupyter notebook'lar
│
├── main.py                    # Ana çalıştırma dosyası
├── requirements.txt           # Python gereksinimleri
├── .gitignore                # Git ignore
└── README.md                 # Bu dosya
```

## 🎯 Kullanım

### RFM Analizi

```python
from src.flo_rfm_analysis import create_rfm_segments
import pandas as pd

# Veri yükle
df = pd.read_csv("data/flo_data_20k.csv")

# RFM analizi yap
rfm = create_rfm_segments(df, csv=True)

# Sonuçları incele
print(rfm['segment'].value_counts())
print(rfm.groupby('segment').agg({'recency': 'mean', 'frequency': 'mean', 'monetary': 'mean'}))
```

### CLTV Prediction

```python
from src.flo_cltv_prediction import create_cltv_prediction
import pandas as pd

# Veri yükle
df = pd.read_csv("data/flo_data_20k.csv")

# 6 aylık CLTV tahmini
cltv = create_cltv_prediction(df, month=6, segment_count=4)

# Sonuçları incele
print(cltv.groupby('cltv_segment')['cltv'].agg(['count', 'mean', 'sum']))
```

## 🐛 Hata Giderme

### "ModuleNotFoundError: No module named 'lifetimes'"

```bash
pip install lifetimes
```

### "FileNotFoundError: flo_data_20k.csv not found"

Veri dosyasını `data/` klasörüne koyduğundan emin ol.

### "pandas version error"

```bash
pip install --upgrade pandas
```

### Import hataları (PyCharm)

1. File → Invalidate Caches
2. Restart IDE
3. Tekrar dene

## 📊 Çıktılar

Çalıştırdıktan sonra `outputs/` klasöründe şu dosyalar oluşacak:

- `rfm_segments.csv` - RFM analizi sonuçları
- `cltv_prediction.csv` - CLTV tahminleri
- `crm_analytics.log` - Log dosyası

## 🤝 Katkıda Bulunma

1. Fork et
2. Feature branch oluştur (`git checkout -b feature/AmazingFeature`)
3. Commit et (`git commit -m 'Add some AmazingFeature'`)
4. Push et (`git push origin feature/AmazingFeature`)
5. Pull Request aç

## 📝 Lisans

MIT License

## 📫 İletişim

- LinkedIn: [https://www.linkedin.com/in/necatictnkya1/]
- Email: necatictnkya1@gmail.com

---

**Made with ❤️ and Python**
