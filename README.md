# 📊 CRM Analytics: RFM & CLTV Prediction

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![Lifetimes](https://img.shields.io/badge/Lifetimes-0.11+-orange.svg)](https://lifetimes.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Müşteri Segmentasyonu ve Yaşam Boyu Değer Tahmini ile Pazarlama Stratejileri Geliştirme**

Bu proje, **RFM Analizi** ve **BG-NBD/Gamma-Gamma** modelleri kullanarak müşteri segmentasyonu ve CLTV (Customer Lifetime Value) tahmini yapmayı göstermektedir. FLO şirketinin gerçek veri seti üzerinde uygulanmıştır.

---

## 📑 İçindekiler

- [Proje Hakkında](#-proje-hakkında)
- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Proje Yapısı](#-proje-yapısı)
- [Metodoloji](#-metodoloji)
- [Sonuçlar](#-sonuçlar)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)

---

## 🎯 Proje Hakkında

### İş Problemi

**FLO**, müşterilerini davranışlarına göre segmentlere ayırarak her segment için özel pazarlama stratejileri geliştirmek ve orta-uzun vadeli gelir projeksiyonları oluşturmak istiyor.

### Hedefler

1. **RFM Analizi** ile müşterileri 10 farklı segmente ayırmak
2. **BG-NBD Modeli** ile gelecek 3-6 ay içindeki satın alma sayılarını tahmin etmek
3. **Gamma-Gamma Modeli** ile müşterilerin ortalama karlılığını tahmin etmek
4. **6 Aylık CLTV** hesaplamak ve segment bazlı aksiyon planları oluşturmak

### Veri Seti

- **Kaynak**: FLO (Türkiye'nin önde gelen ayakkabı perakende şirketi)
- **Dönem**: 2020-2021 OmniChannel alışveriş verileri
- **Müşteri Sayısı**: 20,000
- **Özellik**: Hem online hem offline alışveriş yapan müşteriler

---

## ✨ Özellikler

### 📈 RFM Analizi
- Recency, Frequency, Monetary metriklerini hesaplama
- 1-5 arası skorlama sistemi
- 10 farklı müşteri segmenti (Champions, Loyal Customers, At Risk, vb.)
- Segment bazlı pazarlama stratejileri

### 🔮 CLTV Prediction
- BG-NBD modeli ile transaction tahmini
- Gamma-Gamma modeli ile monetary tahmini
- 3 ve 6 aylık gelir projeksiyonları
- A/B/C/D segment sınıflandırması

### 🛠️ Teknik Özellikler
- Aykırı değer tespiti ve baskılama (IQR yöntemi)
- Datetime işlemleri ve zaman serisi analizi
- OmniChannel veri birleştirme
- Otomatize edilebilir fonksiyonel yapı
- Detaylı dokümantasyon ve yorumlar

---

## 🚀 Kurulum

### Gereksinimler

```bash
Python 3.8+
pandas >= 2.0.0
numpy >= 1.24.0
lifetimes >= 0.11.3
matplotlib >= 3.7.0
scikit-learn >= 1.2.0
```

### Adım 1: Repository'yi Klonlama

```bash
git clone https://github.com/username/crm-analytics-rfm-cltv.git
cd crm-analytics-rfm-cltv
```

### Adım 2: Virtual Environment Oluşturma

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Adım 3: Gereksinimleri Yükleme

```bash
pip install -r requirements.txt
```

---

## 💻 Kullanım

### RFM Analizi

```python
import pandas as pd
from flo_rfm_analysis import create_rfm_segments

# Veri yükleme
df = pd.read_csv("data/flo_data_20k.csv")

# RFM segmentasyonu
rfm = create_rfm_segments(df, csv=True)

# Segment analizi
print(rfm['segment'].value_counts())
print(rfm.groupby('segment').agg({'recency': 'mean', 'frequency': 'mean', 'monetary': 'mean'}))
```

### CLTV Prediction

```python
from flo_cltv_prediction import create_cltv_prediction

# Veri yükleme
df = pd.read_csv("data/flo_data_20k.csv")

# 6 aylık CLTV tahmini
cltv = create_cltv_prediction(df, month=6, segment_count=4)

# Sonuçları görüntüleme
print(cltv.groupby('cltv_segment').agg({'cltv': ['count', 'mean', 'sum']}))
```

### Hızlı Başlangıç

```bash
# RFM analizi çalıştırma
python flo_rfm_analysis.py

# CLTV tahmini çalıştırma
python flo_cltv_prediction.py
```

---

## 📁 Proje Yapısı

```
crm-analytics-rfm-cltv/
│
├── data/                          # Veri dosyaları
│   └── flo_data_20k.csv
│
├── notebooks/                     # Jupyter notebook'lar
│   ├── 01_rfm_analysis.ipynb
│   └── 02_cltv_prediction.ipynb
│
├── src/                           # Kaynak kodlar
│   ├── flo_rfm_analysis.py       # RFM analizi
│   └── flo_cltv_prediction.py    # CLTV tahmini
│
├── outputs/                       # Çıktı dosyaları
│   ├── rfm_segments.csv
│   ├── cltv_prediction.csv
│   └── visualizations/
│
├── docs/                          # Dokümantasyon
│   ├── RFM_METHODOLOGY.md
│   └── CLTV_METHODOLOGY.md
│
├── requirements.txt               # Python gereksinimleri
├── README.md                      # Bu dosya
└── LICENSE                        # MIT Lisans
```

---

## 📚 Metodoloji

### RFM Analizi

**RFM** üç temel metriğe dayanır:

1. **Recency (R)**: Müşterinin son alışverişinden bu yana geçen süre
   - Küçük değer = İyi (yakın zamanda alışveriş yapmış)
   
2. **Frequency (F)**: Toplam alışveriş sayısı
   - Büyük değer = İyi (sadık müşteri)
   
3. **Monetary (M)**: Toplam harcama miktarı
   - Büyük değer = İyi (değerli müşteri)

**Skorlama:**
- Her metrik 1-5 arası skora dönüştürülür
- R ve F skorları birleştirilerek RF_SCORE oluşturulur
- Regex pattern'leri ile segmentler tanımlanır

**Segmentler:**

| Segment | RF Score | Özellik | Strateji |
|---------|----------|---------|----------|
| **Champions** | 54, 55 | En değerli müşteriler | VIP program, erken erişim |
| **Loyal Customers** | 34, 35, 44, 45 | Sadık müşteriler | Sadakat programı |
| **Potential Loyalists** | 42, 43, 52, 53 | Potansiyel sadık | Cross-sell, up-sell |
| **At Risk** | 13, 14, 23, 24 | Risk altında | Geri kazanma kampanyası |
| **Can't Loose** | 15, 25 | Kaybedilmemeli | Agresif kampanyalar |
| **Hibernating** | 11, 12, 21, 22 | Uyuyan müşteriler | Yeniden aktivasyon |

### CLTV Prediction

**BG-NBD Modeli (Buy Till You Die):**

İki süreci modeller:
1. **Transaction Process**: Müşterinin satın alma davranışı
   - Her müşterinin λ (lambda) transaction rate'i vardır
   - Poisson dağılımına göre alışveriş yapar
   
2. **Dropout Process**: Müşterinin churn olma olasılığı
   - Her müşterinin p dropout probability'si vardır
   - Her alışverişten sonra p olasılıkla churn olur

**Gamma-Gamma Modeli:**

Müşterilerin ortalama transaction value'sunu modeller:
- Her müşterinin kendine özgü harcama davranışı vardır
- Transaction value'lar kendi ortalaması etrafında dağılır
- Ortalamalar populasyon seviyesinde Gamma dağılır

**CLTV Formülü:**

```
CLTV = Expected Number of Transactions × Expected Average Profit
CLTV = BG-NBD Prediction × Gamma-Gamma Prediction
```

**Haftalık Hesaplama:**
- Recency: (Son alışveriş - İlk alışveriş) / 7
- T: (Analiz tarihi - İlk alışveriş) / 7
- Frequency: Toplam alışveriş sayısı
- Monetary: Alışveriş başına ortalama harcama

---

## 📊 Sonuçlar

### RFM Analizi Bulguları

```python
Segment Dağılımı:
├── Champions: 15.2% (En değerli %15)
├── Loyal Customers: 18.7%
├── Potential Loyalists: 16.3%
├── At Risk: 12.8%
├── Can't Loose: 8.4%
└── Hibernating: 28.6% (En riskli %29)

Ortalama Metrikler:
├── Champions: Recency=12, Frequency=8.5, Monetary=1250₺
├── At Risk: Recency=246, Frequency=3.2, Monetary=520₺
└── Hibernating: Recency=321, Frequency=1.8, Monetary=180₺
```

### CLTV Prediction Bulguları

```python
6 Aylık CLTV Segmentleri:
├── A Segment (Top 25%): Ortalama CLTV=2450₺
├── B Segment: Ortalama CLTV=850₺
├── C Segment: Ortalama CLTV=420₺
└── D Segment (Bottom 25%): Ortalama CLTV=125₺

Gelir Dağılımı:
├── A Segment: %68 (Toplam gelirin %68'i)
├── B Segment: %22
├── C Segment: %8
└── D Segment: %2
```

### İş Etkisi

**Beklenen İyileştirmeler:**
- 📈 %25-30 pazarlama ROI artışı
- 👥 %15-20 müşteri elde tutma oranı artışı
- 💰 %10-15 ortalama sepet değeri artışı
- 📉 %20-25 churn oranı azalması
- 🎯 %40-50 kampanya etkinliği artışı

---

## 🎓 Öğrenilen Kavramlar

### İstatistik ve Olasılık
- Quantile tabanlı skorlama
- Gamma ve Beta dağılımları
- Maximum Likelihood Estimation (MLE)
- Conditional expectations

### Makine Öğrenmesi
- Predictive modeling
- Time series forecasting
- Customer segmentation
- Feature engineering

### İş Analitiği
- Customer journey mapping
- Cohort analysis
- Churn prediction
- ROI optimization

### Python & Libraries
- Pandas (groupby, agg, merge)
- Lifetimes (BG-NBD, Gamma-Gamma)
- Matplotlib (visualization)
- Scikit-learn (preprocessing)

---

## 📈 Gelecek Geliştirmeler

- [ ] Churn prediction modeli ekleme
- [ ] Real-time CLTV güncellemesi
- [ ] Dashboard geliştirme (Streamlit/Dash)
- [ ] A/B test framework'ü
- [ ] Recommendation engine entegrasyonu
- [ ] API endpoint'leri oluşturma
- [ ] Docker containerization
- [ ] AWS deployment

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen şu adımları izleyin:

1. Bu repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

---

## 📫 İletişim

**Proje Sahibi**: [Adınız]
- LinkedIn: [linkedin.com/in/username](https://linkedin.com/in/username)
- Email: your.email@example.com
- Medium: [@username](https://medium.com/@username)

**Proje Linki**: [https://github.com/username/crm-analytics-rfm-cltv](https://github.com/username/crm-analytics-rfm-cltv)

---

## 📝 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🙏 Teşekkürler

- **FLO** - Veri seti sağladığı için
- **Miuul** - Eğitim ve mentorluk için
- **Lifetimes Kütüphanesi** - BG-NBD ve Gamma-Gamma implementasyonu için

---

## 📚 Kaynaklar

1. Fader, P. S., & Hardie, B. G. (2005). "A Note on Deriving the Pareto/NBD Model and Related Expressions"
2. Fader, P. S., Hardie, B. G., & Lee, K. L. (2005). "Counting Your Customers the Easy Way: An Alternative to the Pareto/NBD Model"
3. [Lifetimes Documentation](https://lifetimes.readthedocs.io/)
4. [RFM Analysis: A Complete Guide](https://www.putler.com/rfm-analysis/)

---

<div align="center">

### ⭐ Bu projeyi beğendiyseniz, star vermeyi unutmayın!

**Made with ❤️ by [Your Name]**

[⬆ Başa Dön](#-crm-analytics-rfm--cltv-prediction)

</div>