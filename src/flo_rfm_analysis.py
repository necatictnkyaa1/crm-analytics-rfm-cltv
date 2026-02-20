###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
# FLO Müşteri Analizi Projesi
###############################################################

"""
İŞ PROBLEMİ:
FLO, müşterilerini davranışlarına göre segmentlere ayırarak 
her segment için özel pazarlama stratejileri geliştirmek istiyor.

HEDEF:
- Müşteri davranışlarını RFM metrikleri ile analiz etmek
- Segmentlere özel aksiyon planları oluşturmak
"""

###############################################################
# VERİ SETİ HİKAYESİ
###############################################################
"""
Veri Seti: 2020-2021 yılları arasında OmniChannel alışveriş yapan 
          müşterilerin geçmiş davranışları

OmniChannel: Hem online hem offline alışveriş yapan müşteriler
            (Gerçek hayatta bu tip müşteriler şirket için çok değerlidir!)

DEĞİŞKENLER:
- master_id: Eşsiz müşteri numarası (Primary Key)
- order_channel: Alışveriş kanalı (Android, iOS, Desktop, Mobile, Offline)
- last_order_channel: Son alışverişin yapıldığı kanal
- first_order_date: İlk alışveriş tarihi (Müşteri yaşını hesaplamak için önemli)
- last_order_date: Son alışveriş tarihi (Recency için kritik!)
- last_order_date_online: Online son alışveriş tarihi
- last_order_date_offline: Offline son alışveriş tarihi
- order_num_total_ever_online: Online toplam alışveriş sayısı
- order_num_total_ever_offline: Offline toplam alışveriş sayısı
- customer_value_total_ever_offline: Offline toplam harcama
- customer_value_total_ever_online: Online toplam harcama
- interested_in_categories_12: Son 12 aydaki alışveriş kategorileri
"""

###############################################################
# KÜTÜPHANELER
###############################################################

import datetime as dt
import pandas as pd

# Pandas görüntüleme ayarları
pd.set_option('display.max_columns', None)  # Tüm sütunları göster
pd.set_option('display.max_rows', 20)       # İlk 20 satır
pd.set_option('display.float_format', lambda x: '%.2f' % x)  # 2 ondalık
pd.set_option('display.width', 1000)        # Genişlik ayarı

###############################################################
# GÖREV 1: Veriyi Hazırlama ve Anlama (Data Understanding)
###############################################################

# 1. VERİYİ OKUMA
print("=" * 70)
print("GÖREV 1: VERİ HAZIRLAMA VE ANLAMA")
print("=" * 70)

# CSV dosyasını okuma
df_ = pd.read_csv("datasets/flo_data_20k.csv")
df = df_.copy()  # Orijinal veriyi korumak için kopya oluşturma

print("\n✓ Veri başarıyla yüklendi!")

# 2. VERİ SETİ İNCELEMESİ

# a. İlk 10 gözlem
print("\n" + "-" * 70)
print("A) İLK 10 GÖZLEM")
print("-" * 70)
print(df.head(10))
"""
İLK GÖZLEMDEN ANLADIKLARIMIZ:
- Her müşterinin benzersiz bir master_id'si var
- Hem online hem offline alışveriş verileri mevcut
- Tarih formatları string olarak gelmiş (düzeltilmeli!)
- Kategori verileri liste formatında
"""

# b. Değişken isimleri
print("\n" + "-" * 70)
print("B) DEĞİŞKEN İSİMLERİ")
print("-" * 70)
print(df.columns.tolist())
print(f"\nToplam {len(df.columns)} değişken var")

# c. Veri seti boyutu
print("\n" + "-" * 70)
print("C) VERİ SETİ BOYUTU")
print("-" * 70)
print(f"Satır sayısı: {df.shape[0]:,}")
print(f"Sütun sayısı: {df.shape[1]}")
print(f"Toplam hücre sayısı: {df.shape[0] * df.shape[1]:,}")
"""
ÖNEMLİ NOT: 
20,000 müşteri verisi ile çalışıyoruz.
Bu orta ölçekli bir veri seti (gerçek projede milyonlarca olabilir)
"""

# d. Betimsel istatistikler
print("\n" + "-" * 70)
print("D) BETİMSEL İSTATİSTİKLER")
print("-" * 70)
print(df.describe().T)
"""
BETİMSEL İSTATİSTİKLERDEN ÇIKARIMLAR:
- order_num_total_ever_online: Ortalama 3 alışveriş, max 200 (aykırı değer!)
- order_num_total_ever_offline: Ortalama 1.9 alışveriş
- customer_value: Ortalama 800-900 TL arası
- MAX değerler çok yüksek → Aykırı değer olabilir
- MIN değerler 0 → Hiç alışveriş yapmayan müşteriler?
"""

# e. Boş değer kontrolü
print("\n" + "-" * 70)
print("E) BOŞ DEĞER KONTROLÜ")
print("-" * 70)
print(df.isnull().sum())
print(f"\nToplam boş değer: {df.isnull().sum().sum()}")
"""
SONUÇ: 
✓ Veri setinde boş değer yok! 
  Bu gerçek hayatta nadiren görülür, veri kalitesi yüksek.
"""

# f. Değişken tipleri
print("\n" + "-" * 70)
print("F) DEĞİŞKEN TİPLERİ")
print("-" * 70)
print(df.dtypes)
print("\nTip Dağılımı:")
print(df.dtypes.value_counts())
"""
DİKKAT EDİLMESİ GEREKENLER:
- Tarih sütunları 'object' tipinde → datetime'a çevrilmeli
- Sayısal değerler float64 → integer'a çevrilebilir (frequency için)
- Kategori sütunu object → Bu normal
"""

# 3. OMNİCHANNEL YENİ DEĞİŞKENLER
print("\n" + "-" * 70)
print("3) OMNİCHANNEL YENİ DEĞİŞKENLER OLUŞTURMA")
print("-" * 70)

# Toplam alışveriş sayısı (online + offline)
df["order_num_total"] = (
    df["order_num_total_ever_online"] + 
    df["order_num_total_ever_offline"]
)

# Toplam harcama (online + offline)
df["customer_value_total"] = (
    df["customer_value_total_ever_online"] + 
    df["customer_value_total_ever_offline"]
)

print("✓ Yeni değişkenler oluşturuldu:")
print("  - order_num_total: Toplam alışveriş sayısı")
print("  - customer_value_total: Toplam harcama")
print("\nÖrnek veriler:")
print(df[["order_num_total", "customer_value_total"]].head())

"""
NEDEN BU DEĞİŞKENLERİ OLUŞTURDUK?
1. OmniChannel müşterilerin TOPLAM davranışını görmek için
2. RFM'de Frequency ve Monetary bu toplam değerlerle hesaplanacak
3. Online ve offline'ı ayrı değerlendirmek yanıltıcı olabilir
   Örn: Bir müşteri online 1, offline 10 alışveriş yapmış → Toplam 11!
"""

# 4. TARİH DEĞİŞKENLERİNİ DATETIME'A ÇEVİRME
print("\n" + "-" * 70)
print("4) TARİH DEĞİŞKENLERİNİ DATETIME'A ÇEVİRME")
print("-" * 70)

# Tarih sütunlarını belirleme
date_columns = [col for col in df.columns if "date" in col]
print(f"Tarih sütunları: {date_columns}")

# Datetime'a çevirme
for col in date_columns:
    df[col] = pd.to_datetime(df[col])

print("\n✓ Tarih sütunları datetime formatına çevrildi!")
print("\nYeni veri tipleri:")
print(df[date_columns].dtypes)

"""
DATETIME'A ÇEVİRMENİN ÖNEMİ:
1. Tarih hesaplamaları yapabilmek için (bugün - son alışveriş = recency)
2. Pandas datetime fonksiyonlarını kullanabilmek
3. Yıl, ay, gün gibi bileşenlere erişebilmek
4. Zaman serisi analizleri yapabilmek

NOT: pd.to_datetime otomatik olarak formatı algılar!
"""

# 5. ALIŞVERIŞ KANALLARINDA DAĞILIM ANALİZİ
print("\n" + "-" * 70)
print("5) ALIŞVERIŞ KANALLARINDA DAĞILIM ANALİZİ")
print("-" * 70)

# Kanala göre gruplama
channel_analysis = df.groupby("order_channel").agg({
    "master_id": "count",                    # Müşteri sayısı
    "order_num_total": "sum",                # Toplam alışveriş
    "customer_value_total": "sum"            # Toplam harcama
})

# Sütun isimlerini değiştirme
channel_analysis.columns = ["Müşteri_Sayısı", "Toplam_Alışveriş", "Toplam_Harcama"]

# Ortalama hesaplama
channel_analysis["Ortalama_Alışveriş"] = (
    channel_analysis["Toplam_Alışveriş"] / channel_analysis["Müşteri_Sayısı"]
)
channel_analysis["Ortalama_Harcama"] = (
    channel_analysis["Toplam_Harcama"] / channel_analysis["Müşteri_Sayısı"]
)

print(channel_analysis.round(2))

"""
KANAL ANALİZİNDEN ÇIKARIMLAR:
- Hangi kanal daha karlı?
- Hangi kanalda müşteri sayısı daha fazla?
- Ortalama sepet değeri hangi kanalda yüksek?

STRATEJİK KARARLAR:
- Düşük performanslı kanallara yatırım azaltılabilir
- Yüksek performanslı kanallarda kampanyalar artırılabilir
- Mobil uygulama kullanıcıları teşvik edilebilir
"""

# 6. EN FAZLA KAZANÇ GETİREN İLK 10 MÜŞTERİ
print("\n" + "-" * 70)
print("6) EN FAZLA KAZANÇ GETİREN İLK 10 MÜŞTERİ")
print("-" * 70)

top_10_revenue = df.sort_values("customer_value_total", ascending=False).head(10)
print(top_10_revenue[["master_id", "customer_value_total", "order_num_total"]])

"""
EN DEĞERLİ MÜŞTERİLER:
- Bu müşteriler "VIP" olarak işaretlenebilir
- Özel kampanyalar ve fırsatlar sunulabilir
- Kaybedilmemeleri için özel ilgi gösterilmeli
- Kişisel hesap yöneticisi atanabilir

PARETO PRENSİBİ: 
Muhtemelen bu müşterilerin %20'si, toplam gelirin %80'ini oluşturuyordur!
"""

# 7. EN FAZLA SİPARİŞ VEREN İLK 10 MÜŞTERİ
print("\n" + "-" * 70)
print("7) EN FAZLA SİPARİŞ VEREN İLK 10 MÜŞTERİ")
print("-" * 70)

top_10_orders = df.sort_values("order_num_total", ascending=False).head(10)
print(top_10_orders[["master_id", "order_num_total", "customer_value_total"]])

"""
SIK ALIŞVERİŞ YAPAN MÜŞTERİLER:
- Yüksek frequency → Sadık müşteriler
- Marka bağlılığı yüksek
- Ürün çeşitliliği deneyenler
- Cross-sell/up-sell potansiyeli yüksek

DİKKAT: 
Çok alışveriş yapan ≠ Çok para harcayan
Bu iki grubu karşılaştırmak stratejik öneme sahip!
"""

# 8. VERİ ÖN HAZIRLIK SÜRECİNİ FONKSİYONLAŞTIRMA
print("\n" + "-" * 70)
print("8) VERİ ÖN HAZIRLIK FONKSİYONU")
print("-" * 70)

def data_preparation(dataframe):
    """
    FLO veri setini RFM analizi için hazırlayan fonksiyon
    
    Parameters
    ----------
    dataframe : DataFrame
        Ham FLO veri seti
    
    Returns
    -------
    DataFrame
        Temizlenmiş ve hazırlanmış veri seti
    
    İşlem Adımları:
    ---------------
    1. Tarih sütunlarını datetime'a çevirme
    2. Omnichannel değişkenler oluşturma (toplam alışveriş ve harcama)
    3. Veri tiplerini kontrol etme
    
    Örnek Kullanım:
    ---------------
    >>> df = pd.read_csv("flo_data_20k.csv")
    >>> df_prepared = data_preparation(df)
    """
    
    # 1. Tarih sütunlarını datetime'a çevirme
    date_columns = [col for col in dataframe.columns if "date" in col]
    for col in date_columns:
        dataframe[col] = pd.to_datetime(dataframe[col])
    
    # 2. Omnichannel toplam değişkenler
    dataframe["order_num_total"] = (
        dataframe["order_num_total_ever_online"] + 
        dataframe["order_num_total_ever_offline"]
    )
    
    dataframe["customer_value_total"] = (
        dataframe["customer_value_total_ever_online"] + 
        dataframe["customer_value_total_ever_offline"]
    )
    
    return dataframe

# Fonksiyonu test etme
df_test = df_.copy()
df_prepared = data_preparation(df_test)
print("✓ Veri hazırlık fonksiyonu başarıyla oluşturuldu ve test edildi!")

"""
FONKSİYONLAŞTIRMANIN FAYDALARI:
1. Kod tekrarını önler (DRY: Don't Repeat Yourself)
2. Yeni veri geldiğinde tek satırla çalıştırılabilir
3. Hata yapma olasılığı azalır
4. Kodun okunabilirliği artar
5. Test edilebilir (unit test yazılabilir)

GERÇEK HAYAT SENARYOSU:
Her ay yeni veri geldiğinde bu fonksiyon otomatik çalıştırılabilir!
"""

###############################################################
# GÖREV 2: RFM Metriklerinin Hesaplanması
###############################################################

print("\n" + "=" * 70)
print("GÖREV 2: RFM METRİKLERİNİN HESAPLANMASI")
print("=" * 70)

"""
RFM NEDİR?
R - Recency: Müşterinin son alışverişinden bu yana geçen süre
F - Frequency: Müşterinin toplam alışveriş sayısı
M - Monetary: Müşterinin toplam harcaması

NEDEN ÖNEMLİDİR?
- Basit ama güçlü bir segmentasyon yöntemi
- Müşteri davranışını 3 kritik metrikle özetler
- Actionable insights sağlar (eyleme dönüştürülebilir)
"""

# Analiz tarihi belirleme (en son alışverişten 2 gün sonrası)
df["last_order_date"].max()  # En son alışveriş tarihi
analysis_date = df["last_order_date"].max() + dt.timedelta(days=2)
print(f"\nAnaliz Tarihi: {analysis_date.date()}")

"""
ANALİZ TARİHİ NEDEN ÖNEMLİ?
- Recency hesaplaması için referans nokta
- Gerçek hayatta "bugün" olarak alınır
- Burada en son alışveriş + 2 gün (veri seti tarihi geçmiş olduğu için)

ÖNEMLİ NOT:
Gerçek bir projede: analysis_date = dt.datetime.now()
"""

# RFM metriklerini hesaplama
rfm = df.groupby('master_id').agg({
    'last_order_date': lambda date: (analysis_date - date.max()).days,  # Recency
    'order_num_total': lambda num: num.sum(),                           # Frequency
    'customer_value_total': lambda value: value.sum()                   # Monetary
})

# Sütun isimlerini değiştirme
rfm.columns = ['recency', 'frequency', 'monetary']

print("\n✓ RFM metrikleri hesaplandı!")
print("\nİlk 5 müşteri:")
print(rfm.head())

print("\nRFM İstatistikleri:")
print(rfm.describe().T)

"""
RFM HESAPLAMALARINDA DİKKAT EDİLECEKLER:

RECENCY:
- (analiz_tarihi - son_alışveriş_tarihi).days
- Küçük değer = İYİ (yakın zamanda alışveriş yapmış)
- Büyük değer = KÖTÜ (uzun süredir alışveriş yapmamış)

FREQUENCY:
- Toplam alışveriş sayısı
- Büyük değer = İYİ (sadık müşteri)
- Küçük değer = KÖTÜ (az alışveriş yapmış)

MONETARY:
- Toplam harcama miktarı
- Büyük değer = İYİ (değerli müşteri)
- Küçük değer = KÖTÜ (az harcama yapmış)

LAMBDA FONKSİYONLARI:
- lambda date: (analysis_date - date.max()).days
  → Her müşterinin SON alışveriş tarihini al, analiz tarihinden çıkar, gün cinsinden döndür
  
- lambda num: num.sum()
  → Her müşterinin TOPLAM alışveriş sayısını topla
  
- lambda value: value.sum()
  → Her müşterinin TOPLAM harcamasını topla
"""

###############################################################
# GÖREV 3: RF ve RFM Skorlarının Hesaplanması
###############################################################

print("\n" + "=" * 70)
print("GÖREV 3: RF VE RFM SKORLARININ HESAPLANMASI")
print("=" * 70)

"""
RFM SKORLAMA SÜRECİ:
1. Her metrik için 1-5 arası skor atama
2. Skorları birleştirerek segment oluşturma

NEDEN SKORLAMA?
- Farklı ölçeklerdeki metrikleri karşılaştırılabilir yapmak
- Standartlaştırma
- Segment tanımlama kolaylığı
"""

# Recency Skoru (küçük değer = yüksek skor, 5 en iyi)
rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])

# Frequency Skoru (büyük değer = yüksek skor, 5 en iyi)
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

# Monetary Skoru (büyük değer = yüksek skor, 5 en iyi)
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

print("✓ RFM skorları hesaplandı!")
print("\nİlk 5 müşteri (skorlu):")
print(rfm.head())

"""
PD.QCUT() FONKSİYONU:
- Quantile-based discretization (çeyrek tabanlı ayrıklaştırma)
- Veriyi eşit sayıda gözlem içeren parçalara böler
- Örnek: 5 parça → Her parça %20 veri içerir

NEDEN RANK(METHOD="FIRST")?
- Frequency'de aynı değerler olabilir (örn: 10 kişi tam 3 alışveriş yapmış)
- qcut() aynı değerlerle çalışırken hata verebilir
- rank(method="first") her değere benzersiz sıra numarası verir
- İlk gelen değere öncelik verir

RECENCY SKORLAMA MANTIĞI:
- Recency = 1 gün  → Skor 5 (mükemmel!)
- Recency = 365 gün → Skor 1 (kötü!)
- labels=[5,4,3,2,1] → Küçük recency'ye yüksek skor

FREQUENCY VE MONETARY SKORLAMA MANTIĞI:
- Frequency = 50 → Skor 5 (çok alışveriş)
- Frequency = 1  → Skor 1 (az alışveriş)
- labels=[1,2,3,4,5] → Büyük değere yüksek skor
"""

# RF Skoru oluşturma (Recency + Frequency)
rfm["RF_SCORE"] = (
    rfm['recency_score'].astype(str) + 
    rfm['frequency_score'].astype(str)
)

print("\n✓ RF skorları oluşturuldu!")
print("\nRF skor dağılımı:")
print(rfm["RF_SCORE"].value_counts().head(10))

"""
RF SKORU NEDEN OLUŞTURUYORUZ?
- Recency ve Frequency'yi tek bir değerde birleştirmek
- Örnek: RF = "55" → Hem yakın zamanda alışveriş yapmış (R=5)
                      hem de sık alışveriş yapıyor (F=5)
                      → CHAMPION müşteri!
- Örnek: RF = "11" → Ne yakın zamanda alışveriş yapmış (R=1)
                      ne de sık alışveriş yapıyor (F=1)
                      → HIBERNATING müşteri (uyuyan)

NEDEN MONETARY KULLANMIYORUZ?
- Segment tanımlamada genellikle R ve F yeterli
- M skorunu ayrı değerlendirebiliriz
- Bazı şirketler RFM yerine RF kullanıyor

ASTYPE(STR) NEDEN?
- 5 + 5 = 10 (sayısal toplama) → YANLIŞ!
- "5" + "5" = "55" (string birleştirme) → DOĞRU!
"""

###############################################################
# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması
###############################################################

print("\n" + "=" * 70)
print("GÖREV 4: RF SKORLARININ SEGMENT OLARAK TANIMLANMASI")
print("=" * 70)

"""
SEGMENT HARITASI (SEG_MAP):
RF skorlarını iş anlamına sahip segment isimlerine dönüştürme

REGEX (REGULAR EXPRESSION) KULLANIMI:
- r'[1-2][1-2]' → İlk karakter 1 veya 2, ikinci karakter 1 veya 2
- Eşleşenler: 11, 12, 21, 22
"""

# Segment haritası
seg_map = {
    r'[1-2][1-2]': 'hibernating',        # Uyuyan müşteriler
    r'[1-2][3-4]': 'at_risk',            # Risk altındaki müşteriler
    r'[1-2]5': 'cant_loose',             # Kaybedilmemesi gereken müşteriler
    r'3[1-2]': 'about_to_sleep',         # Uykuya dalmak üzere
    r'33': 'need_attention',             # İlgi gerektiren müşteriler
    r'[3-4][4-5]': 'loyal_customers',    # Sadık müşteriler
    r'41': 'promising',                   # Umut vaat eden müşteriler
    r'51': 'new_customers',              # Yeni müşteriler
    r'[4-5][2-3]': 'potential_loyalists', # Potansiyel sadık müşteriler
    r'5[4-5]': 'champions'               # Şampiyon müşteriler (en iyiler!)
}

# Segmentleri atama
rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)

print("✓ Segmentler oluşturuldu!")
print("\nSegment dağılımı:")
print(rfm['segment'].value_counts())

"""
SEGMENT AÇIKLAMALARI:

1. CHAMPIONS (54, 55):
   - En değerli müşteriler
   - Yakın zamanda alışveriş yapmış + Sık alışveriş yapıyor
   - Strateji: VIP muamelesi, erken erişim, özel kampanyalar

2. LOYAL_CUSTOMERS (34, 35, 44, 45):
   - Sadık müşteriler
   - Düzenli alışveriş yapıyorlar
   - Strateji: Sadakat programı, cross-sell

3. POTENTIAL_LOYALISTS (42, 43, 52, 53):
   - Sadık olma potansiyeli yüksek
   - Yakın zamanda alışveriş yapmış ama frequency orta
   - Strateji: Sadakat programına davet, membership

4. NEW_CUSTOMERS (51):
   - Yeni müşteriler
   - Yakın zamanda ilk alışverişi yapmış
   - Strateji: Hoş geldin kampanyası, deneme fırsatları

5. PROMISING (41):
   - Umut vaat eden yeni müşteriler
   - Az alışveriş yapmış ama yakın zamanda
   - Strateji: Cross-sell fırsatları

6. NEED_ATTENTION (33):
   - Orta düzey müşteriler
   - İlgi gerektiriyor
   - Strateji: Kişiselleştirilmiş kampanyalar

7. ABOUT_TO_SLEEP (31, 32):
   - Uykuya dalmak üzere
   - Alışveriş sıklığı azalmış
   - Strateji: Hatırlatma e-postaları

8. AT_RISK (13, 14, 23, 24):
   - Risk altında
   - Eskiden iyi müşteriydi, şimdi uzaklaşmış
   - Strateji: Geri kazanma kampanyası

9. CANT_LOOSE (15, 25):
   - Kaybedilmemesi gereken
   - Çok alışveriş yapıyordu ama uzun süredir yok
   - Strateji: Agresif kampanyalar, özel teklifler

10. HIBERNATING (11, 12, 21, 22):
    - Uyuyan müşteriler
    - Uzun süredir alışveriş yapmamış + Az alışveriş yapmış
    - Strateji: Yeniden aktivasyon, özel indirimler

REGEX ÖRNEKLERI:
r'[1-2][1-2]' → 11, 12, 21, 22 (hibernating)
r'5[4-5]'     → 54, 55 (champions)
r'[3-4][4-5]' → 34, 35, 44, 45 (loyal_customers)
"""

###############################################################
# GÖREV 5: Aksiyon Zamanı!
###############################################################

print("\n" + "=" * 70)
print("GÖREV 5: AKSİYON ZAMANI!")
print("=" * 70)

# 1. Segmentlerin RFM ortalamalarını inceleme
print("\n1) SEGMENT ORTALAMALARINI İNCELEME")
print("-" * 70)

segment_analysis = rfm.groupby("segment").agg({
    "recency": "mean",
    "frequency": "mean",
    "monetary": "mean"
})

print(segment_analysis.round(2))

"""
SEGMENT ANALİZİNDEN ÇIKARIMLAR:

Champions:
- Recency: Çok düşük (yakın zamanda alışveriş)
- Frequency: Çok yüksek (sık alışveriş)
- Monetary: Çok yüksek (çok harcama)
→ EN DEĞERLİ SEGMENT!

Hibernating:
- Recency: Çok yüksek (uzun süredir yok)
- Frequency: Düşük (az alışveriş)
- Monetary: Düşük (az harcama)
→ EN DÜŞÜK PERFORMANS!

At_Risk:
- Recency: Yüksek (uzaklaşmış)
- Frequency: Orta-Yüksek (eskiden iyiydi)
- Monetary: Orta-Yüksek (eskiden çok harcardı)
→ ACİL MÜDAHALE GEREKTİRİYOR!

STRATEJİK ÖNEME SAHİP SEGMENTLER:
1. Champions → Elde tutmak
2. At_Risk → Geri kazanmak
3. Cant_Loose → Kaybetmemek
4. Potential_Loyalists → Geliştirmek
"""

# 2. İş Case'leri

# CASE A: Yeni Kadın Ayakkabı Markası
print("\n" + "-" * 70)
print("CASE A: YENİ KADIN AYAKKABI MARKASI")
print("-" * 70)

"""
İŞ PROBLEMİ:
FLO yeni bir kadın ayakkabı markası dahil ediyor.
Ürün fiyatları genel tercihlerin üstünde (premium segment)

HEDEF MÜŞTERİ PROFİLİ:
- Sadık müşteriler (champions, loyal_customers)
- Ortalama 250 TL üzeri harcama yapanlar
- Kadın kategorisinden alışveriş yapanlar

STRATEJİ:
Bu profildeki müşterilere özel tanıtım ve ilk alım indirimi
"""

# Dataframe'i birleştirme (rfm + df)
rfm_df = rfm.merge(df[['master_id', 'interested_in_categories_12']], 
                   left_index=True, 
                   right_on='master_id', 
                   how='left')

# Hedef müşterileri filtreleme
target_customers_a = rfm_df[
    (rfm_df['segment'].isin(['champions', 'loyal_customers'])) &  # Sadık müşteriler
    (rfm_df['monetary'] > 250) &                                   # 250 TL üzeri harcama
    (rfm_df['interested_in_categories_12'].str.contains('KADIN', na=False))  # Kadın kategorisi
]

print(f"✓ Hedef müşteri sayısı: {len(target_customers_a)}")
print(f"  Toplam potansiyel gelir: {target_customers_a['monetary'].sum():,.2f} TL")
print(f"  Ortalama müşteri değeri: {target_customers_a['monetary'].mean():,.2f} TL")

# CSV'ye kaydetme
target_customers_a[['master_id']].to_csv('yeni_marka_hedef_musteri_id.csv', index=False)
print("\n✓ Hedef müşteri ID'leri 'yeni_marka_hedef_musteri_id.csv' dosyasına kaydedildi!")

"""
FİLTRELEME MANTIĞI:

1. rfm_df['segment'].isin(['champions', 'loyal_customers'])
   → Segment'i champions VEYA loyal_customers olanlar
   → isin() fonksiyonu liste içindeki değerleri kontrol eder

2. rfm_df['monetary'] > 250
   → Monetary değeri 250'den büyük olanlar
   → Premium ürünleri karşılayabilecek müşteriler

3. rfm_df['interested_in_categories_12'].str.contains('KADIN', na=False)
   → Kategori listesinde 'KADIN' kelimesi geçenler
   → str.contains(): String içinde arama yapar
   → na=False: NaN değerleri False olarak kabul et (hata vermesin)

PARANTEZ KULLANIMI:
- Her koşul parantez içinde olmalı
- & operatörü ile birleştirme (VE mantığı)
- | operatörü OR (VEYA) mantığı için kullanılır

BEKLENEN SONUÇ:
- Yüksek gelirli, sadık, kadın ürünlerine ilgili müşteriler
- Bu müşterilere premium marka tanıtımı yapılabilir
- İlk alım için %10-15 özel indirim önerilebilir
"""

# CASE B: Erkek ve Çocuk Ürünlerinde İndirim
print("\n" + "-" * 70)
print("CASE B: ERKEK VE ÇOCUK ÜRÜNLERİNDE %40 İNDİRİM")
print("-" * 70)

"""
İŞ PROBLEMİ:
Erkek ve Çocuk ürünlerinde %40'a yakın indirim planlanıyor

HEDEF MÜŞTERİ PROFİLİ:
- Cant_loose: Kaybedilmemesi gereken (eskiden çok alışveriş yapıyordu)
- About_to_sleep: Uykuya dalmak üzere
- New_customers: Yeni müşteriler
- Erkek veya Çocuk kategorisinden ilgilenenler

STRATEJİ:
1. Cant_loose: "Seni özledik! Özel %40 indirim"
2. About_to_sleep: "Geri dön, seni bekliyoruz!"
3. New_customers: "İlk alışverişine özel fırsat!"
"""

# Hedef müşterileri filtreleme
target_customers_b = rfm_df[
    (rfm_df['segment'].isin(['cant_loose', 'about_to_sleep', 'new_customers'])) &  # Hedef segmentler
    (
        (rfm_df['interested_in_categories_12'].str.contains('ERKEK', na=False)) |  # ERKEK veya
        (rfm_df['interested_in_categories_12'].str.contains('COCUK', na=False))    # ÇOCUK
    )
]

print(f"✓ Hedef müşteri sayısı: {len(target_customers_b)}")
print(f"  Segment dağılımı:")
print(target_customers_b['segment'].value_counts())

# CSV'ye kaydetme
target_customers_b[['master_id']].to_csv('indirim_hedef_musteri_ids.csv', index=False)
print("\n✓ Hedef müşteri ID'leri 'indirim_hedef_musteri_ids.csv' dosyasına kaydedildi!")

"""
KARMAŞIK FİLTRELEME MANTIĞI:

1. Segment filtresi:
   (rfm_df['segment'].isin(['cant_loose', 'about_to_sleep', 'new_customers']))
   → 3 segmentten herhangi biri

2. Kategori filtresi (İÇ İÇE PARANTEZLER):
   (
       (str.contains('ERKEK', na=False)) |   # ERKEK içerenler VEYA
       (str.contains('COCUK', na=False))     # ÇOCUK içerenler
   )
   → | operatörü OR (VEYA) mantığı
   → En az birinden alışveriş yapanlar

3. & ile birleştirme:
   (Segment koşulu) & (Kategori koşulu)
   → Her ikisi de TRUE olmalı (AND mantığı)

PARANTEZ HIYERARŞISI:
- En içteki parantezler önce değerlendirilir
- Dış parantez tüm OR mantığını gruplar
- En dış & ile segment filtresine bağlanır

BEKLENEN SONUÇ:
- Risk altındaki veya yeni müşteriler
- Erkek/Çocuk ürünlerine ilgili
- %40 indirimle geri kazanılabilir veya sadakat sağlanabilir

KAMPANYA MESAJLARI:
Cant_loose: "Özledik sizi! Erkek/Çocuk ürünlerinde %40 indirim!"
About_to_sleep: "Uyanma zamanı! Sizin için özel fırsatlar!"
New_customers: "Hoş geldiniz! İlk alışverişinize özel %40 indirim!"
"""

###############################################################
# GÖREV 6: Tüm Süreci Fonksiyonlaştırma
###############################################################

print("\n" + "=" * 70)
print("GÖREV 6: TÜM SÜRECİ FONKSİYONLAŞTIRMA")
print("=" * 70)

def create_rfm_segments(dataframe, csv=False):
    """
    FLO veri seti için RFM analizi yapan ve segmentlere ayıran fonksiyon
    
    Parameters
    ----------
    dataframe : DataFrame
        Ham FLO veri seti
    csv : bool, default False
        True ise sonuçları CSV dosyasına kaydeder
    
    Returns
    -------
    rfm : DataFrame
        RFM metrikleri, skorları ve segmentleri içeren dataframe
    
    İşlem Adımları
    --------------
    1. Veri hazırlama (tarih dönüşümleri, yeni değişkenler)
    2. RFM metriklerini hesaplama
    3. RFM skorlarını oluşturma
    4. Segmentlere ayırma
    
    Örnek Kullanım
    --------------
    >>> df = pd.read_csv("flo_data_20k.csv")
    >>> rfm = create_rfm_segments(df, csv=True)
    >>> print(rfm['segment'].value_counts())
    
    Not
    ---
    - Analiz tarihi: En son alışveriş + 2 gün
    - Segment tanımları: champions, loyal_customers, vs.
    - CSV çıktı: rfm_segments.csv
    """
    
    # 1. VERİ HAZIRLAMA
    # ------------------
    
    # Tarih sütunlarını datetime'a çevirme
    date_columns = [col for col in dataframe.columns if "date" in col]
    for col in date_columns:
        dataframe[col] = pd.to_datetime(dataframe[col])
    
    # Omnichannel toplam değişkenler
    dataframe["order_num_total"] = (
        dataframe["order_num_total_ever_online"] + 
        dataframe["order_num_total_ever_offline"]
    )
    
    dataframe["customer_value_total"] = (
        dataframe["customer_value_total_ever_online"] + 
        dataframe["customer_value_total_ever_offline"]
    )
    
    # 2. RFM METRİKLERİNİ HESAPLAMA
    # -------------------------------
    
    # Analiz tarihi
    analysis_date = dataframe["last_order_date"].max() + dt.timedelta(days=2)
    
    # RFM hesaplama
    rfm = dataframe.groupby('master_id').agg({
        'last_order_date': lambda date: (analysis_date - date.max()).days,
        'order_num_total': lambda num: num.sum(),
        'customer_value_total': lambda value: value.sum()
    })
    
    rfm.columns = ['recency', 'frequency', 'monetary']
    
    # 3. RFM SKORLARINI OLUŞTURMA
    # -----------------------------
    
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])
    
    # RF skoru
    rfm["RF_SCORE"] = (
        rfm['recency_score'].astype(str) + 
        rfm['frequency_score'].astype(str)
    )
    
    # 4. SEGMENTLERE AYIRMA
    # ----------------------
    
    seg_map = {
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
    
    rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)
    
    # 5. CSV'YE KAYDETME (OPSİYONEL)
    # --------------------------------
    
    if csv:
        rfm.to_csv("rfm_segments.csv")
        print("✓ RFM segmentleri 'rfm_segments.csv' dosyasına kaydedildi!")
    
    return rfm

# Fonksiyonu test etme
print("\n✓ RFM segmentasyon fonksiyonu oluşturuldu!")
print("\nFonksiyonu test ediyoruz...")

df_test = pd.read_csv("datasets/flo_data_20k.csv")
rfm_result = create_rfm_segments(df_test, csv=True)

print("\n✓ Fonksiyon başarıyla test edildi!")
print(f"\nOluşturulan segment sayıları:")
print(rfm_result['segment'].value_counts())

"""
FONKSİYON TASARIMI EN İYİ PRATİKLER:

1. DOCSTRING:
   - Fonksiyonun ne yaptığını açıklar
   - Parametreleri ve dönüş değerlerini belirtir
   - Kullanım örnekleri içerir
   - Google/NumPy/Sphinx formatlarından biri kullanılır

2. PARAMETRELERİN VARSAYILAN DEĞERLERİ:
   - csv=False: Kullanıcı istemezse CSV oluşturulmaz
   - Esneklik sağlar

3. AÇIKLAYICI YORUMLAR:
   - Her bölüm açıkça belirtilmiş
   - Başlıklar ve ayırıcılar kullanılmış

4. MODÜLER YAPI:
   - Her adım kendi bölümünde
   - Gerekirse her bölüm ayrı fonksiyon yapılabilir

5. HATA YÖNETİMİ (İLERİ SEVİYE):
   ```python
   try:
       # İşlemler
   except Exception as e:
       print(f"Hata: {e}")
       return None
   ```

6. LOGLAMAç (İLERİ SEVİYE):
   ```python
   import logging
   logging.info("RFM analizi başladı...")
   ```

GERÇEK HAYAT KULLANIMI:
Bu fonksiyon bir Python script'i olarak kaydedilip
cron job veya airflow ile otomatize edilebilir:

# rfm_automation.py
df = pd.read_csv("data/latest_flo_data.csv")
rfm = create_rfm_segments(df, csv=True)
send_email_to_marketing_team(rfm)  # Pazarlama ekibine mail gönder
"""

print("\n" + "=" * 70)
print("✓ FLO RFM ANALİZİ TAMAMLANDI!")
print("=" * 70)
print("""
ÇIKTILAR:
1. rfm_segments.csv - Tüm müşterilerin RFM segmentleri
2. yeni_marka_hedef_musteri_id.csv - Premium kadın ayakkabı hedef kitle
3. indirim_hedef_musteri_ids.csv - Erkek/Çocuk indirim hedef kitle

SONRAKI ADIMLAR:
1. Pazarlama ekibiyle segment stratejilerini görüş
2. A/B testleri tasarla (kampanya başarısını ölç)
3. Segmentleri düzenli olarak güncelle (aylık/haftalık)
4. CLTV tahmini ile birleştir (daha detaylı analiz)
5. Otomasyonu kur (yeni veri geldiğinde otomatik çalışsın)
""")

"""
ÖĞRENİLEN TEMEL KAVRAMLAR:

1. RFM ANALİZİ:
   - Recency, Frequency, Monetary metrikleri
   - Müşteri segmentasyonu
   - Skorlama ve segment tanımlama

2. PANDAS İŞLEMLERİ:
   - groupby() ve agg() kullanımı
   - Lambda fonksiyonları
   - pd.qcut() ile skorlama
   - String işlemleri (str.contains)
   - Tarih işlemleri (datetime)

3. VERİ HAZIRLAMA:
   - Eksik değer kontrolü
   - Veri tipi dönüşümleri
   - Yeni değişken oluşturma
   - Veri birleştirme (merge)

4. İŞ ANLAYIŞI:
   - Segment tanımlama mantığı
   - Müşteri davranış analizi
   - Actionable insights oluşturma
   - Hedef kitle belirleme

5. PYTHON EN İYİ PRATİKLERİ:
   - Fonksiyonlaştırma
   - Docstring yazımı
   - Kod organizasyonu
   - Yorum satırları

GERÇEK HAYAT UYGULAMALARI:
✓ E-ticaret müşteri segmentasyonu
✓ Pazarlama kampanya hedefleme
✓ Müşteri elde tutma stratejileri
✓ Churn önleme programları
✓ Kişiselleştirilmiş ürün önerileri
✓ VIP müşteri programları

Bu analiz bir Data Scientist / CRM Analyst'in temel işidir!
"""
