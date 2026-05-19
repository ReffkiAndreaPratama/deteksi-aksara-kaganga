# 📘 Panduan Lengkap — AksaraDetect

Dokumen ini berisi cara menjalankan project dan jawaban untuk pertanyaan yang mungkin ditanyakan saat presentasi/sidang.

---

## Cara Menjalankan (Lokal)

### Prasyarat
- Python 3.11 atau 3.12 (BUKAN 3.14)
- pip
- Git (opsional)

### Langkah

```bash
# 1. Clone repository
git clone https://github.com/ReffkiAndreaPratama/deteksi-aksara-kaganga.git
cd deteksi-aksara-kaganga

# 2. Buat virtual environment
py -3.11 -m venv venv

# 3. Aktivasi (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# 3. Aktivasi (Linux/Mac)
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Jalankan aplikasi
python -m streamlit run src/app.py
```

Buka browser: **http://localhost:8501**

### Kalau Error

| Error | Solusi |
|-------|--------|
| `streamlit not recognized` | Pastikan venv aktif (ada `(venv)` di terminal) |
| `No module named streamlit` | Jalankan `pip install -r requirements.txt` lagi |
| `Model tidak ditemukan` | Pastikan file `models/best.pt` ada |
| Python 3.14 tidak support | Install Python 3.11: `winget install Python.Python.3.11` |
| Port 8501 sudah dipakai | `python -m streamlit run src/app.py --server.port 8502` |

---

## Cara Akses Online (Streamlit Cloud)

Langsung buka URL:
```
https://deteksi-aksara-kaganga-xsy5xhb2kmxdpsaldsxcyb.streamlit.app
```

Tidak perlu install apa-apa. Bisa dibuka di HP/laptop/tablet.

> Jika app sedang "tidur" (tidak diakses beberapa hari), tunggu ~30 detik untuk bangun.

---

## Pertanyaan yang Mungkin Ditanyakan

### 1. "Apa itu YOLOv8?"

**YOLO** = You Only Look Once. Algoritma object detection real-time yang bisa mendeteksi banyak objek dalam satu gambar sekaligus.

**YOLOv8** adalah versi terbaru dari Ultralytics (2023), lebih akurat dan cepat dari versi sebelumnya. Kami pakai varian **YOLOv8n** (nano) — model paling ringan, cocok untuk deployment.

**Keunggulan YOLOv8:**
- Single-stage detector (langsung prediksi, tidak perlu region proposal)
- Real-time inference (~30ms per gambar di GPU)
- Anchor-free detection
- State-of-the-art accuracy

---

### 2. "Kenapa pakai YOLOv8, bukan CNN biasa?"

| Aspek | CNN Klasifikasi | YOLOv8 Detection |
|-------|----------------|------------------|
| Output | 1 label per gambar | Banyak objek + posisi (bbox) |
| Lokasi | Tidak tahu di mana | Tahu posisi setiap aksara |
| Multi-objek | Tidak bisa | Bisa deteksi 100+ objek sekaligus |
| Use case | "Gambar ini aksara apa?" | "Di mana saja aksara dalam gambar ini?" |

Kami butuh **deteksi** (tahu posisi), bukan hanya klasifikasi.

---

### 3. "Berapa akurasi modelnya?"

| Metric | Nilai | Penjelasan |
|--------|-------|------------|
| mAP@50 | 27.4% | Mean Average Precision pada IoU 50% |
| mAP@50-95 | 19.7% | Rata-rata mAP dari IoU 50% sampai 95% |
| Precision | 33.9% | Dari yang terdeteksi, berapa % yang benar |
| Recall | 37.6% | Dari yang seharusnya terdeteksi, berapa % yang ketemu |

**Kenapa masih rendah?**
- Dataset 253 kelas — sangat banyak untuk object detection
- Training baru 50 epoch dengan model nano (paling kecil)
- Beberapa aksara mirip secara visual

**Cara meningkatkan:**
- Training lebih lama (150+ epoch)
- Pakai model lebih besar (YOLOv8s atau YOLOv8m)
- Tambah data training
- Data augmentation lebih agresif

---

### 4. "Apa itu mAP?"

**mAP** = mean Average Precision.

- Hitung precision-recall curve untuk setiap kelas
- Hitung area di bawah kurva (AP) per kelas
- Rata-ratakan semua kelas → mAP

**mAP@50** = mAP dengan IoU threshold 50% (prediksi dianggap benar jika overlap ≥ 50% dengan ground truth).

**mAP@50-95** = rata-rata mAP dari IoU 50%, 55%, 60%, ..., 95%. Lebih strict.

---

### 5. "Apa itu IoU?"

**IoU** = Intersection over Union.

Mengukur seberapa overlap antara bounding box prediksi dengan ground truth:

```
IoU = Area Overlap / Area Union
```

- IoU = 1.0 → perfect match
- IoU = 0.5 → overlap 50%
- IoU = 0.0 → tidak overlap sama sekali

---

### 6. "Apa itu Confidence Threshold?"

Setiap deteksi punya confidence score (0-100%). Confidence threshold adalah batas minimum:

- Threshold 0.25 → tampilkan deteksi dengan confidence ≥ 25%
- Threshold tinggi (0.7) → hanya tampilkan yang model sangat yakin
- Threshold rendah (0.1) → tampilkan semua, termasuk yang kurang yakin

User bisa atur dari slider di halaman Detect.

---

### 7. "Apa itu NMS (Non-Maximum Suppression)?"

Saat model mendeteksi satu aksara, kadang menghasilkan beberapa bounding box yang overlap. **NMS** memilih box terbaik dan buang yang redundan.

**IoU threshold di NMS:**
- IoU tinggi (0.7) → lebih banyak box dipertahankan
- IoU rendah (0.3) → lebih agresif menghapus overlap

---

### 8. "Dataset dari mana?"

- **Sumber:** Roboflow (platform dataset computer vision)
- **Nama:** Aksara Ulu Rejang v4
- **Format:** YOLOv8 (gambar + label .txt)
- **Jumlah kelas:** 253 aksara
- **Split:** Train / Valid / Test
- **Annotasi:** Bounding box per aksara

---

### 9. "Aksara Ulu Rejang itu apa?"

Aksara Ulu Rejang adalah sistem tulisan tradisional suku Rejang di Provinsi Bengkulu, Sumatera. Termasuk rumpun aksara Brahmi (seperti aksara Jawa, Batak, Lampung).

**Karakteristik:**
- Ditulis dari kiri ke kanan
- Setiap karakter = satu suku kata (konsonan + vokal)
- 253 variasi (kombinasi konsonan + vokal + diakritik)
- Contoh: ka, ga, nga, ba, da, ta, sa, dll.

---

### 10. "Kenapa training di Google Colab?"

- Training butuh **GPU** (CUDA) — tanpa GPU bisa berjam-jam
- Google Colab menyediakan **T4 GPU gratis**
- Training 50 epoch di Colab: ~5-10 menit
- Training 50 epoch di CPU lokal: ~2-4 jam

---

### 11. "Framework apa yang dipakai untuk GUI?"

**Streamlit** — framework Python untuk membuat web app tanpa perlu HTML/JS/CSS manual.

**Kenapa Streamlit:**
- Pure Python (tidak perlu belajar frontend)
- Rapid prototyping (cepat bikin UI)
- Built-in widgets (slider, file uploader, charts)
- Free hosting (Streamlit Cloud)
- Cocok untuk demo ML/AI

---

### 12. "Bagaimana alur kerja sistem?"

```
User upload gambar
       ↓
Streamlit terima file → convert ke PIL Image
       ↓
PIL Image dikirim ke YOLOv8 model (model.predict())
       ↓
Model return: bounding boxes + class IDs + confidence
       ↓
Matplotlib gambar bounding box di atas gambar
       ↓
Hasil ditampilkan ke user + disimpan ke log
```

---

### 13. "Bisa deteksi berapa aksara sekaligus?"

Default: maksimal **100 objek per gambar** (bisa diatur sampai 500 dari UI). Tidak ada batasan jumlah gambar yang di-upload.

---

### 14. "Apa bedanya precision dan recall?"

**Precision:** Dari semua yang model bilang "ini aksara", berapa % yang benar?
- Precision tinggi = jarang salah deteksi (false positive rendah)

**Recall:** Dari semua aksara yang ada di gambar, berapa % yang berhasil ditemukan?
- Recall tinggi = jarang miss (false negative rendah)

**Trade-off:** Naikkan confidence threshold → precision naik, recall turun.

---

### 15. "Apa itu F1 Score?"

Harmonic mean dari precision dan recall:

```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

F1 Score model saat ini: **~35.6%**

---

### 16. "Kenapa pakai Python?"

- Ekosistem ML/AI terlengkap (PyTorch, TensorFlow, Ultralytics)
- Library computer vision mature (OpenCV, Pillow)
- Streamlit hanya support Python
- Mudah dipelajari dan di-maintain

---

### 17. "Library apa saja yang dipakai?"

| Library | Fungsi |
|---------|--------|
| ultralytics | Load & run model YOLOv8 |
| torch (PyTorch) | Backend deep learning |
| streamlit | Web GUI framework |
| opencv-python | Image processing |
| Pillow | Load/save gambar |
| matplotlib | Visualisasi (bounding box, charts) |
| pandas | Data manipulation & CSV export |
| numpy | Operasi numerik |
| PyYAML | Parse konfigurasi dataset |

---

### 18. "Bisa di-deploy di mana saja?"

| Platform | Gratis? | GPU? | URL Publik? |
|----------|---------|------|-------------|
| Streamlit Cloud | ✅ | ❌ | ✅ |
| Hugging Face Spaces | ✅ | ✅ (terbatas) | ✅ |
| Railway | ✅ (limit) | ❌ | ✅ |
| Docker (VPS) | Tergantung | Tergantung | ✅ |
| Lokal | ✅ | Tergantung | ❌ |

Saat ini di-deploy di **Streamlit Cloud** (gratis, tanpa GPU, inference di CPU).

---

### 19. "Apa kekurangan sistem ini?"

1. **Akurasi masih rendah** (27% mAP) — perlu training lebih lama
2. **Tidak real-time** — tidak bisa dari kamera langsung
3. **CPU inference** — lebih lambat dari GPU
4. **253 kelas terlalu banyak** — beberapa aksara sangat mirip
5. **Belum ada transliterasi** — hanya deteksi, belum bisa baca teks

---

### 20. "Apa rencana pengembangan ke depan?"

1. Training lebih lama + model lebih besar → akurasi naik
2. Transliterasi otomatis (aksara → teks Latin)
3. API endpoint untuk integrasi
4. Mobile app
5. Support aksara daerah lain (Lampung, Batak, Bugis)

---

### 21. "Bagaimana cara training ulang?"

1. Buka `train_colab.ipynb` di Google Colab
2. Aktifkan GPU (Runtime → T4 GPU)
3. Masukkan API key Roboflow
4. Jalankan semua cell
5. Download `best.pt`
6. Taruh di folder `models/`
7. Restart app

---

### 22. "Apa itu bounding box?"

Kotak persegi panjang yang menandai lokasi objek dalam gambar. Setiap bounding box punya:
- **Koordinat:** x1, y1 (kiri atas) dan x2, y2 (kanan bawah)
- **Class:** nama aksara yang terdeteksi
- **Confidence:** seberapa yakin model

---

### 23. "Apa perbedaan YOLOv8n, s, m, l, x?"

| Varian | Parameter | Speed | Accuracy | Ukuran |
|--------|-----------|-------|----------|--------|
| YOLOv8**n** (nano) | 3.2M | Tercepat | Terendah | ~6 MB |
| YOLOv8**s** (small) | 11.2M | Cepat | Sedang | ~22 MB |
| YOLOv8**m** (medium) | 25.9M | Sedang | Bagus | ~52 MB |
| YOLOv8**l** (large) | 43.7M | Lambat | Tinggi | ~87 MB |
| YOLOv8**x** (xlarge) | 68.2M | Terlambat | Tertinggi | ~131 MB |

Kami pakai **nano** karena ringan untuk deployment. Untuk akurasi lebih baik, bisa upgrade ke **small** atau **medium**.

---

### 24. "Bagaimana model belajar mendeteksi aksara?"

**Transfer Learning:**
1. Model YOLOv8n sudah pre-trained di dataset COCO (80 kelas objek umum)
2. Kami fine-tune (latih ulang) dengan dataset aksara Ulu Rejang
3. Model belajar fitur visual aksara dari ribuan contoh gambar
4. Setelah training, model bisa mengenali 253 kelas aksara

**Proses training:**
- Input: gambar + label (posisi bounding box setiap aksara)
- Model prediksi posisi & kelas
- Hitung loss (seberapa salah prediksi)
- Update weights (backpropagation)
- Ulangi sampai konvergen

---

### 25. "Apa kontribusi masing-masing anggota?"

| Anggota | Kontribusi |
|---------|-----------|
| Pebi Heriansyah | Dataset preparation, labeling, testing |
| Reffki Andrea Pratama | Development (kode, training, deployment) |
| Muhammad Farhan Dzakki | Dokumentasi, riset aksara, presentasi |

---

## Quick Demo Script (untuk presentasi)

1. Buka app (lokal atau Streamlit Cloud)
2. **Home** → tunjukkan overview & stats
3. **Detect** → upload gambar aksara → tunjukkan bounding box
4. Upload 3 gambar sekaligus → tunjukkan gallery view
5. Download hasil → tunjukkan file PNG dengan bbox
6. **Analytics** → tunjukkan radar chart & metrics
7. **History** → tunjukkan log & statistik
8. **Settings** → tunjukkan 253 kelas

**Durasi:** ~5-7 menit demo

---

## File-file Penting

| File | Fungsi | Wajib ada? |
|------|--------|-----------|
| `models/best.pt` | Model terlatih | ✅ Ya |
| `models/metrics.json` | Data metrics | ✅ Ya (untuk Analytics) |
| `src/app.py` | Entry point | ✅ Ya |
| `src/config.py` | Konfigurasi | ✅ Ya |
| `requirements.txt` | Dependencies | ✅ Ya |
| `train_colab.ipynb` | Notebook training | Opsional |
| `results/results.csv` | Training history | Opsional |
| `logs/prediction_log.json` | Log deteksi | Auto-generated |
