from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ultralytics import YOLO
from PIL import Image, ImageDraw
import io
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = YOLO("model/best.pt")

COLORS = [(220,60,40),(40,160,80),(60,120,220),(200,140,30),(160,60,200)]

@app.get("/")
def home():
    return {"message": "WeedScan API is running!"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    results = model(image)
    draw = ImageDraw.Draw(image)
    detections = []

    for r in results:
        for i, box in enumerate(r.boxes):
            cls_id = int(box.cls)
            cls_name = model.names[cls_id]
            conf = round(float(box.conf), 2)
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            color = COLORS[i % len(COLORS)]
            for t in range(3):
                draw.rectangle([x1-t, y1-t, x2+t, y2+t], outline=color)
            label = f"{cls_name} {int(conf*100)}%"
            label_w = len(label) * 8 + 10
            draw.rectangle([x1, y1-22, x1+label_w, y1], fill=color)
            draw.text((x1+5, y1-18), label, fill=(255,255,255))
            detections.append({
                "class": cls_name,
                "confidence": conf,
                "bbox": [x1, y1, x2, y2]
            })

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=90)
    img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return JSONResponse({
        "detections": detections,
        "annotated_image": f"data:image/jpeg;base64,{img_b64}"
    })
