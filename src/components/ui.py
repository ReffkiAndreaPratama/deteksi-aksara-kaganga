"""
components/ui.py — Komponen UI reusable untuk semua halaman.
"""

import os
import sys
import base64
from pathlib import Path

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


# ── CSS Loader ────────────────────────────────────────────────────────────────

def load_css():
    css_path = Path(__file__).parent.parent / "styles" / "theme.css"
    if css_path.exists():
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ── Inline CSS helpers ────────────────────────────────────────────────────────

CARD_CSS = """
<style>
.vc-card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(108,99,255,0.2);
  border-radius: 14px;
  padding: 24px;
  margin-bottom: 16px;
  backdrop-filter: blur(10px);
  transition: border-color 0.3s, box-shadow 0.3s;
}
.vc-card:hover {
  border-color: rgba(108,99,255,0.5);
  box-shadow: 0 0 24px rgba(108,99,255,0.15);
}
.vc-card-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: #8888AA;
  margin-bottom: 8px;
}
.vc-card-value {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 32px;
  font-weight: 700;
  color: #F0F0FF;
  line-height: 1.1;
}
.vc-card-sub {
  font-size: 13px;
  color: #8888AA;
  margin-top: 4px;
}
.vc-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.3px;
}
.vc-badge-primary  { background: rgba(108,99,255,0.2); color: #6C63FF; border: 1px solid rgba(108,99,255,0.4); }
.vc-badge-success  { background: rgba(76,175,80,0.2);  color: #4CAF50; border: 1px solid rgba(76,175,80,0.4); }
.vc-badge-warning  { background: rgba(255,152,0,0.2);  color: #FF9800; border: 1px solid rgba(255,152,0,0.4); }
.vc-badge-danger   { background: rgba(244,67,54,0.2);  color: #F44336; border: 1px solid rgba(244,67,54,0.4); }
.vc-badge-teal     { background: rgba(62,207,207,0.2); color: #3ECFCF; border: 1px solid rgba(62,207,207,0.4); }
.vc-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(108,99,255,0.4), transparent);
  margin: 20px 0;
}
.vc-result-box {
  background: linear-gradient(135deg, rgba(108,99,255,0.12), rgba(62,207,207,0.08));
  border: 1px solid rgba(108,99,255,0.3);
  border-radius: 16px;
  padding: 28px 24px;
  text-align: center;
}
.vc-result-label {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #8888AA;
  margin-bottom: 8px;
}
.vc-result-class {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 42px;
  font-weight: 700;
  background: linear-gradient(135deg, #6C63FF, #3ECFCF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.1;
  margin-bottom: 12px;
}
.vc-result-conf {
  font-size: 18px;
  color: #C0C0D8;
  font-weight: 500;
}
.vc-stat-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.vc-stat-item {
  flex: 1;
  min-width: 100px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(108,99,255,0.15);
  border-radius: 10px;
  padding: 14px 16px;
  text-align: center;
}
.vc-stat-num {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 24px;
  font-weight: 700;
  color: #6C63FF;
}
.vc-stat-lbl {
  font-size: 11px;
  color: #8888AA;
  margin-top: 2px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}
.vc-header-bar {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 24px;
  background: rgba(255,255,255,0.03);
  border-bottom: 1px solid rgba(108,99,255,0.15);
  margin-bottom: 28px;
}
.vc-logo-text {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 22px;
  font-weight: 700;
  background: linear-gradient(135deg, #6C63FF, #3ECFCF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.vc-logo-version {
  font-size: 11px;
  color: #8888AA;
  margin-top: -4px;
}
.vc-page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: #F0F0FF;
  margin-bottom: 4px;
}
.vc-page-sub {
  font-size: 14px;
  color: #8888AA;
  margin-bottom: 28px;
}
.vc-prob-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}
.vc-prob-label {
  width: 130px;
  font-size: 13px;
  font-weight: 500;
  color: #C0C0D8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.vc-prob-bar-wrap {
  flex: 1;
  height: 8px;
  background: rgba(255,255,255,0.06);
  border-radius: 4px;
  overflow: hidden;
}
.vc-prob-bar-fill {
  height: 100%;
  border-radius: 4px;
  background: linear-gradient(90deg, #6C63FF, #3ECFCF);
  transition: width 0.6s ease;
}
.vc-prob-pct {
  width: 52px;
  text-align: right;
  font-size: 13px;
  font-weight: 600;
  color: #F0F0FF;
}
.vc-history-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(108,99,255,0.1);
  border-radius: 10px;
  margin-bottom: 8px;
  transition: border-color 0.2s;
}
.vc-history-row:hover {
  border-color: rgba(108,99,255,0.35);
}
.vc-history-time {
  font-size: 11px;
  color: #8888AA;
  min-width: 80px;
}
.vc-history-file {
  flex: 1;
  font-size: 13px;
  color: #C0C0D8;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.vc-history-class {
  font-size: 13px;
  font-weight: 600;
  color: #6C63FF;
  min-width: 80px;
  text-align: right;
}
.vc-history-conf {
  font-size: 12px;
  color: #8888AA;
  min-width: 55px;
  text-align: right;
}
</style>
"""


# ── Komponen ──────────────────────────────────────────────────────────────────

def inject_styles():
    load_css()
    st.markdown(CARD_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="vc-page-title">{title}</div>
    <div class="vc-page-sub">{subtitle}</div>
    """, unsafe_allow_html=True)


def top_bar():
    st.markdown(f"""
    <div class="vc-header-bar">
      <div>
        <div class="vc-logo-text">⬡ {config.APP_NAME}</div>
        <div class="vc-logo-version">v{config.APP_VERSION} · {config.APP_TAGLINE}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def stat_card(label: str, value: str, sub: str = "", color: str = "#6C63FF"):
    st.markdown(f"""
    <div class="vc-card">
      <div class="vc-card-title">{label}</div>
      <div class="vc-card-value" style="color:{color}">{value}</div>
      <div class="vc-card-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)


def badge(text: str, kind: str = "primary"):
    return f'<span class="vc-badge vc-badge-{kind}">{text}</span>'


def divider():
    st.markdown('<div class="vc-divider"></div>', unsafe_allow_html=True)


def result_box(class_name: str, confidence: float):
    if confidence >= 80:
        conf_color = "#4CAF50"
        conf_label = "High Confidence"
    elif confidence >= 50:
        conf_color = "#FF9800"
        conf_label = "Medium Confidence"
    else:
        conf_color = "#F44336"
        conf_label = "Low Confidence"

    st.markdown(f"""
    <div class="vc-result-box">
      <div class="vc-result-label">Detected Class</div>
      <div class="vc-result-class">{class_name}</div>
      <div class="vc-result-conf">
        <span style="color:{conf_color}; font-weight:700">{confidence:.2f}%</span>
        &nbsp;·&nbsp; {conf_label}
      </div>
    </div>
    """, unsafe_allow_html=True)


def prob_bars(label_map: dict, probs, top_n: int = None):
    """Render custom probability bars."""
    pairs = sorted(
        [(label_map[i], float(probs[i]) * 100) for i in range(len(probs))],
        key=lambda x: x[1], reverse=True
    )
    if top_n:
        pairs = pairs[:top_n]

    rows = ""
    for cls, pct in pairs:
        rows += f"""
        <div class="vc-prob-row">
          <div class="vc-prob-label" title="{cls}">{cls}</div>
          <div class="vc-prob-bar-wrap">
            <div class="vc-prob-bar-fill" style="width:{pct:.1f}%"></div>
          </div>
          <div class="vc-prob-pct">{pct:.1f}%</div>
        </div>
        """
    st.markdown(f'<div style="margin-top:8px">{rows}</div>', unsafe_allow_html=True)


def history_row(ts: str, filename: str, cls: str, conf: float, model: str):
    conf_color = "#4CAF50" if conf >= 80 else "#FF9800" if conf >= 50 else "#F44336"
    short_ts = ts[11:19] if len(ts) > 10 else ts
    st.markdown(f"""
    <div class="vc-history-row">
      <div class="vc-history-time">{short_ts}</div>
      <div class="vc-history-file" title="{filename}">{filename}</div>
      <span class="vc-badge vc-badge-teal" style="font-size:11px">{model}</span>
      <div class="vc-history-class">{cls}</div>
      <div class="vc-history-conf" style="color:{conf_color}">{conf:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)


def empty_state(icon: str, title: str, desc: str):
    st.markdown(f"""
    <div style="text-align:center; padding:60px 20px; color:#8888AA;">
      <div style="font-size:52px; margin-bottom:16px">{icon}</div>
      <div style="font-size:18px; font-weight:600; color:#C0C0D8; margin-bottom:8px">{title}</div>
      <div style="font-size:14px">{desc}</div>
    </div>
    """, unsafe_allow_html=True)
