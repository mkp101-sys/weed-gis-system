import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os
import gdown
import json
import base64
import io
from datetime import datetime

# -------------------------------
# 🔹 PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Weed GIS System", layout="wide")
st.title("🌱 Weed Detection GIS System")

# -------------------------------
# 🔹 MODEL DOWNLOAD
# -------------------------------
MODEL_PATH = "best.pt"
FILE_ID = "1Ka08yJi6Mw4mhsTSN1GxR5HDBnKUK91H"

if not os.path.exists(MODEL_PATH):
    with st.spinner("Downloading model... ⏳"):
        gdown.download(
            f"https://drive.google.com/uc?id={FILE_ID}",
            MODEL_PATH,
            quiet=False
        )

# -------------------------------
# 🔹 LOAD MODEL
# -------------------------------
@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH)

model = load_model()

# -------------------------------
# 🔹 DATABASE (JSON FILE)
# -------------------------------
DB_FILE = "weed_locations.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f)

def img_to_base64(pil_img):
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG", quality=70)
    return base64.b64encode(buf.getvalue()).decode()

# -------------------------------
# 🔹 LAYOUT: Two columns
# -------------------------------
col_map, col_detect = st.columns([3, 2])

# ================================
# LEFT: MAP (Click or Search)
# ================================
with col_map:
    st.subheader("🗺️ Step 1: Pick a Location")
    st.caption("Click on the map OR search by place name to set a geotag.")

    db = load_db()

    # Build markers JS for saved locations
    markers_js = ""
    for loc_key, loc_data in db.items():
        lat, lng = loc_data["lat"], loc_data["lng"]
        count = len(loc_data.get("detections", []))
        popup_imgs = ""
        for det in loc_data.get("detections", []):
            popup_imgs += f'<img src="data:image/jpeg;base64,{det["image"]}" width="150"><br><small>{det["timestamp"]}</small><hr>'
        popup_html = f"""
        <b>📍 {loc_data.get('name', loc_key)}</b><br>
        Lat: {lat:.5f}, Lng: {lng:.5f}<br>
        Photos: {count}<br><br>
        {popup_imgs}
        """
        popup_escaped = popup_html.replace("`", "\\`").replace("${", "\\${")
        markers_js += f"""
        L.marker([{lat}, {lng}]).addTo(map)
          .bindPopup(`{popup_escaped}`);
        """

    map_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8"/>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
      <link rel="stylesheet" href="https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.css"/>
      <style>
        body {{ margin: 0; padding: 0; }}
        #map {{ height: 480px; width: 100%; }}
        #info {{
          position: absolute; bottom: 10px; left: 50%;
          transform: translateX(-50%);
          background: rgba(0,0,0,0.75); color: #fff;
          padding: 8px 16px; border-radius: 20px;
          font-family: sans-serif; font-size: 14px;
          z-index: 9999; pointer-events: none;
        }}
      </style>
    </head>
    <body>
      <div id="map"></div>
      <div id="info">🖱️ Click anywhere to drop a pin</div>
      <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
      <script src="https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.js"></script>
      <script>
        var map = L.map('map').setView([22.9, 79.0], 5);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
          attribution: '© OpenStreetMap contributors'
        }}).addTo(map);

        // Search box
        L.Control.geocoder({{
          defaultMarkGeocode: false,
          placeholder: "Search village, city..."
        }}).on('markgeocode', function(e) {{
          var latlng = e.geocode.center;
          placePin(latlng.lat, latlng.lng, e.geocode.name);
          map.setView(latlng, 13);
        }}).addTo(map);

        // Existing saved markers
        {markers_js}

        // Click pin
        var clickMarker = null;
        function placePin(lat, lng, name) {{
          if (clickMarker) map.removeLayer(clickMarker);
          clickMarker = L.marker([lat, lng], {{
            icon: L.icon({{
              iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
              shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
              iconSize: [25, 41], iconAnchor: [12, 41]
            }})
          }}).addTo(map).bindPopup("📍 Selected: " + (name || (lat.toFixed(5) + ", " + lng.toFixed(5)))).openPopup();

          document.getElementById('info').innerHTML =
            "📍 Selected: " + lat.toFixed(5) + ", " + lng.toFixed(5);

          // Send to Streamlit via query param trick
          window.parent.postMessage({{
            type: "streamlit:setComponentValue",
            value: lat + "," + lng + "," + (name || "")
          }}, "*");
        }}

        map.on('click', function(e) {{
          placePin(e.latlng.lat, e.latlng.lng, "");
        }});
      </script>
    </body>
    </html>
    """

    # Render map
    from streamlit.components.v1 import html as st_html
    st_html(map_html, height=490)

    st.markdown("---")
    st.subheader("📌 Or Enter Coordinates Manually")
    coord_input = st.text_input("Paste lat, lng (e.g. 28.6139, 77.2090)", placeholder="28.6139, 77.2090")
    place_name = st.text_input("📛 Location Name (optional)", placeholder="e.g. Delhi Farm Field 1")

    selected_lat = None
    selected_lng = None

    if coord_input:
        try:
            parts = coord_input.strip().split(",")
            selected_lat = float(parts[0].strip())
            selected_lng = float(parts[1].strip())
            st.success(f"✅ Location set: {selected_lat:.5f}, {selected_lng:.5f}")
        except:
            st.error("❌ Invalid format. Use: lat, lng (e.g. 28.6139, 77.2090)")

# ================================
# RIGHT: DETECT + SAVE
# ================================
with col_detect:
    st.subheader("📷 Step 2: Upload & Detect")

    uploaded_file = st.file_uploader(
        "Upload weed image for this location",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        if st.button("🔍 Detect Weeds & Save to Map"):
            if selected_lat is None or selected_lng is None:
                st.warning("⚠️ Please enter coordinates in the left panel first!")
            else:
                with st.spinner("Running YOLO detection... 🚀"):
                    results = model(image)
                    result_img_arr = results[0].plot()
                    result_pil = Image.fromarray(result_img_arr)

                st.image(result_pil, caption="Detection Result", use_container_width=True)

                boxes = results[0].boxes
                count = len(boxes) if boxes is not None else 0
                if count > 0:
                    st.success(f"🌿 Detected {count} object(s)")
                else:
                    st.warning("No weeds detected")

                # Save to DB
                db = load_db()
                loc_key = f"{selected_lat:.4f}_{selected_lng:.4f}"

                if loc_key not in db:
                    db[loc_key] = {
                        "lat": selected_lat,
                        "lng": selected_lng,
                        "name": place_name or loc_key,
                        "detections": []
                    }

                db[loc_key]["detections"].append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "weed_count": count,
                    "image": img_to_base64(result_pil)
                })

                save_db(db)
                st.success(f"📍 Saved to map! Total photos at this location: {len(db[loc_key]['detections'])}")
                st.info("🔄 Refresh the page to see the updated pin on the map.")

# ================================
# BOTTOM: SAVED LOCATIONS TABLE
# ================================
st.markdown("---")
st.subheader("📋 All Saved Locations")

db = load_db()
if db:
    for loc_key, loc_data in db.items():
        with st.expander(f"📍 {loc_data.get('name', loc_key)} — {len(loc_data['detections'])} photo(s)"):
            st.write(f"**Lat:** {loc_data['lat']} | **Lng:** {loc_data['lng']}")
            cols = st.columns(min(len(loc_data["detections"]), 3))
            for i, det in enumerate(loc_data["detections"]):
                with cols[i % 3]:
                    img_bytes = base64.b64decode(det["image"])
                    st.image(img_bytes, caption=f"🕒 {det['timestamp']} | Weeds: {det['weed_count']}", use_container_width=True)
else:
    st.info("No locations saved yet. Upload an image with a location to get started!")

# -------------------------------
# 🔹 FOOTER
# -------------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + YOLO + Leaflet.js")

