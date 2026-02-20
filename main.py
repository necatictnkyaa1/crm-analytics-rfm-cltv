"""
CRM Analytics - Ana Çalıştırma Dosyası
Bu dosyayı PyCharm'dan direkt çalıştırabilirsiniz!
"""

import pandas as pd
import sys
from pathlib import Path

# Proje dizinini Python path'ine ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.flo_rfm_analysis import create_rfm_segments, data_preparation
from src.flo_cltv_prediction import create_cltv_prediction
from src.config import DATA_DIR, OUTPUT_DIR, DATA_FILES

def main():
    """
    Ana çalıştırma fonksiyonu
    """
    print("=" * 70)
    print("CRM ANALYTICS - RFM & CLTV PREDICTION")
    print("=" * 70)
    
    # Veri yolunu belirle
    data_path = DATA_DIR / DATA_FILES["flo_data"]
    
    # Alternatif veri yolları (eğer yukarıdaki bulunamazsa)
    alternative_paths = [
        Path("data/flo_data_20k.csv"),
        Path("../data/flo_data_20k.csv"),
        Path("datasets/flo_data_20k.csv"),
    ]
    
    # Veri dosyasını bul
    if not data_path.exists():
        print(f"\n⚠️  Veri dosyası bulunamadı: {data_path}")
        print("\n🔍 Alternatif konumlar kontrol ediliyor...\n")
        
        for alt_path in alternative_paths:
            if alt_path.exists():
                data_path = alt_path
                print(f"✅ Veri dosyası bulundu: {data_path}")
                break
        else:
            print("\n❌ Hata: Veri dosyası hiçbir konumda bulunamadı!")
            print("\nLütfen veri dosyasını şu konumlardan birine koyun:")
            print(f"  1. {DATA_DIR / DATA_FILES['flo_data']}")
            for path in alternative_paths:
                print(f"  2. {path}")
            return
    
    print(f"\n📂 Veri dosyası: {data_path}")
    
    # Veriyi yükle
    print("\n" + "-" * 70)
    print("1️⃣  VERİYİ YÜKLEME")
    print("-" * 70)
    
    try:
        df = pd.read_csv(data_path)
        print(f"✅ Veri başarıyla yüklendi!")
        print(f"   Satır: {df.shape[0]:,}, Sütun: {df.shape[1]}")
    except Exception as e:
        print(f"❌ Veri yükleme hatası: {e}")
        return
    
    # RFM Analizi
    print("\n" + "=" * 70)
    print("2️⃣  RFM ANALİZİ ÇALIŞTIRILIYOR")
    print("=" * 70)
    
    try:
        rfm = create_rfm_segments(df.copy(), csv=False)
        print("\n✅ RFM analizi tamamlandı!")
        print(f"\n📊 Segment Dağılımı:")
        print(rfm['segment'].value_counts().to_string())
        
        # Segment ortalamalarını göster
        print(f"\n📈 Segment Ortalamaları:")
        segment_stats = rfm.groupby('segment').agg({
            'recency': 'mean',
            'frequency': 'mean',
            'monetary': 'mean'
        }).round(2)
        print(segment_stats.to_string())
        
        # RFM sonuçlarını kaydet
        rfm_output_path = OUTPUT_DIR / "rfm_segments.csv"
        rfm.to_csv(rfm_output_path)
        print(f"\n💾 RFM sonuçları kaydedildi: {rfm_output_path}")
        
    except Exception as e:
        print(f"❌ RFM analizi hatası: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # CLTV Prediction
    print("\n" + "=" * 70)
    print("3️⃣  CLTV PREDICTION ÇALIŞTIRILIYOR")
    print("=" * 70)
    
    try:
        cltv = create_cltv_prediction(df.copy(), month=6, segment_count=4)
        print("\n✅ CLTV tahmini tamamlandı!")
        
        # CLTV segment dağılımı
        print(f"\n📊 CLTV Segment Dağılımı:")
        cltv_segment_stats = cltv.groupby('cltv_segment').agg({
            'cltv': ['count', 'mean', 'sum']
        }).round(2)
        print(cltv_segment_stats.to_string())
        
        # En değerli 10 müşteri
        print(f"\n🏆 En Değerli 10 Müşteri:")
        top_10 = cltv.nlargest(10, 'cltv')[['cltv', 'frequency', 'monetary_cltv', 'cltv_segment']]
        print(top_10.to_string())
        
        # CLTV sonuçlarını kaydet
        cltv_output_path = OUTPUT_DIR / "cltv_prediction.csv"
        cltv.to_csv(cltv_output_path)
        print(f"\n💾 CLTV sonuçları kaydedildi: {cltv_output_path}")
        
    except Exception as e:
        print(f"❌ CLTV tahmini hatası: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Özet rapor
    print("\n" + "=" * 70)
    print("📋 ÖZET RAPOR")
    print("=" * 70)
    
    print(f"""
    ✅ RFM Analizi Tamamlandı
       - Toplam Müşteri: {len(rfm):,}
       - Champions: {len(rfm[rfm['segment'] == 'champions']):,}
       - At Risk: {len(rfm[rfm['segment'] == 'at_risk']):,}
       - Hibernating: {len(rfm[rfm['segment'] == 'hibernating']):,}
    
    ✅ CLTV Prediction Tamamlandı
       - 6 Aylık Tahmin
       - A Segment (Top 25%): {len(cltv[cltv['cltv_segment'] == 'A']):,} müşteri
       - Toplam Tahmini Gelir: {cltv['cltv'].sum():,.2f} TL
       - Ortalama CLTV: {cltv['cltv'].mean():,.2f} TL
    
    📂 Çıktı Dosyaları:
       - {rfm_output_path}
       - {cltv_output_path}
    """)
    
    print("=" * 70)
    print("✅ TÜM İŞLEMLER BAŞARIYLA TAMAMLANDI!")
    print("=" * 70)

if __name__ == "__main__":
    main()
