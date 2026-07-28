# Fashion MNIST Classification

A lightweight REST API built with **FastAPI** and **TensorFlow/Keras** that classifies grayscale clothing images into one of the 10 Fashion-MNIST categories.

## Features

- 🚀 Fast, async FastAPI backend
- 🧠 Pre-trained Keras CNN model for image classification
- 🔐 API key authentication for secured endpoints
- 📦 Simple image upload and JSON response
- 🌍 CORS enabled for cross-origin requests

## Classes

The model classifies images into one of the following 10 categories:

| Index | Class Name |
|-------|------------|
| 0 | T_shirt |
| 1 | Trouser |
| 2 | Pullover |
| 3 | Dress |
| 4 | Coat |
| 5 | Sandal |
| 6 | Shirt |
| 7 | Sneaker |
| 8 | Bag |
| 9 | Ankle_Boot |

## Project Structure

```
.
├── main.py                  # FastAPI app and route definitions
├── requirements.txt         # Python dependencies
├── .env.example              # Example environment variables
├── artifacts/
│   └── model.keras          # Trained Keras model
├── F_MNIST.ipynb             # Notebook: model training/experimentation
└── src/
    └── utils/
        ├── config.py         # App configuration and model loading
        ├── inference.py      # Image preprocessing and prediction logic
        └── models.py         # Pydantic response models
```

> **Note:** Adjust the structure above if your project layout differs — `config.py`, `inference.py`, and `models.py` are imported in `main.py` as `src.utils.*`.

## Requirements

- Python 3.10+
- See [`requirements.txt`](./requirements.txt) for exact package versions:
  - `fastapi==0.139.2`
  - `uvicorn==0.51.0`
  - `tensorflow==2.21.0`
  - `pydantic==2.13.4`
  - `python-dotenv==1.2.2`
  - `python-multipart==0.0.32`

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Copy the example file and fill in your own values:
   ```bash
   cp .env.example .env
   ```

   `.env` should contain:
   ```env
   APP_NAME="FASHON-MNIST-Classification"
   VERSION="1.0"
   API_SECRET_KEY="your-secret-key-here"
   ```

5. **Add the trained model**

   Place your trained Keras model at:
   ```
   artifacts/model.keras
   ```

## Running the API

Start the development server with Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:
```
http://127.0.0.1:8000
```

Interactive API docs (Swagger UI) are available at:
```
http://127.0.0.1:8000/docs
```

## API Reference

### Health Check

```http
GET /
```

**Response**
```json
{
  "message": "Up & Running"
}
```

### Classify an Image

```http
POST /classify
```

**Headers**

| Header      | Required | Description                  |
|-------------|----------|-------------------------------|
| `X-API-KEY` | Yes      | Your secret API key           |

**Body** — `multipart/form-data`

| Field  | Type | Description                          |
|--------|------|---------------------------------------|
| `file` | File | Grayscale image of a clothing item    |

**Example Request (cURL)**
```bash
curl -X POST "http://127.0.0.1:8000/classify" \
  -H "X-API-KEY: your-secret-key-here" \
  -F "file=@sneaker.png"
```

**Example Response**
```json
{
  "class_index": 7,
  "class_name": "Sneaker",
  "confidence": 98.42
}
```

**Error Responses**

| Status Code | Reason                                  |
|-------------|-------------------------------------------|
| `403`       | Invalid or missing API key                |
| `500`       | Image processing or prediction failure    |

## Image Preprocessing

Uploaded images are automatically:
1. Converted to grayscale (`L` mode)
2. Resized to `28x28` pixels
3. Normalized to a `[0, 1]` float range
4. Reshaped to match the model's expected input shape

## Model Training

The model was trained on the Fashion-MNIST dataset. See [`F_MNIST.ipynb`](./F_MNIST.ipynb) for the full training pipeline, including data loading, model architecture, training, and evaluation.

## Security Notes

- The `/classify` endpoint requires a valid `X-API-KEY` header.
- Never commit your `.env` file — it's excluded via `.gitignore`.
- CORS is currently set to allow all origins (`*`); restrict this in production.
