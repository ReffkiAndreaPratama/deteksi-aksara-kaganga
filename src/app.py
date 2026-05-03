"""
app.py — Entry point GUI AksaraDetect (YOLOv8).
Jalankan: streamlit run app.py  (dari folder src/)
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

st.set_page_config(
    page_title="AksaraDetect",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.ui import inject_styles
import config, utils

# Pastikan semua folder output ada
utils.ensure_dirs()
inject_styles()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 8px 8px">
      <div style="font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:700;
                  background:linear-gradient(135deg,#6C63FF,#3ECFCF);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                  background-clip:text;margin-bottom:4px">🔍 AksaraDetect</div>
      <div style="font-size:11px;color:#8888AA;margin-bottom:20px">
        YOLOv8 · Aksara Ulu Rejang
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,'
                'rgba(108,99,255,0.4),transparent);margin-bottom:16px"></div>',
                unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["🏠  Home", "🔍  Detect", "📊  Analytics", "📋  History", "⚙️  Settings"],
        label_visibility="collapsed",
    )

    st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,'
                'rgba(108,99,255,0.4),transparent);margin:16px 0"></div>',
                unsafe_allow_html=True)

    # Status
    model_ok = os.path.isfile(config.MODEL_BEST_PATH)
    yaml_ok  = os.path.isfile(config.DATA_YAML)
    log      = utils.load_prediction_log()

    st.markdown('<div style="font-size:11px;font-weight:600;letter-spacing:1px;'
                'text-transform:uppercase;color:#8888AA;margin-bottom:10px">'
                'System Status</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="display:flex;flex-direction:column;gap:8px">
      <div style="display:flex;justify-content:space-between;align-items:center;
                  background:rgba(255,255,255,0.03);border-radius:8px;padding:8px 12px">
        <span style="font-size:12px;color:#C0C0D8">YOLOv8 Model</span>
        <span style="font-size:11px;font-weight:600;
                     color:{'#4CAF50' if model_ok else '#F44336'}">
          {'● Ready' if model_ok else '○ Not trained'}
        </span>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center;
                  background:rgba(255,255,255,0.03);border-radius:8px;padding:8px 12px">
        <span style="font-size:12px;color:#C0C0D8">Dataset</span>
        <span style="font-size:11px;font-weight:600;
                     color:{'#4CAF50' if yaml_ok else '#F44336'}">
          {'● 253 kelas' if yaml_ok else '○ Not found'}
        </span>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center;
                  background:rgba(255,255,255,0.03);border-radius:8px;padding:8px 12px">
        <span style="font-size:12px;color:#C0C0D8">Deteksi Log</span>
        <span style="font-size:11px;font-weight:600;color:#6C63FF">{len(log)}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Route ─────────────────────────────────────────────────────────────────────
if   "Home"      in page: from pages.home      import render; render()
elif "Detect"    in page: from pages.detect    import render; render()
elif "Analytics" in page: from pages.analytics import render; render()
elif "History"   in page: from pages.history   import render; render()
elif "Settings"  in page: from pages.settings  import render; render()
