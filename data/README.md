# Data Klasörü

Bu klasöre veri dosyalarınızı koyun.

## Beklenen Dosyalar

- `flo_data_20k.csv` - FLO müşteri verileri (20,000 müşteri)

## Veri Yapısı

Veri setinde şu sütunlar olmalı:

- `master_id`: Müşteri ID
- `order_channel`: Alışveriş kanalı
- `last_order_channel`: Son alışveriş kanalı
- `first_order_date`: İlk alışveriş tarihi
- `last_order_date`: Son alışveriş tarihi
- `last_order_date_online`: Online son alışveriş
- `last_order_date_offline`: Offline son alışveriş
- `order_num_total_ever_online`: Online toplam alışveriş
- `order_num_total_ever_offline`: Offline toplam alışveriş
- `customer_value_total_ever_offline`: Offline toplam harcama
- `customer_value_total_ever_online`: Online toplam harcama
- `interested_in_categories_12`: Son 12 ay kategorileri

## Not

`.gitignore` dosyasında CSV dosyaları ignore edilmiştir.
Bu sayede büyük veri dosyaları Git'e yüklenmez.
