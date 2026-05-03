"""pages/settings.py — Konfigurasi dan info project."""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import config, utils
from components.ui import page_header, divider


def _size(path):
    if not os.path.isfile(path): return "—"
    s = os.path.getsize(path)
    return f"{s/1024**2:.1f} MB" if s >= 1024**2 else \
           f"{s/1024:.1f} KB"   if s >= 1024    else f"{s} B"


def render():
    page_header("Settings & Info", "Konfigurasi model dan status project")

    # ── Config ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:600;
                color:#F0F0FF;margin-bottom:16px">Konfigurasi Training</div>
    """, unsafe_allow_html=True)

    items = [
        ("Model Size",    f"YOLOv8{config.MODEL_SIZE}"),
        ("Epochs",        str(config.EPOCHS)),
        ("Image Size",    f"{config.IMG_SIZE}px"),
        ("Batch Size",    str(config.BATCH_SIZE)),
        ("Patience",      str(config.PATIENCE)),
        ("Device",        config.DEVICE),
        ("Conf Threshold",str(config.CONF_THRESHOLD)),
        ("IoU Threshold", str(config.IOU_THRESHOLD)),
        ("Workers",       str(config.WORKERS)),
    ]
    cols = st.columns(3)
    for i, (label, value) in enumerate(items):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="vc-card" style="padding:14px 16px">
              <div class="vc-card-title">{label}</div>
              <div style="font-family:'Space Grotesk',sans-serif;font-size:18px;
                          font-weight:600;color:#6C63FF">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:12px;padding:12px 16px;background:rgba(108,99,255,0.08);
                border:1px solid rgba(108,99,255,0.2);border-radius:10px;
                font-size:13px;color:#8888AA">
      💡 Edit <code style="color:#6C63FF">src/config.py</code> untuk mengubah parameter.
    </div>
    """, unsafe_allow_html=True)

    divider()

    # ── File Status ───────────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:600;
                color:#F0F0FF;margin-bottom:16px">Status File</div>
    """, unsafe_allow_html=True)

    files = [
        ("Model Terbaik (best.pt)",  config.MODEL_BEST_PATH),
        ("Model Terakhir (last.pt)", config.MODEL_LAST_PATH),
        ("Label Map",                config.LABEL_MAP_PATH),
        ("Metrics",                  config.METRICS_PATH),
        ("Prediction Log",           config.PREDICT_LOG),
        ("Data YAML",                config.DATA_YAML),
    ]

    rows = ""
    for name, path in files:
        exists = os.path.isfile(path)
        dot    = "●" if exists else "○"
        color  = "#4CAF50" if exists else "#8888AA"
        size   = _size(path)
        rows  += f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
                    padding:10px 16px;border-bottom:1px solid rgba(108,99,255,0.08)">
          <div style="display:flex;align-items:center;gap:10px">
            <span style="color:{color};font-size:10px">{dot}</span>
            <span style="font-size:13px;color:#C0C0D8">{name}</span>
          </div>
          <span style="font-size:12px;color:{'#4CAF50' if exists else '#8888AA'};
                       font-weight:600">{size}</span>
        </div>"""

    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(108,99,255,0.15);
                border-radius:12px;overflow:hidden">{rows}</div>
    """, unsafe_allow_html=True)

    divider()

    # ── Dataset Info ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:600;
                color:#F0F0FF;margin-bottom:16px">Info Dataset</div>
    """, unsafe_allow_html=True)

    dataset_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "Aksara Ulu Rejang.v4-fix.yolov8"
    )

    for split in ["train", "valid", "test"]:
        img_dir = os.path.join(dataset_dir, split, "images")
        lbl_dir = os.path.join(dataset_dir, split, "labels")
        if not os.path.isdir(img_dir):
            continue
        exts  = {".jpg", ".jpeg", ".png"}
        imgs  = [f for f in os.listdir(img_dir)
                 if os.path.splitext(f)[1].lower() in exts]
        lbls  = [f for f in os.listdir(lbl_dir)
                 if f.endswith(".txt")] if os.path.isdir(lbl_dir) else []
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;padding:10px 16px;
                    background:rgba(255,255,255,0.03);border:1px solid rgba(108,99,255,0.1);
                    border-radius:10px;margin-bottom:8px">
          <span style="font-weight:600;color:#F0F0FF;text-transform:capitalize">{split}</span>
          <span style="color:#8888AA;font-size:13px">
            {len(imgs)} gambar &nbsp;·&nbsp; {len(lbls)} label
          </span>
        </div>
        """, unsafe_allow_html=True)

    divider()

    st.markdown(f"""
    <div style="text-align:center;padding:20px;color:#8888AA;font-size:13px">
      <div style="font-family:'Space Grotesk',sans-serif;font-size:16px;font-weight:600;
                  color:#C0C0D8;margin-bottom:6px">{config.APP_NAME} v{config.APP_VERSION}</div>
      {config.APP_TAGLINE}<br>Built with Ultralytics YOLOv8 · Streamlit · Python
    </div>
    """, unsafe_allow_html=True)
