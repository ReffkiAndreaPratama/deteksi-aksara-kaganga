"""
pages/predict.py — Halaman prediksi gambar.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import streamlit as st
from PIL import Image
import tensorflow as tf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import config
import utils
from components.ui import (
    page_header, divider, result_box, prob_bars, badge, empty_state
)


# ── Cache ─────────────────────────────────────────────────────────────────────

@st.cache_resource
def _load_model(model_type: str):
    path = config.MODEL_MOBILENET_PATH if model_type == "MobileNetV2" \
        else config.MODEL_CNN_PATH
    if not os.path.isfile(path):
        return None
    return tf.keras.models.load_model(path)


@st.cache_data
def _load_labels():
    if not os.path.isfile(config.LABEL_MAP_PATH):
        return None
    return utils.load_label_map()


def _preprocess_pil(pil_img: Image.Image) -> np.ndarray:
    img = pil_img.convert("RGB").resize(
        (config.IMG_SIZE, config.IMG_SIZE), Image.LANCZOS
    )
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


def _radar_chart(label_map: dict, probs: np.ndarray):
    """Buat radar/spider chart untuk distribusi probabilitas."""
    import numpy as np
    labels = [label_map[i] for i in range(len(probs))]
    values = [float(p) * 100 for p in probs]

    # Batasi ke top-8 supaya chart tidak terlalu ramai
    if len(labels) > 8:
        pairs = sorted(zip(values, labels), reverse=True)[:8]
        values, labels = zip(*pairs)
        values, labels = list(values), list(labels)

    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values_plot = values + [values[0]]
    angles      = angles + [angles[0]]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#1A1A2E")
    ax.set_facecolor("#16213E")

    ax.plot(angles, values_plot, color="#6C63FF", linewidth=2)
    ax.fill(angles, values_plot, color="#6C63FF", alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color="#C0C0D8", fontsize=9)
    ax.tick_params(colors="#8888AA")
    ax.yaxis.set_tick_params(labelcolor="#8888AA")
    ax.spines["polar"].set_color("#444466")
    ax.grid(color="#444466", alpha=0.5)
    plt.tight_layout()
    return fig


# ── Render ────────────────────────────────────────────────────────────────────

def render():
    page_header("Image Prediction",
                "Upload an image to classify it using your trained model")

    # ── Guard: model & label ──────────────────────────────────────────────────
    label_map = _load_labels()
    if label_map is None:
        st.error("**No trained model found.** Run `python train.py` first.")
        st.code("cd src\npython train.py", language="bash")
        return

    # ── Controls ──────────────────────────────────────────────────────────────
    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([2, 2, 3])
    with col_ctrl1:
        model_choice = st.selectbox(
            "Model",
            ["CNN", "MobileNetV2"],
            help="CNN is lighter; MobileNetV2 usually more accurate",
        )
    with col_ctrl2:
        top_n = st.selectbox("Show top N classes", [3, 5, 10, "All"], index=1)
        top_n = None if top_n == "All" else int(top_n)
    with col_ctrl3:
        show_radar = st.checkbox("Show radar chart", value=True)

    model = _load_model(model_choice)
    if model is None:
        st.warning(f"**{model_choice}** model not found. "
                   f"Train it first with `python train.py"
                   f"{'  --mobilenet' if model_choice=='MobileNetV2' else ''}`")
        return

    divider()

    # ── Upload ────────────────────────────────────────────────────────────────
    uploaded = st.file_uploader(
        "Drop your image here or click to browse",
        type=["jpg", "jpeg", "png", "bmp", "webp"],
        label_visibility="visible",
    )

    if uploaded is None:
        empty_state("🖼️", "No image uploaded",
                    "Supported formats: JPG, PNG, BMP, WEBP")
        return

    # ── Predict ───────────────────────────────────────────────────────────────
    pil_img = Image.open(uploaded)

    with st.spinner("Analyzing image..."):
        arr   = _preprocess_pil(pil_img)
        preds = model.predict(arr, verbose=0)[0]

    pred_idx   = int(np.argmax(preds))
    pred_class = label_map[pred_idx]
    confidence = float(preds[pred_idx]) * 100

    # Log
    utils.log_prediction(
        uploaded.name, model_choice, pred_class, confidence,
        {label_map[i]: float(preds[i]) * 100 for i in range(len(preds))}
    )

    # ── Layout ────────────────────────────────────────────────────────────────
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div style="font-size:13px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#8888AA;margin-bottom:10px">Input Image</div>', unsafe_allow_html=True)
        st.image(pil_img, use_container_width=True)
        st.markdown(f"""
        <div style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap">
          <span class="vc-badge vc-badge-primary">{pil_img.size[0]}×{pil_img.size[1]} px</span>
          <span class="vc-badge vc-badge-teal">{pil_img.mode}</span>
          <span class="vc-badge vc-badge-primary">{model_choice}</span>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown('<div style="font-size:13px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#8888AA;margin-bottom:10px">Result</div>', unsafe_allow_html=True)
        result_box(pred_class, confidence)

        st.markdown('<div style="margin-top:20px;font-size:13px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#8888AA;margin-bottom:10px">Probability Distribution</div>', unsafe_allow_html=True)
        prob_bars(label_map, preds, top_n=top_n)

    # ── Radar Chart ───────────────────────────────────────────────────────────
    if show_radar and len(label_map) >= 3:
        divider()
        st.markdown('<div style="font-size:13px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#8888AA;margin-bottom:10px">Radar Chart</div>', unsafe_allow_html=True)
        _, mid, _ = st.columns([1, 2, 1])
        with mid:
            fig = _radar_chart(label_map, preds)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

    # ── Detail Table ──────────────────────────────────────────────────────────
    divider()
    with st.expander("📋 Full probability table"):
        import pandas as pd
        rows = [
            {"Rank": i + 1,
             "Class": label_map[idx],
             "Probability": f"{float(preds[idx])*100:.4f}%",
             "Raw Score": f"{float(preds[idx]):.6f}"}
            for i, idx in enumerate(
                sorted(range(len(preds)), key=lambda x: preds[x], reverse=True)
            )
        ]
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
