import streamlit as st
from ultralytics import YOLO
from PIL import Image, ImageDraw
import folium
from streamlit_folium import st_folium
import gdown
import os

# ── PAGE CONFIG ──
st.set_page_config(page_title="WeedScan", page_icon="🌿", layout="wide")

# ── MODEL FILE ID ──
MODEL_FILE_ID = "1Ka08yJi6Mw4mhsTSN1GxR5HDBnKUK91H"

# ── CUSTOM CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&family=DM+Mono&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: #1a1208; color: #f5f0e0; }
.stApp { background-color: #1a1208; }
.metric-card { background: #2c1f0e; border: 1px solid #3a5c2a; border-radius: 10px; padding: 14px; text-align: center; }
.metric-value { font-size: 1.8rem; color: #8ab84a; font-family: 'DM Mono', monospace; font-weight: 600; }
.metric-label { font-size: 0.72rem; color: #5a8a3a; font-family: 'DM Mono', monospace; letter-spacing: 0.1em; text-transform: uppercase; }
.det-card { background: rgba(58,92,42,0.2); border: 1px solid #3a5c2a; border-radius: 10px; padding: 12px 16px; margin-bottom: 10px; }
.det-name { font-size: 1rem; color: #b8d878; font-weight: 600; text-transform: capitalize; }
.det-conf { font-family: 'DM Mono', monospace; font-size: 0.8rem; color: #8ab84a; }
.section-label { font-family: 'DM Mono', monospace; font-size: 0.65rem; letter-spacing: 0.15em; color: #5a8a3a; text-transform: uppercase; margin-bottom: 8px; }
section[data-testid="stSidebar"] { background: #2c1f0e !important; border-right: 1px solid #3a5c2a; }
.stButton > button { background: linear-gradient(135deg, #3a5c2a, #5a8a3a) !important; color: #f5f0e0 !important; border: none !important; border-radius: 10px !important; font-weight: 500 !important; width: 100% !important; }
hr { border-color: #3a5c2a !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
for key, val in {
    'model': None, 'saved_locations': [],
    'total_scans': 0, 'total_weeds': 0,
    'clicked_lat': None, 'clicked_lng': None,
    'last_result': None
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── LOAD MODEL (auto on startup) ──
@st.cache_resource
def load_model():
    model_path = "best.pt"
    if not os.path.exists(model_path):
        gdown.download(f"https://drive.google.com/uc?id={MODEL_FILE_ID}", model_path, quiet=False)
    return YOLO(model_path)

if st.session_state.model is None:
    with st.spinner("📥 Loading WeedScan model..."):
        try:
            st.session_state.model = load_model()
        except Exception as e:
            st.error(f"❌ Could not load model: {e}")

# ── HEADER ──
st.markdown("""
<div style="background:#2c1f0e;border-bottom:1px solid #3a5c2a;padding:14px 0 12px 0;margin-bottom:20px;display:flex;align-items:center;gap:12px">
  <span style="font-size:1.8rem">🌿</span>
  <span style="font-family:'DM Mono',monospace;font-size:1.5rem;color:#b8d878;font-weight:700;letter-spacing:0.04em">WeedScan</span>
  <span style="color:#5a8a3a;font-family:'DM Mono',monospace;font-size:0.75rem;margin-left:auto">Field Intelligence Dashboard</span>
</div>
""", unsafe_allow_html=True)

# ── METRICS ──
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{st.session_state.total_scans}</div><div class="metric-label">Total Scans</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{st.session_state.total_weeds}</div><div class="metric-label">Weeds Found</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{len(st.session_state.saved_locations)}</div><div class="metric-label">Locations Saved</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("### 🌿 WeedScan")
    if st.session_state.model:
        st.success("✅ Model Ready")
        classes = list(st.session_state.model.names.values())
        st.markdown(f"**Detects:** {', '.join(classes)}")
    else:
        st.warning("⏳ Loading model...")

    st.markdown("---")
    st.markdown("### 📍 Saved Locations")
    if st.session_state.saved_locations:
        for loc in reversed(st.session_state.saved_locations[-8:]):
            icon = "🔴" if loc['has_weeds'] else "🟢"
            st.markdown(f"{icon} **{loc['top_class']}**  \n`{loc['lat']:.4f}, {loc['lng']:.4f}`")
        st.markdown("---")
        if st.button("🗑️ Clear All"):
            st.session_state.saved_locations = []
            st.session_state.total_scans = 0
            st.session_state.total_weeds = 0
            st.session_state.last_result = None
            st.rerun()
    else:
        st.markdown("<span style='color:#5a8a3a;font-size:0.8rem'>No locations saved yet</span>", unsafe_allow_html=True)

# ── MAIN LAYOUT ──
left_col, right_col = st.columns([3, 2])

with left_col:
    st.markdown('<div class="section-label">📍 Step 1 — Click map to select field location</div>', unsafe_allow_html=True)

    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

    for loc in st.session_state.saved_locations:
        color = "red" if loc['has_weeds'] else "green"
        folium.Marker(
            [loc['lat'], loc['lng']],
            popup=folium.Popup(
                f"<b>{loc['top_class']}</b><br>Conf: {loc['top_conf']}%<br>{loc['count']} weed(s) found",
                max_width=200
            ),
            icon=folium.Icon(color=color, icon="leaf", prefix="fa")
        ).add_to(m)

    if st.session_state.clicked_lat:
        folium.CircleMarker(
            [st.session_state.clicked_lat, st.session_state.clicked_lng],
            radius=10, color="#d4a843", fill=True, fill_color="#d4a843", fill_opacity=0.6
        ).add_to(m)

    map_data = st_folium(m, height=430, width=None, returned_objects=["last_clicked"])

    if map_data and map_data.get("last_clicked"):
        st.session_state.clicked_lat = map_data["last_clicked"]["lat"]
        st.session_state.clicked_lng = map_data["last_clicked"]["lng"]
        st.session_state.last_result = None

    if st.session_state.clicked_lat:
        st.success(f"📍 Location pinned: `{st.session_state.clicked_lat:.5f}, {st.session_state.clicked_lng:.5f}`")
    else:
        st.info("👆 Click anywhere on the map to pin your field location")

with right_col:
    st.markdown('<div class="section-label">🌿 Step 2 — Upload field image</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)

    can_scan = (
        st.session_state.model is not None and
        uploaded_file is not None and
        st.session_state.clicked_lat is not None
    )

    if not st.session_state.model:
        st.warning("⏳ Model is loading...")
    elif not st.session_state.clicked_lat:
        st.warning("⚠️ Click on the map first")
    elif not uploaded_file:
        st.warning("⚠️ Upload a field image")

    if st.button("🔍 Scan for Weeds", disabled=not can_scan):
        with st.spinner("🌿 Analysing image..."):
            image = Image.open(uploaded_file).convert("RGB")
            results = st.session_state.model(image)
            draw = ImageDraw.Draw(image)
            detections = []
            COLORS = [(220,60,40),(40,160,80),(60,120,220),(200,140,30),(160,60,200)]

            for r in results:
                for i, box in enumerate(r.boxes):
                    cls_id = int(box.cls)
                    cls_name = st.session_state.model.names[cls_id]
                    conf = round(float(box.conf), 2)
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    color = COLORS[i % len(COLORS)]
                    for t in range(3):
                        draw.rectangle([x1-t, y1-t, x2+t, y2+t], outline=color)
                    label = f"{cls_name} {int(conf*100)}%"
                    lw = len(label) * 8 + 10
                    draw.rectangle([x1, y1-22, x1+lw, y1], fill=color)
                    draw.text((x1+5, y1-18), label, fill=(255,255,255))
                    detections.append({"class": cls_name, "confidence": conf})

            st.session_state.total_scans += 1
            st.session_state.total_weeds += len(detections)
            has_weeds = len(detections) > 0

            st.session_state.saved_locations.append({
                'lat': st.session_state.clicked_lat,
                'lng': st.session_state.clicked_lng,
                'has_weeds': has_weeds,
                'top_class': detections[0]['class'] if has_weeds else "Clean",
                'top_conf': int(detections[0]['confidence']*100) if has_weeds else 0,
                'count': len(detections),
                'detections': detections,
            })
            st.session_state.last_result = {'image': image, 'detections': detections}
        st.rerun()

    # ── RESULTS ──
    if st.session_state.last_result:
        st.markdown("---")
        st.markdown('<div class="section-label">🔍 Detection Result</div>', unsafe_allow_html=True)
        res = st.session_state.last_result
        caption = f"⚠️ {len(res['detections'])} Weed(s) Detected!" if res['detections'] else "✅ Field Clean"
        st.image(res['image'], caption=caption, use_container_width=True)

        if res['detections']:
            for det in res['detections']:
                pct = int(det['confidence'] * 100)
                st.markdown(f"""<div class="det-card">
                    <div class="det-name">🌿 {det['class']}</div>
                    <div class="det-conf">Confidence: {pct}%</div>
                </div>""", unsafe_allow_html=True)
                st.progress(det['confidence'])
        else:
            st.success("✅ No weeds detected — field looks clean!")
