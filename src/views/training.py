"""views/training.py — Training results viewer."""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import config, utils
from components.ui import page_header, divider, stat_card, empty_state


def render():
    page_header("Training", "Training results & curves")

    # Find results.csv
    csv_path = os.path.join(config.RESULT_DIR, "results.csv")
    alt_path = os.path.join(config.RUNS_DIR, "aksara_ulu", "results.csv")
    if not os.path.isfile(csv_path) and os.path.isfile(alt_path):
        csv_path = alt_path

    if not os.path.isfile(csv_path):
        empty_state("📈", "No training data", "Upload results.csv from your Colab training")

        divider()
        uploaded = st.file_uploader("Upload results.csv", type=["csv"], key="upload_csv")
        if uploaded:
            os.makedirs(config.RESULT_DIR, exist_ok=True)
            save_to = os.path.join(config.RESULT_DIR, "results.csv")
            with open(save_to, "wb") as f:
                f.write(uploaded.getvalue())
            st.success("Saved! Refreshing...")
            st.rerun()
        return

    # Load
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    epochs = len(df)

    metrics = utils.load_metrics()
    yolo_m = metrics.get("yolov8", metrics)
    map50 = yolo_m.get("metrics/mAP50(B)", yolo_m.get("metrics/mAP50", None))

    # Stats
    c1, c2, c3 = st.columns(3)
    with c1: stat_card("Epochs", str(epochs), "completed", "#6C63FF")
    with c2: stat_card("Model", f"YOLOv8{config.MODEL_SIZE}", "", "#3ECFCF")
    with c3: stat_card("Best mAP", f"{map50*100:.1f}%" if map50 else "—", "", "#FF6584")

    divider()

    # Curves
    loss_cols = [c for c in df.columns if "loss" in c.lower()]
    metric_cols = [c for c in df.columns if "map" in c.lower()
                   or "precision" in c.lower() or "recall" in c.lower()]

    if loss_cols or metric_cols:
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
        fig.patch.set_facecolor("#09090F")

        # Loss
        ax = axes[0]
        ax.set_facecolor("#12121E")
        colors = ["#6C63FF", "#3ECFCF", "#FF6584", "#FFD166", "#06D6A0"]
        for i, col in enumerate(loss_cols[:5]):
            ax.plot(df.index + 1, df[col], linewidth=1.5,
                    color=colors[i % len(colors)], alpha=0.9,
                    label=col.split("/")[-1] if "/" in col else col)
        ax.set_title("Loss", color="#E8E8F0", fontsize=12, fontweight="600")
        ax.set_xlabel("Epoch", color="#666680", fontsize=9)
        ax.legend(facecolor="#12121E", labelcolor="#8888AA", fontsize=8, framealpha=0.8)
        ax.tick_params(colors="#555570", labelsize=8)
        for s in ax.spines.values(): s.set_visible(False)
        ax.grid(alpha=0.06, color="#ffffff")

        # Metrics
        ax = axes[1]
        ax.set_facecolor("#12121E")
        for i, col in enumerate(metric_cols[:5]):
            ax.plot(df.index + 1, df[col], linewidth=1.5,
                    color=colors[i % len(colors)], alpha=0.9,
                    label=col.split("/")[-1] if "/" in col else col)
        ax.set_title("Metrics", color="#E8E8F0", fontsize=12, fontweight="600")
        ax.set_xlabel("Epoch", color="#666680", fontsize=9)
        ax.legend(facecolor="#12121E", labelcolor="#8888AA", fontsize=8, framealpha=0.8)
        ax.tick_params(colors="#555570", labelsize=8)
        for s in ax.spines.values(): s.set_visible(False)
        ax.grid(alpha=0.06, color="#ffffff")

        plt.tight_layout(pad=2)
        st.pyplot(fig)
        plt.close(fig)

    divider()

    # Config
    st.markdown(f"""
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <span class="ak-badge ak-badge-purple">img {config.IMG_SIZE}px</span>
      <span class="ak-badge ak-badge-teal">batch {config.BATCH_SIZE}</span>
      <span class="ak-badge ak-badge-pink">patience {config.PATIENCE}</span>
      <span class="ak-badge ak-badge-orange">lr {config.LR0}</span>
    </div>
    """, unsafe_allow_html=True)

    # Table
    with st.expander(f"📋 All epochs ({epochs} rows)"):
        st.dataframe(df, hide_index=True)
