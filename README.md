# VisionSafe: Big Data Ingestion & Analytics Pipeline

Repository ini berisi sistem otomatisasi pengumpulan data (Data Ingestion) dan analisis data untuk project **VisionSafe**. Sistem ini dirancang untuk memenuhi standar pengolahan Big Data dengan alur kerja yang otomatis dan terstruktur.

## 🚀 Fitur Utama
- **Automated Crawler:** Mengambil data dari 10+ sumber otoritas kesehatan dunia (WHO, NIH, Kemenkes, dll).
- **GitHub Actions Integration:** Proses crawling berjalan otomatis setiap hari tanpa intervensi manual.
- **Firebase Firestore Storage:** Data disimpan dalam database NoSQL yang scalable.
- **NLP Analytics:** Preprocessing teks bilingual dan visualisasi tren kesehatan mata.

## 📁 Struktur Folder
- `.github/workflows/`: Konfigurasi GitHub Actions untuk jadwal sinkronisasi harian.
- `data_ingestion.py`: Script Python utama untuk crawling dan ekstraksi data (SDA Elite Logic).
- `requirements.txt`: Daftar dependensi Python yang diperlukan.
- `DOKUMENTASI_COLAB_BIGDATA_FIX.txt`: Penjelasan teknis langkah-langkah pengerjaan tugas.

## 🛠️ Cara Penggunaan (Local Setup)
1. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
2. Set Environment Variable:
   Pastikan Anda memiliki file `serviceAccountKey.json` dari Firebase dan set ke dalam environment variable `FIREBASE_CONFIG`.
3. Jalankan ingestion manual:
   ```bash
   python data_ingestion.py
   ```

---
*Dibuat untuk penilaian mata kuliah Big Data - VisionSafe Project.*
