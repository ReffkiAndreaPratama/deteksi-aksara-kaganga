"""views/analytics.py — Model performance dashboard."""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import config, utils
from components.ui import page_header, divider, stat_card, empty_state, info_banner


def _img(fname):
    p = os.path.join(config.RESULT_DIR, fname)
    return Image.open(p) if os.path.isfile(p) else None


def render():
    page_header("Analytics", "Model performance & evaluation")

    metrics = utils.load_metrics()
    if not metrics:
        empty_state("📊", "No metrics yet", "Train the model first to see performance data")
        return

    yolo_m = metrics.get("yolov8", metrics)

    map50 = yolo_m.get("metrics/mAP50(B)", yolo_m.get("metrics/mAP50", None))
    map5095 = yolo_m.get("metrics/mAP50-95(B)", yolo_m.get("metrics/mAP50-95", None))
    prec = yolo_m.get("metrics/precision(B)", yolo_m.get("metrics/precision", None))
    rec = yolo_m.get("metrics/recall(B)", yolo_m.get("metrics/recall", None))

    # Metric cards
    c1, c2, c3, c4 = st.columns(4)
    with c1: stat_card("mAP@50", f"{map50*100:.1f}%" if map50 else "—", "", "#6C63FF")
    with c2: stat_card("mAP@50-95", f"{map5095*100:.1f}%" if map5095 else "—", "", "#3ECFCF")
    with c3: stat_card("Precision", f"{prec*100:.1f}%" if prec else "—", "", "#FF6584")
    with c4: stat_card("Recall", f"{rec*100:.1f}%" if rec else "—", "", "#FFD166")

    divider()

    # Tabs
    tab_overview, tab_charts, tab_data = st.tabs(["Overview", "Charts", "Data"])

    with tab_overview:
        # Radar
        if map50 and prec and rec and map5095:
            _, center, _ = st.columns([1, 2, 1])
            with center:
                fig = _radar(map50, map5095, prec, rec)
                st.pyplot(fig)
                plt.close(fig)

            # F1 score
            f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
            st.markdown(f"""
            <div style="text-align:center;margin:16px 0">
              <span style="font-size:12px;color:#666680">F1 Score: </span>
              <span style="font-family:'Space Grotesk',sans-serif;font-size:16px;
                           font-weight:700;color:#6C63FF">{f1*100:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)

        # Model info
        divider()
        pt_files = [f for f in os.listdir(config.MODEL_DIR) if f.endswith(".pt")] \
            if os.path.isdir(config.MODEL_DIR) else []
        if pt_files:
            st.markdown('<div style="font-size:10px;font-weight:600;letter-spacing:1px;'
                        'text-transform:uppercase;color:#444460;margin-bottom:10px">Models</div>',
                        unsafe_allow_html=True)
            for f in sorted(pt_files):
                path = os.path.join(config.MODEL_DIR, f)
                sz = os.path.getsize(path) / (1024*1024)
                active = f == "best.pt"
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            padding:8px 12px;background:#{'12121E' if active else '0C0C16'};
                            border:1px solid #{'6C63FF20' if active else 'ffffff06'};
                            border-radius:8px;margin-bottom:4px">
                  <span style="font-size:12px;color:#{'F5F5FF' if active else '8888AA'};
                               font-weight:{'600' if active else '400'}">{f}</span>
                  <span style="font-size:11px;color:#555570">{sz:.1f} MB</span>
                </div>
                """, unsafe_allow_html=True)

    with tab_charts:
        # Training curves
        curves = _img("training_curves.png")
        if curves:
            st.image(curves, use_column_width=True)
            divider()

        # PR / F1 / P / R curves
        pairs = [("PR_curve.png", "F1_curve.png"), ("P_curve.png", "R_curve.png")]
        has_any = False
        for lf, rf in pairs:
            li, ri = _img(lf), _img(rf)
            if li or ri:
                has_any = True
                c1, c2 = st.columns(2)
                with c1:
                    if li: st.image(li, use_column_width=True, caption=lf.replace(".png",""))
                with c2:
                    if ri: st.image(ri, use_column_width=True, caption=rf.replace(".png",""))
                st.markdown("<div style='margin:12px 0'></div>", unsafe_allow_html=True)

        # Confusion matrix
        cm = _img("confusion_matrix_normalized.png") or _img("confusion_matrix.png")
        if cm:
            st.image(cm, use_column_width=True, caption="Confusion Matrix")

        # If no image charts, generate from metrics
        if not has_any and not curves and not cm:
            if map50 and prec and rec and map5095:
                _generate_metric_charts(map50, map5095, prec, rec)
            else:
                empty_state("📈", "No charts available",
                            "Charts appear after training completes")

    with tab_data:
        import pandas as pd
        numeric = {k: v for k, v in yolo_m.items() if isinstance(v, (int, float))}
        if numeric:
            df = pd.DataFrame([
                {"Metric": k, "Value": round(v, 6), "%": f"{v*100:.2f}%"}
                for k, v in sorted(numeric.items())
            ])
            st.dataframe(df, hide_index=True)
        else:
            st.info("No numeric metrics found.")


def _radar(map50, map5095, prec, rec):
    labels = ["mAP@50", "mAP@50-95", "Precision", "Recall"]
    values = [map50*100, map5095*100, prec*100, rec*100]

    N = len(labels)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    values_p = values + [values[0]]
    angles_p = angles + [angles[0]]

    fig, ax = plt.subplots(figsize=(4.5, 4.5), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#09090F")
    ax.set_facecolor("#12121E")

    ax.plot(angles_p, values_p, color="#6C63FF", linewidth=2, marker="o", markersize=5)
    ax.fill(angles_p, values_p, color="#6C63FF", alpha=0.1)

    for a, v in zip(angles, values):
        ax.text(a, v + 7, f"{v:.0f}%", ha="center", fontsize=9,
                color="#E8E8F0", fontweight="600")

    ax.set_xticks(angles)
    ax.set_xticklabels(labels, color="#8888AA", fontsize=10)
    ax.set_ylim(0, 100)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(["25", "50", "75", "100"], color="#444460", fontsize=8)
    ax.spines["polar"].set_color("#ffffff10")
    ax.grid(color="#ffffff08")
    plt.tight_layout()
    return fig


def _generate_metric_charts(map50, map5095, prec, rec):
    """Generate visual charts from available metrics when no image files exist."""
    st.markdown('<div style="font-size:10px;font-weight:600;letter-spacing:1px;'
                'text-transform:uppercase;color:#444460;margin-bottom:12px">'
                'Performance Breakdown</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        # Bar chart of metrics
        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor("#09090F")
        ax.set_facecolor("#12121E")

        metrics_names = ["mAP@50", "mAP@50-95", "Precision", "Recall"]
        metrics_vals = [map50*100, map5095*100, prec*100, rec*100]
        colors = ["#6C63FF", "#3ECFCF", "#FF6584", "#FFD166"]

        bars = ax.bar(metrics_names, metrics_vals, color=colors, width=0.6, alpha=0.85)

        # Value labels on bars
        for bar, val in zip(bars, metrics_vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                    f"{val:.1f}%", ha="center", fontsize=9, color="#E8E8F0", fontweight="600")

        ax.set_ylim(0, max(metrics_vals) * 1.2)
        ax.set_ylabel("Score (%)", color="#666680", fontsize=9)
        ax.tick_params(colors="#8888AA", labelsize=9)
        for s in ax.spines.values(): s.set_visible(False)
        ax.grid(axis="y", alpha=0.06, color="#ffffff")
        ax.set_title("Metrics Comparison", color="#E8E8F0", fontsize=11, fontweight="600")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with c2:
        # Gauge-style chart
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0

        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor("#09090F")
        ax.set_facecolor("#09090F")

        # Donut chart showing F1 vs remaining
        sizes = [f1 * 100, 100 - f1 * 100]
        colors_d = ["#6C63FF", "#ffffff08"]
        wedges, _ = ax.pie(sizes, colors=colors_d, startangle=90,
                           wedgeprops=dict(width=0.3, edgecolor="#09090F"))

        # Center text
        ax.text(0, 0.05, f"{f1*100:.1f}%", ha="center", va="center",
                fontsize=24, fontweight="700", color="#6C63FF",
                fontfamily="Space Grotesk")
        ax.text(0, -0.15, "F1 Score", ha="center", va="center",
                fontsize=10, color="#666680")

        ax.set_title("Overall Score", color="#E8E8F0", fontsize=11,
                     fontweight="600", pad=15)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # Additional info
    divider()
    st.markdown("""
    <div class="ak-info">
      <span style="font-size:16px">💡</span>
      <span>Upload training charts (PR_curve.png, F1_curve.png, etc.) ke folder
      <code style="color:#6C63FF">results/</code> untuk visualisasi lebih lengkap</span>
    </div>
    """, unsafe_allow_html=True)
