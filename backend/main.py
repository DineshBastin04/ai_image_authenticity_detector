from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch
import cv2
import numpy as np
import sqlite3
from datetime import datetime
import os

from artifacts import detect_artifacts
from heatmap import generate_heatmap

from transformers import pipeline, AutoImageProcessor, ViTForImageClassification

app = FastAPI(title="AI Image Authenticity Detector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading AI Detection Model...")

# Load from local directory to ensure stability
MODEL_PATH = "models/prithivMLmods"

if not os.path.exists(MODEL_PATH):
    print(f"FATAL: Model directory {MODEL_PATH} not found. Please run download_prithiv.py first.")
    raise FileNotFoundError(f"Model directory {MODEL_PATH} not found.")

try:
    print(f"Loading model from {MODEL_PATH}...")
    # Force use of local files
    model = ViTForImageClassification.from_pretrained(MODEL_PATH, local_files_only=True)
    processor = AutoImageProcessor.from_pretrained(MODEL_PATH, local_files_only=True)
    pipe = pipeline("image-classification", model=model, feature_extractor=processor)
    print("Model loaded successfully!")
    print(f"Model Labels: {model.config.id2label}")
except Exception as e:
    print(f"FATAL: Failed to load model from {MODEL_PATH}: {e}")
    raise e

# Init SQLite DB if not exists
conn = sqlite3.connect("logs.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS detections(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    result TEXT,
    confidence REAL,
    created_at TEXT
)""")
conn.commit()
conn.close()

@app.post("/detect")
async def detect_ai(file: UploadFile = File(...)):
    # Load image
    image = Image.open(file.file).convert("RGB")
    
    # Run inference using Hugging Face pipeline
    predictions = pipe(image)
    
    # Sort by score to get the top prediction
    top_pred = max(predictions, key=lambda x: x["score"])
    
    # Dynamic Label Mapping
    # prithivMLmods labels: {0: 'Realism', 1: 'Deepfake'}
    
    label_map = {
        "fake": "AI-Generated",
        "real": "Real",
        "true": "Real",
        "human": "Real",
        "ai": "AI-Generated",
        "artificial": "AI-Generated",
        "deepfake": "AI-Generated",
        "realism": "Real",
        "0": "Real",      # Assuming 0 is Realism
        "1": "AI-Generated",
        "LABEL_0": "Real",
        "LABEL_1": "AI-Generated"
    }
    
    raw_label = str(top_pred["label"]).lower().strip()
    result = label_map.get(raw_label)
    
    if not result:
        lc_raw = raw_label.lower()
        if "real" in lc_raw or "human" in lc_raw:
            result = "Real"
        elif "fake" in lc_raw or "ai" in lc_raw or "artificial" in lc_raw:
            result = "AI-Generated"
        else:
            result = f"Unknown ({top_pred['label']})"

    confidence = top_pred["score"]

    # Artifact and heatmap
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    artifacts = detect_artifacts(img_cv)
    heatmap_img = generate_heatmap(img_cv)

    # Log
    try:
        db = sqlite3.connect("logs.db")
        c = db.cursor()
        c.execute(
            "INSERT INTO detections(filename,result,confidence,created_at) VALUES (?,?,?,?)",
            (file.filename, result, float(confidence), datetime.now().isoformat())
        )
        db.commit()
        db.close()
    except Exception as e:
        print(f"Database error: {e}")

    _, encoded = cv2.imencode(".jpg", heatmap_img)

    return {
        "result": result,
        "confidence": float(confidence),
        "artifacts": artifacts,
        "heatmap": encoded.tobytes().hex(),
        "timestamp": datetime.now().isoformat()
    }
