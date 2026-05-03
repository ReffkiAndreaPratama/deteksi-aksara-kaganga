# ⬡ VisionClassify v2.0

**Professional Image Classification System** — CNN + MobileNetV2, dataset-agnostic, production-ready GUI.

---

## 📁 Struktur Project

```
kaganga-detector/
├── dataset/
│   ├── train/              ← subfolder = nama kelas
│   └── test/               ← subfolder = nama kelas
├── models/                 ← model .h5, label_map.json, history (auto)
├── results/                ← grafik & laporan evaluasi (auto)
├── logs/                   ← TensorBoard logs & prediction log (auto)
└── src/
    ├── app.py              ← entry point GUI (streamlit run app.py)
    ├── train.py            ← training CLI
    ├── predict.py          ← prediksi CLI
    ├── config.py           ← semua konfigurasi
    ├── utils.py            ← fungsi pembantu
    ├── components/
    │   └── ui.py           ← komponen UI reusable
    ├── pages/
    │   ├── home.py         ← halaman beranda
    │   ├── predict.py      ← halaman prediksi
    │   ├── analytics.py    ← dashboard evaluasi
    │   ├── training.py     ← monitor training
    │   ├── history.py      ← riwayat prediksi
    │   └── settings.py     ← konfigurasi & info
    └── styles/
        └── theme.css       ← custom dark theme
```

---

## ⚙️ Instalasi

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

---

## 🗂️ Menyiapkan Dataset

```
dataset/
├── train/
│   ├── ka/     ← gambar aksara ka
│   ├── ga/
│   └── nga/
└── test/
    ├── ka/
    ├── ga/
    └── nga/
```

> Nama folder = nama kelas. Jumlah kelas dibaca otomatis.

---

## 🚀 Training

```bash
cd src

# CNN saja
python train.py

# CNN + MobileNetV2 + perbandingan
python train.py --mobilenet

# MobileNetV2 saja
python train.py --only-mobilenet
```

---

## 🖥️ Menjalankan GUI

```bash
cd src
streamlit run app.py
```

Buka browser di **http://localhost:8501**

### Halaman GUI:
| Halaman | Fungsi |
|---------|--------|
| 🏠 Home | Overview, quick stats, quick start guide |
| 🔍 Predict | Upload gambar → prediksi + radar chart |
| 📊 Analytics | Confusion matrix, accuracy/loss curves, perbandingan model |
| 📈 Training | Monitor history training per epoch |
| 📋 History | Log semua prediksi + export CSV |
| ⚙️ Settings | Konfigurasi, status file, info dataset |

---

## 🔮 Prediksi via CLI

```bash
cd src

# Satu gambar
python predict.py --image ../sample.jpg

# Dengan MobileNetV2
python predict.py --image ../sample.jpg --model mobilenet

# Batch (seluruh folder)
python predict.py --batch ../folder_gambar/
```

---

## 🔄 Mengganti Dataset

1. Kosongkan `dataset/train/` dan `dataset/test/`
2. Isi dengan dataset baru (struktur folder = nama kelas)
3. Hapus `models/` (opsional)
4. Jalankan ulang `python train.py`

**Zero code changes required.**

---

## ⚙️ Konfigurasi (`src/config.py`)

| Parameter | Default | Keterangan |
|-----------|---------|-----------|
| `IMG_SIZE` | 64 | Ukuran gambar (px) |
| `BATCH_SIZE` | 32 | Batch size |
| `EPOCHS` | 30 | Maks epoch |
| `LEARNING_RATE` | 1e-3 | Adam LR |
| `VALIDATION_SPLIT` | 0.2 | 20% train → val |
| `EARLY_STOPPING_PATIENCE` | 5 | Stop jika tidak improve |
| `ROTATION_RANGE` | 20 | Augmentasi rotasi |
| `ZOOM_RANGE` | 0.2 | Augmentasi zoom |
| `HORIZONTAL_FLIP` | True | Augmentasi flip |

---

## 🛠️ Troubleshooting

| Masalah | Solusi |
|---------|--------|
| `Folder tidak ditemukan` | Pastikan `dataset/train/` dan `dataset/test/` ada |
| `Model tidak ditemukan` | Jalankan `train.py` dulu |
| Memory error | Kurangi `BATCH_SIZE` atau `IMG_SIZE` |
| Akurasi rendah | Tambah data, naikkan `EPOCHS`, atau pakai `--mobilenet` |
| Port sudah dipakai | `streamlit run app.py --server.port 8502` |
