"""
config.py — Konfigurasi project YOLOv8 Aksara Ulu Rejang.
"""

import os

# ── Direktori ─────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "Aksara Ulu Rejang.v4-fix.yolov8")
DATA_YAML   = os.path.join(DATASET_DIR, "data.yaml")
MODEL_DIR   = os.path.join(BASE_DIR, "models")
RESULT_DIR  = os.path.join(BASE_DIR, "results")
LOG_DIR     = os.path.join(BASE_DIR, "logs")
RUNS_DIR    = os.path.join(BASE_DIR, "runs")

# ── Training ──────────────────────────────────────────────────────────────────
MODEL_SIZE   = "n"        # n=nano, s=small, m=medium, l=large, x=xlarge
EPOCHS       = 50
IMG_SIZE     = 640
BATCH_SIZE   = 16
PATIENCE     = 10         # early stopping
WORKERS      = 4
DEVICE       = "cpu"      # "cpu" atau "0" untuk GPU

# ── Model output ──────────────────────────────────────────────────────────────
TRAIN_RUN_NAME  = "aksara_ulu_yolov8"
MODEL_BEST_PATH = os.path.join(MODEL_DIR, "best.pt")
MODEL_LAST_PATH = os.path.join(MODEL_DIR, "last.pt")
LABEL_MAP_PATH  = os.path.join(MODEL_DIR, "label_map.json")
METRICS_PATH    = os.path.join(MODEL_DIR, "metrics.json")
PREDICT_LOG     = os.path.join(LOG_DIR,   "prediction_log.json")

# ── Aplikasi ──────────────────────────────────────────────────────────────────
APP_NAME    = "AksaraDetect"
APP_VERSION = "1.0.0"
APP_TAGLINE = "Aksara Ulu Rejang — YOLOv8 Object Detection"

# ── Confidence threshold ──────────────────────────────────────────────────────
CONF_THRESHOLD = 0.25
IOU_THRESHOLD  = 0.45
