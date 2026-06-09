# 🌱 WeedScan

### Automated Weed Detection in Crop Fields Using YOLOv8, Roboflow & GPS-Integrated GIS Mapping

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red)
![GIS](https://img.shields.io/badge/GIS-GPS_Mapping-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Overview

WeedScan is an AI-powered Precision Agriculture system that automatically detects weeds in crop fields using YOLOv8 object detection and generates GPS-enabled GIS maps for targeted herbicide application.

Developed as part of the **M.Sc. Agriculture Analytics Program** at the **Indian Institute of Remote Sensing (IIRS), ISRO Dehradun**, WeedScan aims to reduce herbicide waste, lower farming costs, and support sustainable agriculture through AI and geospatial technologies.

Traditional blanket herbicide spraying wastes chemicals, increases production costs, contaminates soil and groundwater, and damages soil microbiomes. WeedScan solves this problem by providing an affordable, scalable, and fully open-source solution for site-specific weed management.

---

## 🚀 Features

✅ Automated weed detection using YOLOv8

✅ Upload drone or smartphone field images

✅ GPS-integrated weed location mapping

✅ Interactive GIS visualization

✅ Streamlit-based web application

✅ Gradio demo interface

✅ Folium GIS weed hotspot mapping

✅ Detection history tracking

✅ CSV export for precision spraying systems

✅ Drone-ready workflow

✅ 100% Open Source and Reproducible

---

## 🎯 Problem Statement

### The Weed Infestation Crisis

- 🌾 34% annual crop yield loss due to weeds
- 💰 ₹60+ Billion herbicide waste annually
- 🌍 Soil and groundwater contamination
- 🚜 Blanket spraying across entire fields
- 👨‍🌾 Lack of affordable precision agriculture tools

WeedScan provides a low-cost AI-powered alternative capable of identifying weed locations before herbicide application.

---

## 🏗 System Workflow

```text
Field Image
     │
     ▼
YOLOv8 Detection
     │
     ▼
Bounding Boxes + Confidence Scores
     │
     ▼
Coordinate Extraction
     │
     ▼
CSV Generation
     │
     ▼
GPS Mapping
     │
     ▼
GIS Visualization
     │
     ▼
Precision Herbicide Application
```

---

## 🛠 Technology Stack

### Machine Learning

- YOLOv8n
- PyTorch
- Roboflow

### Computer Vision

- OpenCV
- Pillow
- NumPy

### Data Processing

- Pandas

### GIS & Mapping

- Folium
- Leaflet.js
- GPS Coordinate Mapping

### Deployment

- Streamlit
- FastAPI
- Gradio

### Environment

- Google Colab T4 GPU
- Python 3.10+

---

## 📂 Project Structure

```text
WeedScan/
│
├── streamlit_app.py
├── app.py
├── best.pt
├── requirements.txt
├── detections/
├── outputs/
├── maps/
├── data/
├── notebooks/
├── assets/
└── README.md
```

---

## ⚙ Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/weedscan.git
cd weedscan
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Mac/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶ Run Streamlit App

```bash
streamlit run streamlit_app.py
```

Open:

```text
http://localhost:8501
```

---

## 📊 Model Training Configuration

| Parameter | Value |
|------------|--------|
| Model | YOLOv8n |
| Epochs | 50 |
| Image Size | 640 × 640 |
| Optimizer | AdamW |
| Scheduler | Cosine LR |
| Dataset Split | 70/15/15 |
| Platform | Google Colab T4 GPU |

---

## 📈 Performance Metrics

| Metric | Score |
|----------|----------|
| mAP@0.5 | 0.82 |
| Precision | 0.81 |
| Recall | 0.77 |
| F1 Score | 0.79 |

### Performance Summary

- All acceptance criteria exceeded.
- Strong generalization without overfitting.
- Validation loss closely tracked training loss.
- Stable convergence across 50 epochs.

---

## 🗺 GIS Integration

WeedScan generates geospatial outputs that can be directly integrated into precision agriculture workflows.

### Supported Outputs

- GPS-linked weed coordinates
- CSV export
- GIS hotspot mapping
- Drone spraying route generation
- Variable-rate herbicide application

### Example CSV Output

```csv
class,confidence,x_center,y_center,width,height
weed,0.91,0.54,0.61,0.12,0.14
weed,0.87,0.31,0.44,0.10,0.11
```

---

## 🌐 Deployment Interfaces

### 1️⃣ Streamlit GIS Application

Features:

- Interactive India map
- GPS pin selection
- Field image upload
- Live YOLOv8 inference
- Detection history database
- Multi-location visualization

---

### 2️⃣ Gradio Demo

Features:

- Drag-and-drop interface
- Instant model predictions
- Public shareable URL
- No server configuration required

---

### 3️⃣ Folium GIS Map

Features:

- Interactive HTML map
- Weed hotspot visualization
- GPS coordinate plotting
- Detection popups and summaries

---

## 📸 Screenshots

Add your screenshots here:

### Streamlit Interface

```markdown
![Streamlit App](images/streamlit_app.png)
```

### Detection Results

```markdown
![Detection](images/detection_result.png)
```

### GIS Map

```markdown
![GIS Map](images/gis_map.png)
```

---

## 🌍 Real-World Impact

### 👨‍🌾 Farm Level

- 60–70% reduction in herbicide usage
- Increased farmer profitability
- Reduced labor requirements

### 🌱 Ecosystem Level

- Reduced soil contamination
- Improved groundwater protection
- Preservation of beneficial soil microbes

### 🏛 Policy Level

- Weed hotspot identification
- Regional agricultural planning
- Data-driven subsidy allocation

### 🔬 Research Level

- Open-source benchmark for agricultural AI
- Fully reproducible workflow
- GIS-enabled precision agriculture framework

---

## 🔮 Future Scope

- Multi-class Indian weed detection
- Parthenium detection
- Cyperus rotundus detection
- Phalaris minor detection
- UAV aerial imagery training
- GPS EXIF extraction
- ONNX deployment
- TorchScript export
- Android mobile application
- QGIS integration
- Google Earth Engine integration
- Real-time drone spraying support

---

## 👨‍💻 

### Maharshi K. Patel

- Streamlit GIS Application
- Gradio Interface
- Folium GIS Mapping
- CSV Export Pipeline
- Documentation
- FastAPI Integration
- Project Deployment
- Dataset Preparation
- Roboflow Integration
- YOLOv8 Training
- Model Evaluation
- Training Monitoring
- Hyperparameter Optimization

---

## 🎓 Academic Information

**Project Title:** WeedScan – Automated Weed Detection in Crop Fields

**Program:** M.Sc. Agriculture Analytics

**Institution:** Indian Institute of Remote Sensing (IIRS), ISRO Dehradun

**Supervisor:** Dr. Kamal Pandey

**Year:** 2026

---

## 📚 Citation

If you use this project in your research, please cite:

```text
Maharshi k patel (2026).
WeedScan: Automated Weed Detection in Crop Fields Using YOLOv8,
Roboflow and GPS-Integrated GIS Mapping.
M.Sc. Agriculture Analytics,
Indian Institute of Remote Sensing (IIRS), ISRO Dehradun.
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

Feel free to fork the repository and submit a pull request.

---


## 🙏 Acknowledgements

- Ultralytics YOLOv8
- Roboflow
- Google Colab
- Streamlit
- Folium
- FastAPI
- PyTorch
- Open Source Community

---

# ⭐ Precision Agriculture Doesn't Need Expensive Hardware — Just Smarter Software.

