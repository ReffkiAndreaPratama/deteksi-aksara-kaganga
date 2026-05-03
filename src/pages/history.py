"""pages/history.py — Riwayat semua deteksi."""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import Counter

import config, utils
from components.ui import page_header, divider, empty_state, stat_card

PALETTE = {"primary":"#6C63FF","secondary":"#3ECFCF","dark":"#1A1A2E","surface":"#16213E","text":"#E0E0E0"}


def render():
    page_header("Riwayat Deteksi", "Log semua prediksi yang pernah dilakukan")

    log = utils.load_prediction_log()
    if not log:
        empty_state("📋", "Belum ada riwayat",
                    "Lakukan deteksi di halaman Detect terlebih dahulu.")
        return

    total      = len(log)
    total_det  = sum(e.get("count", 0) for e in log)
    all_dets   = [d for e in log for d in e.get("detections", [])]
    avg_conf   = np.mean([d["confidence"] for d in all_dets]) * 100 if all_dets else 0
    classes_seen = len(set(d["class_name"] for d in all_dets))

    c1, c2, c3, c4 = st.columns(4)
    with c1: stat_card("Total Gambar",    str(total),      "diproses",         "#6C63FF")
    with c2: stat_card("Total Deteksi",   str(total_det),  "aksara ditemukan", "#3ECFCF")
    with c3: stat_card("Avg Confidence",  f"{avg_conf:.1f}%", "",              "#FF6584")
    with c4: stat_card("Kelas Unik",      str(classes_seen), "terdeteksi",     "#FFD166")

    divider()

    # ── Filter ────────────────────────────────────────────────────────────────
    sort_by = st.selectbox("Urutkan", ["Terbaru", "Terlama",
                                       "Deteksi terbanyak", "Deteksi tersedikit"])
    if sort_by == "Terbaru":
        log = sorted(log, key=lambda x: x["timestamp"], reverse=True)
    elif sort_by == "Terlama":
        log = sorted(log, key=lambda x: x["timestamp"])
    elif sort_by == "Deteksi terbanyak":
        log = sorted(log, key=lambda x: x.get("count", 0), reverse=True)
    else:
        log = sorted(log, key=lambda x: x.get("count", 0))

    st.markdown(f'<div style="font-size:13px;color:#8888AA;margin-bottom:12px">'
                f'{len(log)} records</div>', unsafe_allow_html=True)

    for entry in log[:50]:
        ts    = entry["timestamp"][11:19] if len(entry["timestamp"]) > 10 else entry["timestamp"]
        fname = entry.get("filename", "—")
        count = entry.get("count", 0)
        dets  = entry.get("detections", [])
        classes_str = ", ".join(sorted(set(d["class_name"] for d in dets)))[:60]
        if len(classes_str) == 60:
            classes_str += "..."

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;padding:12px 16px;
                    background:rgba(255,255,255,0.03);border:1px solid rgba(108,99,255,0.1);
                    border-radius:10px;margin-bottom:8px">
          <div style="font-size:11px;color:#8888AA;min-width:70px">{ts}</div>
          <div style="flex:1;font-size:13px;color:#C0C0D8;overflow:hidden;
                      text-overflow:ellipsis;white-space:nowrap" title="{fname}">{fname}</div>
          <div style="font-size:13px;font-weight:700;color:#6C63FF;min-width:30px;
                      text-align:center">{count}</div>
          <div style="font-size:12px;color:#8888AA;max-width:200px;overflow:hidden;
                      text-overflow:ellipsis;white-space:nowrap">{classes_str}</div>
        </div>
        """, unsafe_allow_html=True)

    divider()

    # ── Charts ────────────────────────────────────────────────────────────────
    if all_dets:
        c1, c2 = st.columns(2)

        with c1:
            st.markdown('<div style="font-size:12px;color:#8888AA;text-transform:uppercase;'
                        'letter-spacing:1px;margin-bottom:8px">Top 15 Aksara Terdeteksi</div>',
                        unsafe_allow_html=True)
            counts = Counter(d["class_name"] for d in all_dets).most_common(15)
            labels, values = zip(*counts)
            fig, ax = plt.subplots(figsize=(6, 5))
            fig.patch.set_facecolor(PALETTE["dark"])
            ax.set_facecolor(PALETTE["surface"])
            colors = plt.cm.cool(np.linspace(0.2, 0.8, len(labels)))
            ax.barh(list(labels)[::-1], list(values)[::-1], color=colors)
            ax.set_xlabel("Jumlah", color=PALETTE["text"])
            ax.tick_params(colors=PALETTE["text"])
            for spine in ax.spines.values():
                spine.set_edgecolor("#444466")
            ax.grid(axis="x", alpha=0.15, color="#555577")
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with c2:
            st.markdown('<div style="font-size:12px;color:#8888AA;text-transform:uppercase;'
                        'letter-spacing:1px;margin-bottom:8px">Distribusi Confidence</div>',
                        unsafe_allow_html=True)
            confs = [d["confidence"] * 100 for d in all_dets]
            fig, ax = plt.subplots(figsize=(6, 5))
            fig.patch.set_facecolor(PALETTE["dark"])
            ax.set_facecolor(PALETTE["surface"])
            ax.hist(confs, bins=20, color=PALETTE["primary"],
                    alpha=0.8, edgecolor=PALETTE["secondary"], linewidth=0.5)
            ax.axvline(np.mean(confs), color="#FF6584", linewidth=2,
                       linestyle="--", label=f"Mean: {np.mean(confs):.1f}%")
            ax.set_xlabel("Confidence (%)", color=PALETTE["text"])
            ax.set_ylabel("Count", color=PALETTE["text"])
            ax.tick_params(colors=PALETTE["text"])
            ax.legend(facecolor=PALETTE["surface"], labelcolor=PALETTE["text"], fontsize=9)
            for spine in ax.spines.values():
                spine.set_edgecolor("#444466")
            ax.grid(alpha=0.15, color="#555577")
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

    divider()

    with st.expander("📥 Export data"):
        rows = []
        for e in log:
            for d in e.get("detections", []):
                rows.append({
                    "Timestamp":  e["timestamp"],
                    "File":       e.get("filename", ""),
                    "Aksara":     d["class_name"],
                    "Confidence": f"{d['confidence']:.4f}",
                    "X1": int(d["bbox"][0]), "Y1": int(d["bbox"][1]),
                    "X2": int(d["bbox"][2]), "Y2": int(d["bbox"][3]),
                })
        if rows:
            df  = pd.DataFrame(rows)
            csv = df.to_csv(index=False).encode("utf-8")
            st.dataframe(df.head(100), use_container_width=True, hide_index=True)
            st.download_button("⬇️ Download CSV", csv,
                               "detection_history.csv", "text/csv")

    with st.expander("🗑️ Hapus riwayat"):
        st.warning("Semua log prediksi akan dihapus permanen.")
        if st.button("Hapus semua log", type="primary"):
            import json
            with open(config.PREDICT_LOG, "w") as f:
                json.dump([], f)
            st.success("Log dihapus.")
            st.rerun()
