"""views/home.py — Landing page."""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import config, utils
from components.ui import divider, stat_card


def render():
    # Hero
    st.markdown("""
    <div style="padding:32px 0 24px">
      <div style="font-family:'Space Grotesk',sans-serif;font-size:40px;font-weight:700;
                  color:#F5F5FF;letter-spacing:-1px;line-height:1.1;margin-bottom:8px">
        Deteksi Aksara<br>
        <span style="background:linear-gradient(135deg,#6C63FF,#3ECFCF);
                     -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                     background-clip:text">Ulu Rejang</span>
      </div>
      <div style="font-size:15px;color:#666680;max-width:480px;line-height:1.7;margin-bottom:24px">
        Upload gambar, dapatkan deteksi aksara dengan bounding box.
        Powered by YOLOv8 object detection.
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <span style="padding:5px 12px;border-radius:6px;font-size:11px;font-weight:500;
                     background:#6C63FF12;color:#6C63FF;border:1px solid #6C63FF20">YOLOv8</span>
        <span style="padding:5px 12px;border-radius:6px;font-size:11px;font-weight:500;
                     background:#3ECFCF12;color:#3ECFCF;border:1px solid #3ECFCF20">Real-time</span>
        <span style="padding:5px 12px;border-radius:6px;font-size:11px;font-weight:500;
                     background:#FF658412;color:#FF6584;border:1px solid #FF658420">Multi-image</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    divider()

    # Metrics
    metrics = utils.load_metrics()
    log = utils.load_prediction_log()
    yolo_m = metrics.get("yolov8", metrics)
    map50 = yolo_m.get("metrics/mAP50(B)", yolo_m.get("metrics/mAP50", None))
    prec = yolo_m.get("metrics/precision(B)", yolo_m.get("metrics/precision", None))
    rec = yolo_m.get("metrics/recall(B)", yolo_m.get("metrics/recall", None))
    total_det = sum(e.get("count", 0) for e in log)

    num_classes = "253"
    try:
        if os.path.isfile(config.MODEL_BEST_PATH):
            from ultralytics import YOLO
            m = YOLO(config.MODEL_BEST_PATH)
            num_classes = str(len(m.names))
    except Exception:
        pass

    c1, c2, c3, c4 = st.columns(4)
    with c1: stat_card("Classes", num_classes, "aksara", "#6C63FF")
    with c2: stat_card("mAP@50", f"{map50*100:.1f}%" if map50 else "—", "accuracy", "#3ECFCF")
    with c3: stat_card("Precision", f"{prec*100:.1f}%" if prec else "—", "", "#FF6584")
    with c4: stat_card("Detections", str(total_det), "total", "#FFD166")

    divider()

    # Features — compact grid
    st.markdown("""
    <div style="font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;
                color:#444460;margin-bottom:14px">Capabilities</div>
    """, unsafe_allow_html=True)

    features = [
        ("🎯", "Batch Detection", "Upload banyak gambar, proses sekaligus"),
        ("📊", "Analytics", "Radar chart, metrics, confusion matrix"),
        ("⬇️", "Export", "Download gambar + CSV hasil deteksi"),
        ("📋", "History", "Log lengkap setiap deteksi"),
        ("⚡", "Fast", "YOLOv8 nano — inference cepat"),
        ("🔧", "Configurable", "Atur threshold langsung dari UI"),
    ]

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="ak-card" style="padding:16px">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
                <span style="font-size:18px">{icon}</span>
                <span style="font-size:13px;font-weight:600;color:#E8E8F0">{title}</span>
              </div>
              <div style="font-size:12px;color:#666680;line-height:1.5">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    divider()

    # Quick start — minimal
    st.markdown("""
    <div style="font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;
                color:#444460;margin-bottom:14px">Get Started</div>
    """, unsafe_allow_html=True)

    steps = [
        ("01", "Buka halaman Detect dari sidebar"),
        ("02", "Upload satu atau beberapa gambar aksara"),
        ("03", "Lihat hasil deteksi — download jika perlu"),
    ]
    for num, text in steps:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:14px;padding:12px 16px;
                    background:#ffffff03;border:1px solid #ffffff06;border-radius:10px;
                    margin-bottom:8px">
          <span style="font-family:'JetBrains Mono',monospace;font-size:12px;
                       font-weight:600;color:#6C63FF;min-width:24px">{num}</span>
          <span style="font-size:13px;color:#C0C0D8">{text}</span>
        </div>
        """, unsafe_allow_html=True)
