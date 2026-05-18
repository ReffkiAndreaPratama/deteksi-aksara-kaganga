"""
components/ui.py — Minimal, clean UI components.
"""

import os, sys
from pathlib import Path
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def load_css():
    css_path = Path(__file__).parent.parent / "styles" / "theme.css"
    if css_path.exists():
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


COMPONENT_CSS = """
<style>
/* ── Cards ── */
.ak-card {
  background: #12121E;
  border: 1px solid #ffffff0A;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 12px;
  transition: border-color 0.2s, transform 0.2s;
}
.ak-card:hover {
  border-color: #ffffff15;
  transform: translateY(-1px);
}

/* ── Stat ── */
.ak-stat {
  background: #12121E;
  border: 1px solid #ffffff08;
  border-radius: 12px;
  padding: 18px 16px;
  text-align: center;
}
.ak-stat-label {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: #666680;
  margin-bottom: 8px;
}
.ak-stat-value {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 26px;
  font-weight: 700;
  line-height: 1;
}
.ak-stat-sub {
  font-size: 11px;
  color: #555570;
  margin-top: 6px;
}

/* ── Divider ── */
.ak-divider {
  height: 1px;
  background: #ffffff08;
  margin: 24px 0;
}

/* ── Page Header ── */
.ak-header {
  margin-bottom: 28px;
}
.ak-header-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: #F5F5FF;
  margin-bottom: 4px;
  letter-spacing: -0.5px;
}
.ak-header-sub {
  font-size: 14px;
  color: #666680;
}

/* ── Empty ── */
.ak-empty {
  text-align: center;
  padding: 48px 20px;
  border: 1px dashed #ffffff10;
  border-radius: 16px;
  margin: 16px 0;
}
.ak-empty-icon { font-size: 40px; margin-bottom: 12px; opacity: 0.6; }
.ak-empty-title {
  font-size: 16px;
  font-weight: 600;
  color: #C0C0D8;
  margin-bottom: 6px;
}
.ak-empty-desc { font-size: 13px; color: #666680; }

/* ── Badge ── */
.ak-badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
}
.ak-badge-purple { background: #6C63FF15; color: #6C63FF; }
.ak-badge-teal { background: #3ECFCF15; color: #3ECFCF; }
.ak-badge-pink { background: #FF658415; color: #FF6584; }
.ak-badge-green { background: #4CAF5015; color: #4CAF50; }
.ak-badge-orange { background: #FF980015; color: #FF9800; }

/* ── Info ── */
.ak-info {
  padding: 12px 16px;
  background: #6C63FF08;
  border: 1px solid #6C63FF15;
  border-radius: 10px;
  font-size: 13px;
  color: #9090AA;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 8px 0;
}

/* ── Detection Item ── */
.ak-det-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #ffffff03;
  border: 1px solid #ffffff06;
  border-radius: 8px;
  margin-bottom: 4px;
  transition: background 0.15s;
}
.ak-det-item:hover { background: #ffffff06; }

/* ── Mono text ── */
.ak-mono {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
}
</style>
"""


def inject_styles():
    load_css()
    st.markdown(COMPONENT_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="ak-header">
      <div class="ak-header-title">{title}</div>
      <div class="ak-header-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def stat_card(label: str, value: str, sub: str = "", color: str = "#6C63FF"):
    st.markdown(f"""
    <div class="ak-stat">
      <div class="ak-stat-label">{label}</div>
      <div class="ak-stat-value" style="color:{color}">{value}</div>
      <div class="ak-stat-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)


def divider():
    st.markdown('<div class="ak-divider"></div>', unsafe_allow_html=True)


def empty_state(icon: str, title: str, desc: str):
    st.markdown(f"""
    <div class="ak-empty">
      <div class="ak-empty-icon">{icon}</div>
      <div class="ak-empty-title">{title}</div>
      <div class="ak-empty-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


def info_banner(text: str, icon: str = "💡"):
    st.markdown(f"""
    <div class="ak-info">
      <span style="font-size:16px">{icon}</span>
      <span>{text}</span>
    </div>
    """, unsafe_allow_html=True)


def metric_row(items: list):
    """items = [(label, value, color), ...]"""
    html = ""
    for label, value, color in items:
        html += f"""
        <div style="flex:1;min-width:100px;text-align:center;padding:12px;
                    background:#12121E;border-radius:10px;border:1px solid #ffffff08">
          <div style="font-size:10px;color:#666680;text-transform:uppercase;
                      letter-spacing:1px;margin-bottom:4px">{label}</div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:18px;
                      font-weight:700;color:{color}">{value}</div>
        </div>
        """
    st.markdown(f'<div style="display:flex;gap:8px;flex-wrap:wrap">{html}</div>',
                unsafe_allow_html=True)
