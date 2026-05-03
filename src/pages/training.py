"""
pages/training.py — Halaman training monitor & history.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import config
import utils
from components.ui import page_header, divider, stat_card, empty_state, badge


PALETTE = {
    "primary":   "#6C63FF",
    "secondary": "#3ECFCF",
    "accent":    "#FF6584",
    "dark":      "#1A1A2E",
    "surface":   "#16213E",
    "text":      "#E0E0E0",
}


def _plot_interactive(hist: dict, prefix: str):
    """Render training curves dengan matplotlib dark theme."""
    epochs = range(1, len(hist["accuracy"]) + 1)

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
    fig.patch.set_facecolor(PALETTE["dark"])

    for ax, (train_key, val_key, title) in zip(
        axes,
        [("accuracy", "val_accuracy", "Accuracy"),
         ("loss",     "val_loss",     "Loss")]
    ):
        ax.set_facecolor(PALETTE["surface"])
        ax.plot(epochs, hist[train_key], color=PALETTE["primary"],
                linewidth=2.5, label=f"Train", marker="o", markersize=3)
        ax.plot(epochs, hist[val_key], color=PALETTE["secondary"],
                linewidth=2.5, label=f"Validation", marker="s", markersize=3,
                linestyle="--")

        # Best epoch marker
        if title == "Accuracy":
            best_ep = int(np.argmax(hist[val_key])) + 1
            best_val = max(hist[val_key])
        else:
            best_ep = int(np.argmin(hist[val_key])) + 1
            best_val = min(hist[val_key])

        ax.axvline(best_ep, color=PALETTE["accent"], linewidth=1,
                   linestyle=":", alpha=0.7)
        ax.scatter([best_ep], [best_val], color=PALETTE["accent"],
                   s=80, zorder=5, label=f"Best (ep {best_ep})")

        ax.set_title(f"[{prefix.upper()}] {title}", color=PALETTE["text"],
                     fontsize=13, pad=10)
        ax.set_xlabel("Epoch", color=PALETTE["text"], fontsize=10)
        ax.set_ylabel(title, color=PALETTE["text"], fontsize=10)
        ax.tick_params(colors=PALETTE["text"])
        ax.legend(facecolor=PALETTE["surface"], labelcolor=PALETTE["text"],
                  framealpha=0.8, fontsize=9)
        ax.grid(True, alpha=0.15, color="#555577")
        for spine in ax.spines.values():
            spine.set_edgecolor("#444466")

    plt.tight_layout(pad=2)
    return fig


def render():
    page_header("Training Monitor",
                "Inspect training history and model performance over epochs")

    cnn_hist_exists = os.path.isfile(config.TRAIN_HISTORY_CNN)
    mob_hist_exists = os.path.isfile(config.TRAIN_HISTORY_MOB)

    if not cnn_hist_exists and not mob_hist_exists:
        empty_state("📈", "No training history found",
                    "Run `python train.py` to start training and generate history.")
        st.code("cd src\npython train.py\n# or with MobileNetV2:\npython train.py --mobilenet",
                language="bash")
        return

    # ── Dataset Info ──────────────────────────────────────────────────────────
    label_map = utils.load_label_map() if os.path.isfile(config.LABEL_MAP_PATH) else {}
    metrics   = utils.load_metrics()

    if label_map:
        st.markdown(f"""
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px">
          <div class="vc-card" style="flex:1;min-width:140px;padding:16px">
            <div class="vc-card-title">Classes</div>
            <div class="vc-card-value" style="font-size:28px;color:#6C63FF">{len(label_map)}</div>
          </div>
          <div class="vc-card" style="flex:1;min-width:140px;padding:16px">
            <div class="vc-card-title">Image Size</div>
            <div class="vc-card-value" style="font-size:28px;color:#3ECFCF">{config.IMG_SIZE}px</div>
          </div>
          <div class="vc-card" style="flex:1;min-width:140px;padding:16px">
            <div class="vc-card-title">Batch Size</div>
            <div class="vc-card-value" style="font-size:28px;color:#FF6584">{config.BATCH_SIZE}</div>
          </div>
          <div class="vc-card" style="flex:1;min-width:140px;padding:16px">
            <div class="vc-card-title">Max Epochs</div>
            <div class="vc-card-value" style="font-size:28px;color:#FFD166">{config.EPOCHS}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    divider()

    # ── CNN History ───────────────────────────────────────────────────────────
    if cnn_hist_exists:
        cnn_hist = utils.load_history(config.TRAIN_HISTORY_CNN)
        actual_epochs = len(cnn_hist["accuracy"])
        best_val_acc  = max(cnn_hist["val_accuracy"])
        best_ep       = cnn_hist["val_accuracy"].index(best_val_acc) + 1

        st.markdown("""
        <div style="font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:600;
                    color:#F0F0FF;margin-bottom:16px">
          CNN Training History
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            stat_card("Epochs Run", str(actual_epochs), f"of {config.EPOCHS} max", "#6C63FF")
        with m2:
            stat_card("Best Val Acc", f"{best_val_acc*100:.2f}%", f"at epoch {best_ep}", "#3ECFCF")
        with m3:
            final_train = cnn_hist["accuracy"][-1]
            stat_card("Final Train Acc", f"{final_train*100:.2f}%", "last epoch", "#FF6584")
        with m4:
            cnn_test = metrics.get("cnn", {}).get("accuracy")
            stat_card("Test Accuracy",
                      f"{cnn_test*100:.2f}%" if cnn_test else "—",
                      "on test set", "#FFD166")

        fig = _plot_interactive(cnn_hist, "cnn")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        # Epoch table
        with st.expander("📋 Epoch-by-epoch data"):
            import pandas as pd
            df = pd.DataFrame({
                "Epoch":        list(range(1, actual_epochs + 1)),
                "Train Acc":    [f"{v*100:.2f}%" for v in cnn_hist["accuracy"]],
                "Val Acc":      [f"{v*100:.2f}%" for v in cnn_hist["val_accuracy"]],
                "Train Loss":   [f"{v:.4f}" for v in cnn_hist["loss"]],
                "Val Loss":     [f"{v:.4f}" for v in cnn_hist["val_loss"]],
            })
            st.dataframe(df, use_container_width=True, hide_index=True)

    # ── MobileNetV2 History ───────────────────────────────────────────────────
    if mob_hist_exists:
        divider()
        mob_hist = utils.load_history(config.TRAIN_HISTORY_MOB)
        actual_epochs = len(mob_hist["accuracy"])
        best_val_acc  = max(mob_hist["val_accuracy"])
        best_ep       = mob_hist["val_accuracy"].index(best_val_acc) + 1

        st.markdown("""
        <div style="font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:600;
                    color:#F0F0FF;margin-bottom:16px">
          MobileNetV2 Training History
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            stat_card("Epochs Run", str(actual_epochs), f"of {config.EPOCHS} max", "#6C63FF")
        with m2:
            stat_card("Best Val Acc", f"{best_val_acc*100:.2f}%", f"at epoch {best_ep}", "#3ECFCF")
        with m3:
            final_train = mob_hist["accuracy"][-1]
            stat_card("Final Train Acc", f"{final_train*100:.2f}%", "last epoch", "#FF6584")
        with m4:
            mob_test = metrics.get("mobilenet", {}).get("accuracy")
            stat_card("Test Accuracy",
                      f"{mob_test*100:.2f}%" if mob_test else "—",
                      "on test set", "#FFD166")

        fig = _plot_interactive(mob_hist, "mobilenet")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        with st.expander("📋 Epoch-by-epoch data"):
            import pandas as pd
            df = pd.DataFrame({
                "Epoch":        list(range(1, actual_epochs + 1)),
                "Train Acc":    [f"{v*100:.2f}%" for v in mob_hist["accuracy"]],
                "Val Acc":      [f"{v*100:.2f}%" for v in mob_hist["val_accuracy"]],
                "Train Loss":   [f"{v:.4f}" for v in mob_hist["loss"]],
                "Val Loss":     [f"{v:.4f}" for v in mob_hist["val_loss"]],
            })
            st.dataframe(df, use_container_width=True, hide_index=True)
