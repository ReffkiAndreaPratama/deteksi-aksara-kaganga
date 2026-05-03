"""pages/analytics.py — Dashboard evaluasi YOLOv8."""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from PIL import Image

import config, utils
from components.ui import page_header, divider, stat_card, empty_state


def _img(fname):
    p = os.path.join(config.RESULT_DIR, fname)
    return Image.open(p) if os.path.isfile(p) else None


def render():
    page_header("Analytics", "Evaluasi performa model YOLOv8")

    metrics = utils.load_metrics()
    yolo_m  = metrics.get("yolov8", {})

    if not metrics:
        empty_state("📊", "Belum ada data evaluasi",
                    "Jalankan training terlebih dahulu.")
        return

    # ── Metric Cards ──────────────────────────────────────────────────────────
    map50   = yolo_m.get("metrics/mAP50(B)",    yolo_m.get("metrics/mAP50",    None))
    map5095 = yolo_m.get("metrics/mAP50-95(B)", yolo_m.get("metrics/mAP50-95", None))
    prec    = yolo_m.get("metrics/precision(B)", yolo_m.get("metrics/precision", None))
    rec     = yolo_m.get("metrics/recall(B)",    yolo_m.get("metrics/recall",    None))

    c1, c2, c3, c4 = st.columns(4)
    with c1: stat_card("mAP@50",
                       f"{map50*100:.2f}%"   if map50   else "—", "", "#6C63FF")
    with c2: stat_card("mAP@50-95",
                       f"{map5095*100:.2f}%" if map5095 else "—", "", "#3ECFCF")
    with c3: stat_card("Precision",
                       f"{prec*100:.2f}%"    if prec    else "—", "", "#FF6584")
    with c4: stat_card("Recall",
                       f"{rec*100:.2f}%"     if rec     else "—", "", "#FFD166")

    divider()

    # ── Training Curves ───────────────────────────────────────────────────────
    curves = _img("training_curves.png")
    if curves:
        st.markdown('<div style="font-size:12px;color:#8888AA;text-transform:uppercase;'
                    'letter-spacing:1px;margin-bottom:8px">Training Curves</div>',
                    unsafe_allow_html=True)
        st.image(curves, use_container_width=True)
        divider()

    # ── YOLO Charts ───────────────────────────────────────────────────────────
    chart_pairs = [
        ("PR_curve.png",  "F1_curve.png"),
        ("P_curve.png",   "R_curve.png"),
    ]
    for left_f, right_f in chart_pairs:
        li, ri = _img(left_f), _img(right_f)
        if li or ri:
            c1, c2 = st.columns(2)
            with c1:
                if li:
                    st.markdown(f'<div style="font-size:12px;color:#8888AA;'
                                f'text-transform:uppercase;letter-spacing:1px;'
                                f'margin-bottom:6px">{left_f.replace(".png","").replace("_"," ")}</div>',
                                unsafe_allow_html=True)
                    st.image(li, use_container_width=True)
            with c2:
                if ri:
                    st.markdown(f'<div style="font-size:12px;color:#8888AA;'
                                f'text-transform:uppercase;letter-spacing:1px;'
                                f'margin-bottom:6px">{right_f.replace(".png","").replace("_"," ")}</div>',
                                unsafe_allow_html=True)
                    st.image(ri, use_container_width=True)
            divider()

    # ── Confusion Matrix ──────────────────────────────────────────────────────
    cm_norm = _img("confusion_matrix_normalized.png")
    cm_raw  = _img("confusion_matrix.png")
    if cm_norm or cm_raw:
        st.markdown('<div style="font-size:12px;color:#8888AA;text-transform:uppercase;'
                    'letter-spacing:1px;margin-bottom:8px">Confusion Matrix</div>',
                    unsafe_allow_html=True)
        tabs = st.tabs(["Normalized", "Raw"])
        with tabs[0]:
            if cm_norm: st.image(cm_norm, use_container_width=True)
            else: st.info("Tidak tersedia.")
        with tabs[1]:
            if cm_raw: st.image(cm_raw, use_container_width=True)
            else: st.info("Tidak tersedia.")

    # ── Raw Metrics ───────────────────────────────────────────────────────────
    if yolo_m:
        divider()
        with st.expander("🔍 Semua metrics"):
            import pandas as pd
            df = pd.DataFrame([
                {"Metric": k, "Value": f"{v:.6f}"}
                for k, v in sorted(yolo_m.items())
            ])
            st.dataframe(df, use_container_width=True, hide_index=True)
