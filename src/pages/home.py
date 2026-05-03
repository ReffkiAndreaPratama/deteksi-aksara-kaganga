"""pages/home.py — Halaman beranda."""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import config, utils
from components.ui import page_header, divider, stat_card


def render():
    st.markdown("""
    <div style="text-align:center;padding:48px 20px 32px">
      <div style="font-size:64px;margin-bottom:16px">🔍</div>
      <div style="font-family:'Space Grotesk',sans-serif;font-size:48px;font-weight:700;
                  background:linear-gradient(135deg,#6C63FF,#3ECFCF,#FF6584);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                  background-clip:text;line-height:1.1;margin-bottom:12px">
        AksaraDetect
      </div>
      <div style="font-size:18px;color:#8888AA;max-width:540px;margin:0 auto 32px;line-height:1.6">
        Deteksi aksara Ulu Rejang secara otomatis menggunakan YOLOv8.
        253 kelas aksara, bounding box real-time.
      </div>
    </div>
    """, unsafe_allow_html=True)

    metrics   = utils.load_metrics()
    log       = utils.load_prediction_log()
    yolo_m    = metrics.get("yolov8", {})
    map50     = yolo_m.get("metrics/mAP50(B)", yolo_m.get("metrics/mAP50", None))
    map5095   = yolo_m.get("metrics/mAP50-95(B)", yolo_m.get("metrics/mAP50-95", None))
    total_det = sum(e.get("count", 0) for e in log)

    c1, c2, c3, c4 = st.columns(4)
    with c1: stat_card("Jumlah Kelas",   "253",  "aksara Ulu Rejang", "#6C63FF")
    with c2: stat_card("mAP@50",
                       f"{map50*100:.1f}%" if map50 else "—",
                       "setelah training", "#3ECFCF")
    with c3: stat_card("mAP@50-95",
                       f"{map5095*100:.1f}%" if map5095 else "—",
                       "setelah training", "#FF6584")
    with c4: stat_card("Total Deteksi",  str(total_det), "aksara terdeteksi", "#FFD166")

    divider()

    features = [
        ("🎯", "Object Detection",
         "Deteksi banyak aksara sekaligus dalam satu gambar dengan bounding box presisi."),
        ("⚡", "YOLOv8",
         "Model state-of-the-art yang cepat dan akurat, tersedia dari nano hingga xlarge."),
        ("📊", "Analytics Lengkap",
         "mAP, confusion matrix, precision-recall curve, dan F1 curve tersedia."),
        ("📋", "Log Prediksi",
         "Setiap deteksi dicatat lengkap dengan timestamp, kelas, dan confidence."),
        ("🔄", "Dataset Siap",
         "Dataset Aksara Ulu Rejang v4 dari Roboflow sudah terintegrasi langsung."),
        ("⚙️", "Konfigurasi Mudah",
         "Semua parameter training ada di config.py — ganti model size, epoch, dll."),
    ]

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="vc-card" style="height:160px">
              <div style="font-size:28px;margin-bottom:10px">{icon}</div>
              <div style="font-family:'Space Grotesk',sans-serif;font-size:15px;
                          font-weight:600;color:#F0F0FF;margin-bottom:6px">{title}</div>
              <div style="font-size:13px;color:#8888AA;line-height:1.5">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    divider()

    st.markdown("""
    <div style="font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:600;
                color:#F0F0FF;margin-bottom:16px">Quick Start</div>
    """, unsafe_allow_html=True)

    for num, title, desc in [
        ("1", "Install dependensi",
         "<code>pip install -r requirements.txt</code>"),
        ("2", "Training model",
         "<code>cd src → python train.py</code> (atau <code>--model s</code> untuk lebih akurat)"),
        ("3", "Deteksi aksara",
         "Buka halaman <b>Detect</b>, upload gambar, lihat bounding box hasil deteksi"),
    ]:
        st.markdown(f"""
        <div style="display:flex;gap:16px;align-items:flex-start;margin-bottom:14px;
                    background:rgba(255,255,255,0.03);border:1px solid rgba(108,99,255,0.15);
                    border-radius:12px;padding:16px 20px">
          <div style="width:32px;height:32px;border-radius:50%;
                      background:linear-gradient(135deg,#6C63FF,#3ECFCF);
                      display:flex;align-items:center;justify-content:center;
                      font-weight:700;font-size:14px;flex-shrink:0;color:white">{num}</div>
          <div>
            <div style="font-weight:600;color:#F0F0FF;margin-bottom:4px">{title}</div>
            <div style="font-size:13px;color:#8888AA">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
