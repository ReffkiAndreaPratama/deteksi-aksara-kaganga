"""views/detect.py — Detection page with multi-image, gallery, download."""

import os, sys, io
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import config, utils
from components.ui import page_header, divider, empty_state, info_banner


@st.cache_resource
def _load_model():
    if not os.path.isfile(config.MODEL_BEST_PATH):
        return None
    try:
        from ultralytics import YOLO
        return YOLO(config.MODEL_BEST_PATH)
    except Exception:
        return None


def _draw_boxes(pil_img: Image.Image, detections: list) -> Image.Image:
    colors = ["#6C63FF", "#3ECFCF", "#FF6584", "#FFD166",
              "#06D6A0", "#EF476F", "#118AB2", "#F77F00",
              "#9B59B6", "#1ABC9C", "#E67E22", "#2ECC71"]

    w, h = pil_img.size
    fig_w = min(12, max(8, w / 100))
    fig_h = fig_w * (h / w)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    fig.patch.set_facecolor("#09090F")
    ax.set_facecolor("#09090F")
    ax.imshow(pil_img)

    for i, det in enumerate(detections):
        x1, y1, x2, y2 = det["bbox"]
        color = colors[i % len(colors)]
        rect = patches.Rectangle(
            (x1, y1), x2 - x1, y2 - y1,
            linewidth=2, edgecolor=color, facecolor=color + "10",
        )
        ax.add_patch(rect)

        font_size = max(7, min(11, w / 80))
        label = f"{det['class_name']} {det['confidence']:.0%}"
        ax.text(x1 + 3, y1 - 4, label,
                color="white", fontsize=font_size, fontweight="bold",
                bbox=dict(boxstyle="square,pad=0.2",
                          facecolor=color, alpha=0.85, edgecolor="none"))

    ax.axis("off")
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight",
                facecolor=fig.get_facecolor(), pad_inches=0, dpi=150)
    buf.seek(0)
    result = Image.open(buf).copy()
    plt.close(fig)
    buf.close()
    return result


def _detect(model, pil_img, conf, iou, max_det):
    results = model.predict(source=pil_img, conf=conf, iou=iou,
                            max_det=max_det, verbose=False)
    detections = []
    if results and results[0].boxes is not None:
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            detections.append({
                "class_name": results[0].names[cls_id],
                "confidence": float(box.conf[0]),
                "bbox": [float(x) for x in box.xyxy[0].tolist()],
            })
    return detections


def _to_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def render():
    page_header("Detect", "Upload gambar → deteksi aksara Ulu Rejang")

    model = _load_model()
    if model is None:
        st.error("Model `best.pt` tidak ditemukan di folder `models/`")
        return

    num_classes = len(model.names) if hasattr(model, 'names') else 253

    # Controls
    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1:
            conf = st.slider("Confidence", 0.05, 0.95, config.CONF_THRESHOLD, 0.05)
        with c2:
            iou = st.slider("IoU NMS", 0.1, 0.9, config.IOU_THRESHOLD, 0.05)
        with c3:
            max_det = st.number_input("Max objects", 1, 500, 100)

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;margin:8px 0 16px">
      <span style="width:6px;height:6px;border-radius:50%;background:#4CAF50"></span>
      <span style="font-size:12px;color:#666680">Model ready · {num_classes} classes</span>
    </div>
    """, unsafe_allow_html=True)

    divider()

    # Upload
    files = st.file_uploader(
        "Upload gambar",
        type=["jpg", "jpeg", "png", "bmp", "webp"],
        accept_multiple_files=True,
    )

    if not files:
        empty_state("📷", "Drop images here", "JPG, PNG, BMP, WEBP — bisa multiple")
        return

    # Process
    results_list = []
    bar = st.progress(0)
    for i, f in enumerate(files):
        img = Image.open(f).convert("RGB")
        dets = _detect(model, img, conf, iou, max_det)
        utils.log_prediction(f.name, dets)
        results_list.append({"name": f.name, "image": img, "dets": dets})
        bar.progress((i + 1) / len(files))
    bar.empty()

    # Stats bar
    total_d = sum(len(r["dets"]) for r in results_list)
    all_conf = [d["confidence"] for r in results_list for d in r["dets"]]
    avg_c = sum(all_conf) / len(all_conf) * 100 if all_conf else 0

    st.markdown(f"""
    <div style="display:flex;gap:16px;padding:14px 0;flex-wrap:wrap">
      <div style="display:flex;align-items:center;gap:6px">
        <span style="font-family:'Space Grotesk',sans-serif;font-size:20px;
                     font-weight:700;color:#F5F5FF">{len(results_list)}</span>
        <span style="font-size:12px;color:#666680">images</span>
      </div>
      <div style="width:1px;background:#ffffff10"></div>
      <div style="display:flex;align-items:center;gap:6px">
        <span style="font-family:'Space Grotesk',sans-serif;font-size:20px;
                     font-weight:700;color:#6C63FF">{total_d}</span>
        <span style="font-size:12px;color:#666680">detections</span>
      </div>
      <div style="width:1px;background:#ffffff10"></div>
      <div style="display:flex;align-items:center;gap:6px">
        <span style="font-family:'Space Grotesk',sans-serif;font-size:20px;
                     font-weight:700;color:#3ECFCF">{avg_c:.0f}%</span>
        <span style="font-size:12px;color:#666680">avg conf</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    divider()

    # Render
    if len(results_list) == 1:
        _single_view(results_list[0])
    else:
        _gallery_view(results_list)


def _single_view(r: dict):
    img, dets, name = r["image"], r["dets"], r["name"]

    col_img, col_info = st.columns([5, 3], gap="large")

    with col_img:
        if dets:
            result_img = _draw_boxes(img, dets)
            st.image(result_img, use_column_width=True)
            c1, c2 = st.columns(2)
            with c1:
                st.download_button("⬇ With boxes", _to_bytes(result_img),
                                   f"det_{name}", "image/png", key="dl1")
            with c2:
                st.download_button("⬇ Original", _to_bytes(img),
                                   name, "image/png", key="dl2")
        else:
            st.image(img, use_column_width=True)
            st.caption("No detections. Try lowering confidence threshold.")

    with col_info:
        st.markdown(f"""
        <div style="text-align:center;padding:20px;background:#12121E;
                    border-radius:12px;border:1px solid #ffffff08;margin-bottom:16px">
          <div style="font-size:10px;color:#666680;text-transform:uppercase;
                      letter-spacing:1px;margin-bottom:6px">Detected</div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:48px;
                      font-weight:700;color:#6C63FF">{len(dets)}</div>
        </div>
        """, unsafe_allow_html=True)

        if dets:
            sorted_d = sorted(dets, key=lambda x: x["confidence"], reverse=True)
            for i, d in enumerate(sorted_d[:30]):
                cv = d["confidence"]
                c = "#4CAF50" if cv >= 0.7 else "#FF9800" if cv >= 0.4 else "#F44336"
                st.markdown(f"""
                <div class="ak-det-item">
                  <div style="display:flex;align-items:center;gap:8px">
                    <span style="font-family:'JetBrains Mono',monospace;font-size:10px;
                                 color:#555570;min-width:18px">{i+1:02d}</span>
                    <span style="font-size:13px;color:#E8E8F0;font-weight:500">
                      {d['class_name']}</span>
                  </div>
                  <span style="font-family:'JetBrains Mono',monospace;font-size:11px;
                               color:{c};font-weight:600">{cv:.0%}</span>
                </div>
                """, unsafe_allow_html=True)

    # Table
    if dets:
        divider()
        with st.expander(f"📋 Detail ({len(dets)} items)"):
            import pandas as pd
            df = pd.DataFrame([{
                "#": i+1, "Class": d["class_name"],
                "Conf": f"{d['confidence']:.3f}",
                "Box": f"({int(d['bbox'][0])},{int(d['bbox'][1])},{int(d['bbox'][2])},{int(d['bbox'][3])})",
            } for i, d in enumerate(sorted(dets, key=lambda x: x["confidence"], reverse=True))])
            st.dataframe(df, hide_index=True)


def _gallery_view(results_list: list):
    # Toggle
    view = st.radio("View", ["Grid", "List"], horizontal=True, label_visibility="collapsed")

    if view == "Grid":
        cols = st.columns(2)
        for i, r in enumerate(results_list):
            with cols[i % 2]:
                _gallery_card(r, i)
    else:
        for i, r in enumerate(results_list):
            _gallery_card(r, i)

    # Export
    divider()
    with st.expander("📥 Export all"):
        import pandas as pd
        rows = []
        for r in results_list:
            for d in r["dets"]:
                rows.append({"File": r["name"], "Class": d["class_name"],
                             "Confidence": f"{d['confidence']:.4f}",
                             "X1": int(d["bbox"][0]), "Y1": int(d["bbox"][1]),
                             "X2": int(d["bbox"][2]), "Y2": int(d["bbox"][3])})
        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df, hide_index=True)
            st.download_button("⬇ CSV", df.to_csv(index=False).encode(),
                               "detections.csv", "text/csv", key="csv_all")


def _gallery_card(r: dict, idx: int):
    img, dets, name = r["image"], r["dets"], r["name"]
    n = len(dets)

    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;
                padding:8px 12px;background:#12121E;border-radius:8px 8px 0 0;
                border:1px solid #ffffff08;border-bottom:none;margin-top:8px">
      <span style="font-size:12px;color:#C0C0D8;font-weight:500;
                   max-width:180px;overflow:hidden;text-overflow:ellipsis;
                   white-space:nowrap">{name}</span>
      <span class="ak-badge ak-badge-purple">{n}</span>
    </div>
    """, unsafe_allow_html=True)

    if dets:
        result_img = _draw_boxes(img, dets)
        st.image(result_img, use_column_width=True)
        st.download_button(f"⬇ Download", _to_bytes(result_img),
                           f"det_{name}", "image/png", key=f"g_{idx}")
    else:
        st.image(img, use_column_width=True)
