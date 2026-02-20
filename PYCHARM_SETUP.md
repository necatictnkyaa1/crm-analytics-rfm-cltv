# PyCharm Run Configuration

## main.py için Run Configuration Oluşturma

### Adım 1: Run Configuration Aç
1. Üst menüden: Run → Edit Configurations
2. Veya: Sağ üstteki dropdown menüden "Edit Configurations"

### Adım 2: Yeni Python Configuration Ekle
1. Sol üstteki + butonuna tıkla
2. "Python" seç

### Adım 3: Ayarları Yap
```
Name: CRM Analytics - Main
Script path: /path/to/crm_analytics_project/main.py
Working directory: /path/to/crm_analytics_project
Python interpreter: Project Default (Python 3.x)
```

### Adım 4: Kaydet
- OK butonuna tıkla

### Çalıştırma
- Üst menüden seçili configuration'ı seç
- Yeşil ▶️ play butonuna tıkla
- Veya: Shift + F10

## Alternatif: Direkt Çalıştırma

1. main.py dosyasını aç
2. Dosya içinde herhangi bir yere sağ tıkla
3. "Run 'main'" seç

## Debug Mode

1. main.py'de breakpoint koy (satır numarasının yanına tıkla)
2. Sağ tık → Debug 'main'
3. Veya: Shift + F9

## Console Output

Terminal'de çıktıları görmek için:
- View → Tool Windows → Run
- Veya: Alt + 4

## Common Issues

### "No module named 'src'"
→ Working directory'nin proje root'u olduğundan emin ol

### "Cannot find file"
→ Script path'in doğru olduğundan emin ol

### Import errors
→ Python interpreter'ın doğru seçildiğinden emin ol
