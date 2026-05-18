"""views/history.py — Detection log & statistics."""

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


def render():
    page_header("History", "Detection log & statistics")

    log = utils.load_prediction_log()
    if not log:
        empty_state("📋", "No history yet", "Run detection first")
        return

    total = len(log)
    total_det = sum(e.get("count", 0) for e in log)
    all_dets = [d for e in log for d in e.get("detections", [])]
    avg_conf = np.mean([d["confidence"] for d in all_dets]) * 100 if all_dets else 0
    unique_cls = len(set(d["class_name"] for d in all_dets))

    c1, c2, c3, c4 = st.columns(4)
    with c1: stat_card("Images", str(total), "processed", "#6C63FF")
    with c2: stat_card("Detections", str(total_det), "total", "#3ECFCF")
    with c3: stat_card("Avg Conf", f"{avg_conf:.0f}%", "", "#FF6584")
    with c4: stat_card("Classes", str(unique_cls), "unique", "#FFD166")

    divider()

    # Tabs
    tab_log, tab_stats, tab_export = st.tabs(["Log", "Statistics", "Export"])

    with tab_log:
        # Sort
        sort = st.selectbox("Sort", ["Newest", "Oldest", "Most detections"],
                            label_visibility="collapsed")
        if sort == "Newest":
            log_s = sorted(log, key=lambda x: x["timestamp"], reverse=True)
        elif sort == "Oldest":
            log_s = sorted(log, key=lambda x: x["timestamp"])
        else:
            log_s = sorted(log, key=lambda x: x.get("count", 0), reverse=True)

        for entry in log_s[:60]:
            ts = entry["timestamp"]
            date_str = ts[:10] if len(ts) > 10 else ""
            time_str = ts[11:19] if len(ts) > 10 else ts
            fname = entry.get("filename", "—")
            count = entry.get("count", 0)
            dets = entry.get("detections", [])
            top_cls = sorted(set(d["class_name"] for d in dets))[:3]
            cls_str = ", ".join(top_cls)

            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:10px 14px;
                        background:#ffffff03;border:1px solid #ffffff06;
                        border-radius:8px;margin-bottom:4px">
              <div style="min-width:70px">
                <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
                            color:#6C63FF">{date_str}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
                            color:#555570">{time_str}</div>
              </div>
              <div style="flex:1;font-size:12px;color:#C0C0D8;overflow:hidden;
                          text-overflow:ellipsis;white-space:nowrap">{fname}</div>
              <div style="font-family:'Space Grotesk',sans-serif;font-size:14px;
                          font-weight:700;color:#6C63FF;min-width:24px;text-align:center">{count}</div>
              <div style="font-size:11px;color:#555570;max-width:150px;overflow:hidden;
                          text-overflow:ellipsis;white-space:nowrap">{cls_str}</div>
            </div>
            """, unsafe_allow_html=True)

    with tab_stats:
        if all_dets:
            c1, c2 = st.columns(2)

            with c1:
                st.markdown('<div style="font-size:10px;font-weight:600;letter-spacing:1px;'
                            'text-transform:uppercase;color:#444460;margin-bottom:8px">'
                            'Top Classes</div>', unsafe_allow_html=True)
                counts = Counter(d["class_name"] for d in all_dets).most_common(12)
                labels, values = zip(*counts)
                fig, ax = plt.subplots(figsize=(5, 4))
                fig.patch.set_facecolor("#09090F")
                ax.set_facecolor("#12121E")
                bars = ax.barh(list(labels)[::-1], list(values)[::-1],
                               color="#6C63FF", alpha=0.8, height=0.6)
                ax.set_xlabel("Count", color="#666680", fontsize=9)
                ax.tick_params(colors="#8888AA", labelsize=9)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.grid(axis="x", alpha=0.08, color="#ffffff")
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

            with c2:
                st.markdown('<div style="font-size:10px;font-weight:600;letter-spacing:1px;'
                            'text-transform:uppercase;color:#444460;margin-bottom:8px">'
                            'Confidence Distribution</div>', unsafe_allow_html=True)
                confs = [d["confidence"] * 100 for d in all_dets]
                fig, ax = plt.subplots(figsize=(5, 4))
                fig.patch.set_facecolor("#09090F")
                ax.set_facecolor("#12121E")
                ax.hist(confs, bins=20, color="#3ECFCF", alpha=0.7, edgecolor="#09090F")
                ax.axvline(np.mean(confs), color="#FF6584", linewidth=1.5,
                           linestyle="--", label=f"Mean: {np.mean(confs):.0f}%")
                ax.set_xlabel("Confidence %", color="#666680", fontsize=9)
                ax.tick_params(colors="#8888AA", labelsize=9)
                ax.legend(facecolor="#12121E", labelcolor="#8888AA", fontsize=8)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.grid(alpha=0.08, color="#ffffff")
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
        else:
            st.info("No detection data for statistics.")

    with tab_export:
        rows = []
        for e in log:
            for d in e.get("detections", []):
                rows.append({
                    "Timestamp": e["timestamp"], "File": e.get("filename", ""),
                    "Class": d["class_name"], "Confidence": round(d["confidence"], 4),
                    "X1": int(d["bbox"][0]), "Y1": int(d["bbox"][1]),
                    "X2": int(d["bbox"][2]), "Y2": int(d["bbox"][3]),
                })
        if rows:
            df = pd.DataFrame(rows)
            st.markdown(f"**{len(rows)}** detection records from **{total}** images")
            st.dataframe(df.head(200), hide_index=True)
            st.download_button("⬇ Download CSV", df.to_csv(index=False).encode(),
                               "history.csv", "text/csv")
        else:
            st.info("No data to export.")

        divider()
        st.markdown("**Danger zone**")
        if st.button("🗑 Clear all history", type="secondary"):
            import json
            with open(config.PREDICT_LOG, "w") as f:
                json.dump([], f)
            st.success("History cleared.")
            st.rerun()
