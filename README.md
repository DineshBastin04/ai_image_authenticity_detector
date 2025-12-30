# 🕵️‍♂️ AI Authenticator (Open Source)

**Detect if an image is Real or AI-Generated using advanced Deep Learning.**

This project acts as a "Reality Check" for digital media, helping users verify the authenticity of images. It uses a **FastAPI** backend powering a **fine-tuned Vision Transformer (ViT)** model, coupled with a beautiful **React Web App** and a **Flutter Mobile App**.

---

## 🚀 Features

*   **Dual-Frontend**: responsive Web Dashboard & Native Mobile App.
*   **Deep Learning Core**: Powered by Hugging Face Transformers (`prithivMLmods/Deep-Fake-Detector-v2-Model`).
*   **Visual Forensics**: Generates heatmaps to highlight suspicious noise/pixel variances.
*   **Modern UI**: Dark-themed, premium aesthetic.
*   **Open Source**: MIT Licensed.

---

## 🛠️ Tech Stack

*   **Backend**: Python, FastAPI, PyTorch, Transformers, OpenCV
*   **Web**: React, Vite, Vanilla CSS
*   **Mobile**: Flutter, Dart
*   **Database**: SQLite (for logging requests)

---

## 📦 Setup Guide

### 1. Backend (Python/FastAPI)
The brain of the operation.
```bash
cd backend
# Create virtual environment (optional but recommended)
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Install dependencies based on requirements.txt
pip install -r requirements.txt

# ⬇️ IMPORTANT: Download the AI Model locally
python download_prithiv.py

# Run the server
uvicorn main:app --reload
```
*Server runs at `http://localhost:8000`*

### 2. Frontend Web (React)
The web dashboard.
```bash
cd frontend-web
npm install
npm run dev
```
*Web app runs at `http://localhost:5173`*

### 3. Frontend Mobile (Flutter)
The Android/iOS app.
```bash
cd frontend-mobile
flutter pub get
flutter run
```
*Note: Ensure you have an Emulator running or a physical device connected.*

---

## 🧪 Testing

We have included a test script to check if your backend is running correctly.
```bash
cd backend
python test_api.py
```

## ⚠️ Limitations
*   The current model is a free pre-trained one from Hugging Face.
*   It may not detect the absolute latest AI generators (e.g., Midjourney v6) with 100% accuracy.
*   For production use, consider fine-tuning on a newer dataset.

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## 📜 License
[MIT](https://choosealicense.com/licenses/mit/)
