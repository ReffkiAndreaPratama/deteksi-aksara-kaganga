"""pages/detect.py — Halaman deteksi aksara dengan bounding box."""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import streamlit as st
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import config, utils
from components.ui import page_header, divider, empty_state, badge


@st.cache_resource
def _load_model():
    if not os.path.isfile(config.MODEL_BEST_PATH):
        return None
    try:
        from ultralytics import YOLO
        return YOLO(config.MODEL_BEST_PATH)
    except Exception:
        return None


@st.cache_data
def _load_labels():
    if os.path.isfile(config.LABEL_MAP_PATH):
        return utils.load_label_map()
    if os.path.isfile(config.DATA_YAML):
        return utils.load_label_map_from_yaml()
    return None


def _draw_boxes(pil_img: Image.Image, detections: list) -> Image.Image:
    """Gambar bounding box di atas gambar, kembalikan PIL Image."""
    colors = ["#6C63FF","#3ECFCF","#FF6584","#FFD166",
              "#06D6A0","#EF476F","#118AB2","#F77F00"]

    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor("#1A1A2E")
    ax.set_facecolor("#1A1A2E")
    ax.imshow(pil_img)

    for i, det in enumerate(detections):
        x1, y1, x2, y2 = det["bbox"]
        color = colors[i % len(colors)]
        rect  = patches.Rectangle(
            (x1, y1), x2 - x1, y2 - y1,
            linewidth=2.5, edgecolor=color, facecolor="none"
        )
        ax.add_patch(rect)
        label = f"{det['class_name']}  {det['confidence']:.0%}"
        ax.text(x1, max(y1 - 8, 0), label,
                color="white", fontsize=9, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.25",
                          facecolor=color, alpha=0.85, edgecolor="none"))

    ax.axis("off")
    plt.tight_layout(pad=0)
    fig.canvas.draw()
    w, h = fig.canvas.get_width_height()
    buf = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8).reshape(h, w, 3)
    plt.close(fig)
    return Image.fromarray(buf)


def render():
    page_header("Deteksi Aksara",
                "Upload gambar untuk mendeteksi aksara Ulu Rejang secara otomatis")

    label_map = _load_labels()
    model     = _load_model()

    if model is None:
        st.error("**Model belum ditemukan.** Jalankan training terlebih dahulu.")
        st.code("cd src\npython train.py", language="bash")
        return

    # ── Controls ──────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns([2, 2, 2])
    with c1:
        conf = st.slider("Confidence threshold", 0.1, 0.9,
                         config.CONF_THRESHOLD, 0.05)
    with c2:
        iou = st.slider("IoU threshold", 0.1, 0.9,
                        config.IOU_THRESHOLD, 0.05)
    with c3:
        max_det = st.number_input("Max deteksi", 1, 300, 100)

    st.success(f"✅ Model siap — {len(label_map) if label_map else 253} kelas")
    divider()

    # ── Upload ────────────────────────────────────────────────────────────────
    uploaded = st.file_uploader(
        "Upload gambar aksara",
        type=["jpg", "jpeg", "png", "bmp", "webp"],
    )

    if uploaded is None:
        empty_state("🖼️", "Belum ada gambar",
                    "Upload gambar yang mengandung aksara Ulu Rejang")
        return

    pil_img = Image.open(uploaded).convert("RGB")

    # ── Prediksi ──────────────────────────────────────────────────────────────
    with st.spinner("Mendeteksi aksara..."):
        results = model.predict(
            source  = pil_img,
            conf    = conf,
            iou     = iou,
            max_det = max_det,
            verbose = False,
        )

    detections = []
    if results and results[0].boxes is not None:
        boxes = results[0].boxes
        names = results[0].names
        for box in boxes:
            cls_id = int(box.cls[0])
            detections.append({
                "class_name": names[cls_id],
                "confidence": float(box.conf[0]),
                "bbox":       [float(x) for x in box.xyxy[0].tolist()],
            })

    # Log
    utils.log_prediction(uploaded.name, detections)

    # ── Tampilkan hasil ───────────────────────────────────────────────────────
    left, right = st.columns([3, 2], gap="large")

    with left:
        st.markdown('<div style="font-size:12px;color:#8888AA;text-transform:uppercase;'
                    'letter-spacing:1px;margin-bottom:8px">Hasil Deteksi</div>',
                    unsafe_allow_html=True)
        if detections:
            result_img = _draw_boxes(pil_img, detections)
            st.image(result_img, use_container_width=True)
        else:
            st.image(pil_img, use_container_width=True)
            st.warning("Tidak ada aksara terdeteksi. Coba turunkan confidence threshold.")

    with right:
        st.markdown(f"""
        <div style="background:rgba(108,99,255,0.1);border:1px solid rgba(108,99,255,0.3);
                    border-radius:14px;padding:20px;margin-bottom:16px;text-align:center">
          <div style="font-size:12px;color:#8888AA;text-transform:uppercase;
                      letter-spacing:1px;margin-bottom:8px">Aksara Terdeteksi</div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:52px;
                      font-weight:700;color:#6C63FF;line-height:1">{len(detections)}</div>
          <div style="font-size:13px;color:#8888AA;margin-top:4px">objek ditemukan</div>
        </div>
        """, unsafe_allow_html=True)

        if detections:
            st.markdown('<div style="font-size:12px;color:#8888AA;text-transform:uppercase;'
                        'letter-spacing:1px;margin-bottom:10px">Daftar Deteksi</div>',
                        unsafe_allow_html=True)

            # Sort by confidence
            sorted_dets = sorted(detections, key=lambda x: x["confidence"], reverse=True)
            for i, det in enumerate(sorted_dets):
                conf_val = det["confidence"]
                color = "#4CAF50" if conf_val >= 0.8 else \
                        "#FF9800" if conf_val >= 0.5 else "#F44336"
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            padding:8px 12px;background:rgba(255,255,255,0.03);
                            border:1px solid rgba(108,99,255,0.1);border-radius:8px;
                            margin-bottom:6px">
                  <div style="display:flex;align-items:center;gap:8px">
                    <span style="background:#6C63FF;color:white;border-radius:50%;
                                 width:20px;height:20px;display:inline-flex;
                                 align-items:center;justify-content:center;
                                 font-size:10px;font-weight:700">{i+1}</span>
                    <span style="font-weight:600;color:#F0F0FF;font-size:14px">
                      {det['class_name']}
                    </span>
                  </div>
                  <span style="font-weight:700;color:{color};font-size:13px">
                    {conf_val:.0%}
                  </span>
                </div>
                """, unsafe_allow_html=True)

    # ── Tabel detail ──────────────────────────────────────────────────────────
    if detections:
        divider()
        with st.expander("📋 Detail lengkap semua deteksi"):
            import pandas as pd
            df = pd.DataFrame([{
                "No":         i + 1,
                "Aksara":     d["class_name"],
                "Confidence": f"{d['confidence']:.4f}",
                "X1": int(d["bbox"][0]), "Y1": int(d["bbox"][1]),
                "X2": int(d["bbox"][2]), "Y2": int(d["bbox"][3]),
                "W":  int(d["bbox"][2] - d["bbox"][0]),
                "H":  int(d["bbox"][3] - d["bbox"][1]),
            } for i, d in enumerate(
                sorted(detections, key=lambda x: x["confidence"], reverse=True)
            )])
            st.dataframe(df, use_container_width=True, hide_index=True)
