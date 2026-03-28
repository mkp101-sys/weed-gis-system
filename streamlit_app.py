import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os
import gdown

# -------------------------------
# 🔹 PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Weed Detection System", layout="centered")

st.title("🌱 Weed Detection System")
st.write("Upload an image to detect weeds using YOLO")

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
# 🔹 LOAD MODEL (FAST)
# -------------------------------
@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH)

model = load_model()

# -------------------------------
# 🔹 IMAGE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader(
    "📤 Upload Image",
    type=["jpg", "jpeg", "png"]
)

# -------------------------------
# 🔹 DETECTION
# -------------------------------
if uploaded_file:
    image = Image.open(uploaded_file)

    st.subheader("📷 Uploaded Image")
    st.image(image, use_container_width=True)

    if st.button("🔍 Detect Weeds"):
        with st.spinner("Running detection... 🚀"):
            results = model(image)
            result_img = results[0].plot()

        st.subheader("🌿 Detection Result")
        st.image(result_img, use_container_width=True)

        # Count detections
        boxes = results[0].boxes
        if boxes is not None:
            st.success(f"Detected objects: {len(boxes)}")
        else:
            st.warning("No weeds detected")

# -------------------------------
# 🔹 FOOTER
# -------------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + YOLO")
