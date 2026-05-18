"""views/settings.py — Configuration & system info."""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import config, utils
from components.ui import page_header, divider


def _size(path):
    if not os.path.isfile(path): return "—"
    s = os.path.getsize(path)
    if s >= 1024**2: return f"{s/1024**2:.1f} MB"
    if s >= 1024: return f"{s/1024:.1f} KB"
    return f"{s} B"


def render():
    page_header("Settings", "Configuration & system info")

    # Model info
    st.markdown("""
    <div style="font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;
                color:#444460;margin-bottom:12px">Model</div>
    """, unsafe_allow_html=True)

    model_info = {"type": f"YOLOv8{config.MODEL_SIZE}", "classes": "—",
                  "size": _size(config.MODEL_BEST_PATH)}
    if os.path.isfile(config.MODEL_BEST_PATH):
        try:
            from ultralytics import YOLO
            m = YOLO(config.MODEL_BEST_PATH)
            model_info["classes"] = str(len(m.names))
        except Exception:
            pass

    c1, c2, c3 = st.columns(3)
    for col, (k, v) in zip([c1, c2, c3], model_info.items()):
        with col:
            st.markdown(f"""
            <div class="ak-card" style="text-align:center;padding:16px">
              <div style="font-size:10px;color:#555570;text-transform:uppercase;
                          letter-spacing:1px;margin-bottom:6px">{k}</div>
              <div style="font-family:'Space Grotesk',sans-serif;font-size:20px;
                          font-weight:700;color:#6C63FF">{v}</div>
            </div>
            """, unsafe_allow_html=True)

    divider()

    # Training config
    st.markdown("""
    <div style="font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;
                color:#444460;margin-bottom:12px">Training Config</div>
    """, unsafe_allow_html=True)

    params = [
        ("Epochs", config.EPOCHS), ("Image Size", f"{config.IMG_SIZE}px"),
        ("Batch Size", config.BATCH_SIZE), ("Patience", config.PATIENCE),
        ("Learning Rate", config.LR0), ("Device", config.DEVICE),
        ("Conf Threshold", config.CONF_THRESHOLD), ("IoU Threshold", config.IOU_THRESHOLD),
        ("Workers", config.WORKERS),
    ]

    cols = st.columns(3)
    for i, (label, value) in enumerate(params):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="padding:10px 14px;background:#ffffff03;border:1px solid #ffffff06;
                        border-radius:8px;margin-bottom:6px;
                        display:flex;justify-content:space-between;align-items:center">
              <span style="font-size:12px;color:#8888AA">{label}</span>
              <span style="font-family:'JetBrains Mono',monospace;font-size:12px;
                           color:#E8E8F0;font-weight:500">{value}</span>
            </div>
            """, unsafe_allow_html=True)

    divider()

    # File status
    st.markdown("""
    <div style="font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;
                color:#444460;margin-bottom:12px">Files</div>
    """, unsafe_allow_html=True)

    files = [
        ("best.pt", config.MODEL_BEST_PATH),
        ("last.pt", config.MODEL_LAST_PATH),
        ("label_map.json", config.LABEL_MAP_PATH),
        ("metrics.json", config.METRICS_PATH),
        ("prediction_log.json", config.PREDICT_LOG),
        ("data.yaml", config.DATA_YAML),
    ]

    for name, path in files:
        exists = os.path.isfile(path)
        size = _size(path)
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
                    padding:8px 14px;border-bottom:1px solid #ffffff05">
          <div style="display:flex;align-items:center;gap:8px">
            <span style="width:6px;height:6px;border-radius:50%;
                         background:{'#4CAF50' if exists else '#333340'}"></span>
            <span style="font-size:12px;color:#{'C0C0D8' if exists else '555570'}">{name}</span>
          </div>
          <span style="font-family:'JetBrains Mono',monospace;font-size:11px;
                       color:#555570">{size}</span>
        </div>
        """, unsafe_allow_html=True)

    divider()

    # Class list
    if os.path.isfile(config.MODEL_BEST_PATH):
        with st.expander("All classes"):
            try:
                from ultralytics import YOLO
                m = YOLO(config.MODEL_BEST_PATH)
                names = m.names
                # Render as compact grid
                html = '<div style="display:flex;flex-wrap:wrap;gap:4px">'
                for idx, name in sorted(names.items()):
                    html += f"""<span style="padding:3px 8px;background:#ffffff04;
                                border:1px solid #ffffff08;border-radius:4px;
                                font-size:11px;color:#8888AA">
                                <span style="color:#6C63FF;font-weight:600">{idx}</span> {name}</span>"""
                html += '</div>'
                st.markdown(html, unsafe_allow_html=True)
            except Exception as e:
                st.error(str(e))

    # Footer
    st.markdown(f"""
    <div style="text-align:center;padding:24px 0 0;font-size:11px;color:#333340">
      {config.APP_NAME} v{config.APP_VERSION} · {config.APP_TAGLINE}
    </div>
    """, unsafe_allow_html=True)
