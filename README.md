# Student Vocabulary Analyzer API

## Teknoloji Stack

### **spaCy** 
- Doğal Dil İşleme (NLP) kütüphanesi
- Kelimeleri ayırma (tokenization)
- Kelimeleri kök formuna çevirme (lemmatization)
- Kelime türlerini belirleme (POS tagging)
- İngilizce dil modeli kullanıyor

### **pyspellchecker**
- Yazım hatalarını tespit etme ve düzeltme
- Yanlış yazılan kelimeleri doğru formlarına çeviriyor

## Kurulum

### 1. Virtual Environment ile

```bash
# Virtual environment oluştur
python -m venv venv

# Aktif et (Mac/Linux)
source venv/bin/activate

# Aktif et (Windows)
venv\\Scripts\\activate

# Paketleri yükle
pip install -r requirements.txt

# spaCy dil modelini indir
python -m spacy download en_core_web_sm

# Sunucuyu başlat
python main.py
```

## API Endpoints

### 1. Sağlık Kontrolü
```
GET /health
```

### 2. Tek Ders Analizi
```
POST /analyze-lesson
```

**Örnek Request:**
```json
{
    "transcript_text": "[S]: I went to my aunt and visited my grandmother...",
    "book_text": "Talking about Your First Trip Abroad..."
}
```

## API Dokümantasyonu

Sunucu çalışırken şu adreslerden API dokümantasyonuna erişebilirsiniz:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc