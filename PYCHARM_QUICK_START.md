# 🚀 PyCharm'da Projeyi Çalıştırma Rehberi

**Hazırlayan:** Muhammet Necati
**Rol:** Veri Bilimi Adayı
**Tarih:** 20.02.2026

## 📥 Adım 1: Projeyi PyCharm'a Açma

### Yöntem 1: Zip'ten Açma (Önerilen)
1. `crm_analytics_project.zip` dosyasını indir
2. İstediğin bir klasöre çıkart (örn: `C:\Projects\`)
3. PyCharm'ı aç
4. **File → Open**
5. `crm_analytics_project` klasörünü seç
6. **OK** / **Trust Project**

### Yöntem 2: Git Clone (Eğer GitHub'da ise)
1. PyCharm'da **File → New → Project from Version Control**
2. GitHub URL'sini yapıştır
3. Clone

---

## 🐍 Adım 2: Python Interpreter Kurulumu

### PyCharm'da Virtual Environment Oluşturma:

1. **File → Settings** (veya `Ctrl+Alt+S`)
2. Sol menüden: **Project: crm_analytics_project → Python Interpreter**
3. Sağ üstteki **⚙️ (ayarlar)** → **Add...**
4. **Virtualenv Environment** seç
5. **New environment** seç
6. Ayarlar:
   ```
   Location: <proje_klasörü>\venv
   Base interpreter: Python 3.8 (veya daha yüksek)
   ✅ Inherit global site-packages: Kapalı
   ✅ Make available to all projects: İsteğe bağlı
   ```
7. **OK** → **Apply** → **OK**

### Terminal'de Doğrulama:
PyCharm'ın alt kısmında **Terminal** (Alt+F12) aç ve kontrol et:

```bash
# Virtual environment aktif mi?
# Windows'ta şöyle görünmeli: (venv) C:\Projects\crm_analytics_project>
# Mac/Linux'ta: (venv) user@computer:~/crm_analytics_project$

python --version
# Python 3.8 veya üzeri olmalı
```

---

## 📦 Adım 3: Gereksinimleri Yükleme

### Yöntem 1: PyCharm GUI ile (Kolay) ⭐

1. `requirements.txt` dosyasını aç
2. Üstte bir banner görünecek: "Package requirements file requirements.txt is not satisfied"
3. **Install requirements** linkine tıkla
4. Bekle... (1-2 dakika sürebilir)

### Yöntem 2: Terminal ile

PyCharm Terminal'de (Alt+F12):

```bash
# Virtual environment'ın aktif olduğundan emin ol
pip install -r requirements.txt
```

### Kurulum Kontrolü:

```bash
pip list
# pandas, numpy, lifetimes, matplotlib vb. görünmeli
```

---

## 📁 Adım 4: Veri Dosyasını Yerleştirme

### Veri dosyası nereden bulunur?
- Eğitim platformundan indirilmeli: `flo_data_20k.csv`

### Nereye koymalı?
Şu konumlardan **birine** koy:

**Option 1 (Önerilen):**
```
crm_analytics_project/
└── data/
    └── flo_data_20k.csv  ← Buraya
```

**Option 2:**
```
crm_analytics_project/
└── flo_data_20k.csv  ← Ana dizine
```

**Option 3:**
```
crm_analytics_project/
└── datasets/
    └── flo_data_20k.csv  ← Yeni klasör oluştur
```

### PyCharm'da Dosyayı Kopyalama:
1. Veri dosyasını bul (Windows Explorer / Finder)
2. Sürükle-bırak ile PyCharm'daki `data/` klasörüne at

---

## ▶️ Adım 5: Projeyi Çalıştırma

### Yöntem 1: main.py'yi Çalıştırma (Kolay) ⭐

1. Sol panelde **main.py** dosyasını bul
2. **Çift tıkla** (dosya açılacak)
3. Üstte **yeşil ▶️ play butonu** görünecek
4. Tıkla veya `Shift + F10` bas

**Veya:**
1. `main.py` dosyasına **sağ tıkla**
2. **Run 'main'** seç

### Yöntem 2: Terminal'den Çalıştırma

```bash
python main.py
```

### ✅ Başarılı Çıktı Örneği:

```
======================================================================
CRM ANALYTICS - RFM & CLTV PREDICTION
======================================================================

📂 Veri dosyası: data/flo_data_20k.csv

----------------------------------------------------------------------
1️⃣  VERİYİ YÜKLEME
----------------------------------------------------------------------
✅ Veri başarıyla yüklendi!
   Satır: 20,000, Sütun: 12

======================================================================
2️⃣  RFM ANALİZİ ÇALIŞTIRILIYOR
======================================================================

✅ RFM analizi tamamlandı!

📊 Segment Dağılımı:
hibernating           5,720
loyal_customers       3,740
...

💾 RFM sonuçları kaydedildi: outputs/rfm_segments.csv

======================================================================
3️⃣  CLTV PREDICTION ÇALIŞTIRILIYOR
======================================================================

✅ CLTV tahmini tamamlandı!
...
```

---

## 🔧 Adım 6: Jupyter Notebook Kullanma (Opsiyonel)

### Jupyter'ı Başlatma:

**Terminal'de:**
```bash
jupyter notebook
```

Tarayıcıda açılacak. `notebooks/rfm_analysis_notebook.ipynb` dosyasını aç.

**PyCharm Professional'da:**
1. `.ipynb` dosyasına çift tıkla
2. PyCharm içinde açılacak
3. Hücreleri çalıştır (Shift+Enter)

---

## 🐛 Yaygın Hatalar ve Çözümleri

### ❌ "ModuleNotFoundError: No module named 'lifetimes'"

**Çözüm:**
```bash
pip install lifetimes
```

**Veya tüm gereksinimleri tekrar yükle:**
```bash
pip install -r requirements.txt
```

---

### ❌ "FileNotFoundError: flo_data_20k.csv not found"

**Sorun:** Veri dosyası bulunamıyor

**Çözüm 1:** Veri dosyasının yolunu kontrol et
```bash
# Terminal'de kontrol et
ls data/           # Mac/Linux
dir data\          # Windows
```

**Çözüm 2:** Veri dosyasını doğru klasöre kopyala
- `data/flo_data_20k.csv` konumuna koy

**Çözüm 3:** `main.py`'deki yolu güncelle
```python
# main.py içinde, satır ~20 civarı
data_path = Path("BURAYA_DOĞRU_YOLU_YAZ/flo_data_20k.csv")
```

---

### ❌ "ImportError: cannot import name 'create_rfm_segments'"

**Sorun:** Python modül import sorunu

**Çözüm 1:** PyCharm'ı yeniden başlat
1. File → Invalidate Caches
2. Restart

**Çözüm 2:** Working Directory'yi kontrol et
1. Run → Edit Configurations
2. Working directory: Proje root klasörü olmalı

**Çözüm 3:** `src/__init__.py` dosyasının var olduğundan emin ol

---

### ❌ "No Python interpreter configured for the project"

**Sorun:** Python interpreter seçilmemiş

**Çözüm:** Adım 2'yi tekrarla (Python Interpreter Kurulumu)

---

### ❌ Kod çalışıyor ama çıktı görünmüyor

**Çözüm:** Run window'u aç
- View → Tool Windows → Run (Alt+4)

---

### ❌ "pandas has no attribute 'read_csv'"

**Sorun:** pandas yanlış versiyonda veya yüklenmemiş

**Çözüm:**
```bash
pip uninstall pandas
pip install pandas>=2.0.0
```

---

## 📊 Çıktıları Görüntüleme

### Çıktı dosyaları nerede?

```
crm_analytics_project/
└── outputs/
    ├── rfm_segments.csv              ← RFM sonuçları
    ├── cltv_prediction.csv           ← CLTV sonuçları
    └── crm_analytics.log             ← Log dosyası
```

### PyCharm'da CSV Dosyalarını Açma:

1. Sol panelde `outputs/` klasörünü aç
2. `rfm_segments.csv` dosyasına **çift tıkla**
3. PyCharm'ın dahili CSV viewer'ı açılacak

**Veya Excel'de aç:**
1. Dosyaya **sağ tıkla**
2. **Open In → Explorer/Finder**
3. Excel ile aç

---

## 🎯 İleri Seviye: Debug Mode

### Breakpoint Koyma:

1. Kodun herhangi bir satırında, satır numarasının yanına **tıkla**
2. Kırmızı nokta (breakpoint) oluşacak

### Debug Çalıştırma:

1. `main.py` dosyasına **sağ tıkla**
2. **Debug 'main'** seç
3. Veya: `Shift + F9`

### Debug Sırasında:
- Değişken değerlerini görebilirsin
- Adım adım ilerleyebilirsin (F8)
- İşlemi durdurup inceleyebilirsin

---

## 🎓 Yardım ve Destek

### PyCharm Yardım Menüsü:
- Help → PyCharm Help
- Help → Keyboard Shortcuts (PDF)

### Faydalı Kısayollar:

```
Ctrl+Alt+S          → Settings
Shift+F10           → Run
Shift+F9            → Debug
Alt+F12             → Terminal
Ctrl+Shift+F10      → Run context configuration
Ctrl+/              → Yorum satırı (comment/uncomment)
```

### Online Kaynaklar:
- [PyCharm Documentation](https://www.jetbrains.com/help/pycharm/)
- [Python.org Tutorials](https://docs.python.org/3/tutorial/)

---

## ✅ Kontrol Listesi

Çalıştırmadan önce kontrol et:

- [ ] PyCharm kurulu (Community veya Professional)
- [ ] Python 3.8+ yüklü
- [ ] Proje PyCharm'da açık
- [ ] Virtual environment oluşturulmuş ve aktif
- [ ] `requirements.txt` yüklenmiş (`pip list` ile kontrol)
- [ ] Veri dosyası doğru konumda (`data/flo_data_20k.csv`)
- [ ] `main.py` dosyası açılabilir durumda
- [ ] Yeşil play butonu görünüyor

Hepsi ✅ ise: **Çalıştır!** 🚀


