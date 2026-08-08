<div align="center">

<img src="logo.png" alt="LOOM Logo" width="120" />

# LOOM — Fashion MNIST Classification
**A production-grade deep learning API for clothing image classification, wrapped in a real-time Streamlit control room.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.21-FF6F00?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Validation-E92063?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Supabase](https://img.shields.io/badge/Database-Supabase-3FCF8E?logo=supabase&logoColor=white)](https://supabase.com/)

</div>

---

## What is LOOM?

LOOM is a full-stack deep learning service that classifies grayscale clothing images into one of 10 Fashion-MNIST categories in real time. It is composed of two independent components that work together:

- **Backend** — a FastAPI service that loads a trained Keras dense neural network and exposes it as a secured REST API, with Supabase-backed request logging on every call.
- **Frontend** — a Streamlit control room (named LOOM) that connects to the API to offer single-image classification, batch classification, model insights, and live usage analytics — all without loading the model locally.



--- 
---

> ⚠️ **Security note:** the `X-API-Key` below is a **demo key** shared for evaluation purposes only. If this repository is public, rotate the key (set a new `SECRET_KEY_TOKEN` in your Hugging Face Space secrets) so this value stops working. Never rely on a key that has appeared in a public README for anything beyond a quick demo.

```
Demo X-API-Key: c0c2d9d05029aed5d5174ff5ff8e6d88
```

---

## Features

| Feature | Detail |
|---|---|
| 🚀 **Async FastAPI backend** | Production-grade, non-blocking request handling via Uvicorn |
| 🧠 **Pre-trained Keras model** | Dense neural network trained on Fashion-MNIST, saved as `.keras` |
| 🔐 **API key authentication** | Every protected endpoint requires `X-API-KEY` in the request header |
| 📊 **Supabase logging** | Every `/classify` call (success or failure) is logged to Postgres in real time |
| 🗂️ **Batch classification** | Upload multiple images at once; results downloadable as CSV |
| 🔁 **Duplicate-request detection** | SHA-256 fingerprint on input — identical requests reuse the cached result |
| 📈 **Live usage analytics** | KPI cards, class split bar chart, requests-over-time with dynamic bucketing |
| 🌍 **CORS enabled** | Ready for cross-origin frontends out of the box |

---

## The 10 Garment Classes

| Index | Class | Emoji |
|---|---|---|
| 0 | T-Shirt | 👕 |
| 1 | Trouser | 👖 |
| 2 | Pullover | 🧶 |
| 3 | Dress | 👗 |
| 4 | Coat | 🧥 |
| 5 | Sandal | 👡 |
| 6 | Shirt | 👔 |
| 7 | Sneaker | 👟 |
| 8 | Bag | 👜 |
| 9 | Ankle Boot | 🥾 |

Each class has exactly **6,000 training images** and **1,000 test images** in the original Fashion-MNIST dataset — a perfectly balanced split.

---

## Model Architecture

The deployed model is a fully-connected (dense) neural network — no convolutions — trained from scratch on Fashion-MNIST.

```
Input image  →  28×28 grayscale pixels, normalized to [0, 1]
Flatten      →  (784,)          |   0 parameters
Dense ReLU   →  (128,)          | 100,480 parameters  ← largest layer
Dense ReLU   →  (64,)           |   8,256 parameters
Dense ReLU   →  (32,)           |   2,080 parameters
Dense Softmax→  (10,)           |     330 parameters
                                 ──────────────────
                       Total:   | 111,146 parameters
```

**Training configuration:**

| Setting | Value |
|---|---|
| Optimizer | SGD (lr = 0.01) |
| Loss function | `sparse_categorical_crossentropy` |
| Batch size | 32 |
| Max epochs | 30 |
| Early stopping | `monitor=val_loss`, `patience=5`, `restore_best_weights=True` |
| Random seed | 2025 |
| Final val accuracy | **88.27%** |

See [`F_MNIST.ipynb`](./F_MNIST.ipynb) for the complete training pipeline.

---

## Project Structure

```
.
├── main.py                    # FastAPI app — routes, auth, /logs endpoint
├── pyproject.toml             # Project metadata and dependencies
├── .env.example               # Environment variable template
├── artifacts/
│   └── model.keras            # Trained Keras model (not tracked by Git)
├── F_MNIST.ipynb              # Training notebook
├── src/
│   └── utils/
│       ├── config.py          # Env loading, model loading, Supabase client
│       ├── inference.py       # Image preprocessing + prediction logic
│       ├── logger.py          # Supabase log writer (fire-and-forget)
│       └── models.py          # Pydantic response schema
└── streamlit_app/
    └── streamlit_app.py       # LOOM — the Streamlit control room
```

---

## Requirements

**Backend**
- Python 3.12
- See `pyproject.toml` for pinned versions — key packages:
  - `fastapi[standard]==0.139.2`
  - `uvicorn==0.51.0`
  - `tensorflow==2.21.0`
  - `pydantic==2.13.4`
  - `supabase==2.31.0`
  - `Pillow==11.0.0`
  - `python-dotenv==1.2.2`
  - `python-multipart==0.0.32`

**Frontend (LOOM)**
- `streamlit`
- `plotly`
- `pandas`
- `requests`

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install backend dependencies

```bash
pip install -e .                # installs from pyproject.toml
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
APP_NAME="LOOM"
VERSION="1.0"
API_SECRET_KEY="your-strong-secret-key"
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_KEY="your-service-role-key"
```

> ⚠️ Use the **`service_role`** key for `SUPABASE_KEY` (not the `anon` key) — it bypasses Row Level Security so the backend can write logs. Never expose it in the frontend.

### 5. Add the trained model

Place the trained model file at:

```
artifacts/model.keras
```

---

## Running the Services

### Backend API

```bash
uvicorn main:app --reload
```

Available at: `http://127.0.0.1:8000`
Swagger UI: `http://127.0.0.1:8000/docs`

### Frontend (LOOM)

```bash
cd streamlit_app
pip install streamlit plotly pandas requests
streamlit run streamlit_app.py
```

Available at: `http://localhost:8501`

---

## API Reference

### `GET /`
Health check — no authentication required.

**Response**
```json
{ "message": "Up & Running" }
```

---

### `POST /classify`
Classify a clothing image. Requires `X-API-KEY` header.

**Headers**

| Header | Required | Description |
|---|---|---|
| `X-API-KEY` | ✅ | Your secret API key |

**Body** — `multipart/form-data`

| Field | Type | Description |
|---|---|---|
| `file` | File | Image of a clothing item (PNG, JPG, WebP…) |

**Example**
```bash
curl -X POST "http://127.0.0.1:8000/classify" \
  -H "X-API-KEY: your-secret-key" \
  -F "file=@sneaker.png"
```

**Success response**
```json
{
  "class_index": 7,
  "class_name": "Sneaker",
  "confidence": 98.42
}
```

**Error responses**

| Status | Reason |
|---|---|
| `403` | Missing or invalid API key |
| `500` | Image processing or model inference failure |

---

### `GET /logs`
Returns all logged classification requests (newest first). Requires `X-API-KEY` header. Used by the LOOM Usage Analytics page.

**Response**
```json
{
  "count": 42,
  "logs": [
    {
      "id": 42,
      "created_at": "2026-08-05T14:22:10.123Z",
      "predicted_class": "Sneaker",
      "class_index": 7,
      "confidence": 98.42,
      "success": true
    }
  ]
}
```

---

## Image Preprocessing Pipeline

Every image uploaded to `/classify` goes through the following steps before reaching the model:

1. **Open** — load from raw bytes (any common format)
2. **Grayscale** — convert to `L` mode if not already
3. **Resize** — scale to exactly `28×28` pixels
4. **Normalize** — divide pixel values by 255 → `[0.0, 1.0]`
5. **Reshape** — add batch dimension → `(1, 28, 28)`
6. **Predict** — pass through the Keras model, return `argmax` class + confidence

---

## Supabase Logging

Every `/classify` call — whether it succeeds or fails — writes one row to the `predictions_log` table in Supabase:

| Column | Type | Description |
|---|---|---|
| `id` | bigint (auto) | Primary key |
| `created_at` | timestamptz | UTC timestamp of the request |
| `predicted_class` | text | Class name (null on failure) |
| `class_index` | int | Class index 0–9 (null on failure) |
| `confidence` | float | Model confidence % (null on failure) |
| `success` | bool | Whether inference succeeded |

Logging failures are swallowed silently — a Supabase outage will never break the prediction response.

---

## Security Notes

- The `/classify` and `/logs` endpoints both require a valid `X-API-KEY` header.
- Never commit your `.env` file — it is excluded by `.gitignore`.
- `SUPABASE_KEY` must be the `service_role` secret and must only live server-side.
- CORS is currently open (`allow_origins=["*"]`). Restrict this in production.

---

## Live Deployment

| Component | URL |
|---|---|
| Backend API | `https://churn-detection-classification-project.fastapicloud.dev` |
| API Docs (Swagger) | `https://churn-detection-classification-project.fastapicloud.dev/docs` |

---

<div align="center">
<sub>LOOM · built with FastAPI, TensorFlow, Streamlit &amp; Supabase</sub>
</div>