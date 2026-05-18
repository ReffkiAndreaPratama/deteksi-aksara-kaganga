"""
app.py — AksaraDetect GUI
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

st.set_page_config(
    page_title="AksaraDetect",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.ui import inject_styles
import config, utils

utils.ensure_dirs()
inject_styles()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown(f"""
    <div style="padding:20px 16px 16px">
      <div style="display:flex;align-items:center;gap:10px">
        <div style="font-size:22px">◈</div>
        <div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:16px;
                      font-weight:700;color:#F5F5FF;letter-spacing:-0.3px">AksaraDetect</div>
          <div style="font-size:10px;color:#555570;margin-top:1px">v{config.APP_VERSION}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:#ffffff08;margin:0 16px 16px"></div>',
                unsafe_allow_html=True)

    # Nav
    page = st.radio(
        "nav",
        ["🏠  Home", "🔍  Detect", "📊  Analytics", "📈  Training", "📋  History", "⚙️  Settings"],
        label_visibility="collapsed",
    )

    st.markdown('<div style="height:1px;background:#ffffff08;margin:16px 16px 14px"></div>',
                unsafe_allow_html=True)

    # Status
    model_ok = os.path.isfile(config.MODEL_BEST_PATH)
    log = utils.load_prediction_log()

    st.markdown(f"""
    <div style="margin:0 16px">
      <div style="font-size:10px;font-weight:600;letter-spacing:1.2px;
                  text-transform:uppercase;color:#444460;margin-bottom:10px">Status</div>
      <div style="display:flex;flex-direction:column;gap:6px">
        <div style="display:flex;justify-content:space-between;align-items:center;
                    padding:7px 10px;background:#ffffff04;border-radius:6px">
          <span style="font-size:12px;color:#8888AA">Model</span>
          <span style="font-size:11px;font-weight:600;
                       color:{'#4CAF50' if model_ok else '#555570'}">
            {'● loaded' if model_ok else '○ missing'}</span>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;
                    padding:7px 10px;background:#ffffff04;border-radius:6px">
          <span style="font-size:12px;color:#8888AA">Detections</span>
          <span style="font-size:11px;font-weight:600;color:#6C63FF">{len(log)}</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Route ─────────────────────────────────────────────────────────────────────
if   "Home"      in page: from views.home      import render; render()
elif "Detect"    in page: from views.detect     import render; render()
elif "Analytics" in page: from views.analytics  import render; render()
elif "Training"  in page: from views.training   import render; render()
elif "History"   in page: from views.history    import render; render()
elif "Settings"  in page: from views.settings   import render; render()
