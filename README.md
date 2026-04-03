# 📄 AI Document Analysis API

An intelligent document processing REST API that extracts, analyzes, and summarizes content from **PDF**, **DOCX**, and **image** files using **Google Gemini AI** (free tier).

---

## 🚀 Features

- **Multi-format support** — PDF, DOCX, and images (JPG, PNG, TIFF, BMP)
- **Automatic text extraction** — layout-aware PDF parsing, structured DOCX reading, and Tesseract OCR for images
- **AI-powered summarization** — concise 2–3 sentence summaries via Gemini 1.5 Flash
- **Named entity extraction** — names, dates, organizations, and monetary amounts
- **Sentiment analysis** — Positive / Negative / Neutral classification
- **API key authentication** — via `x-api-key` header
- **Swagger UI** — interactive docs at `/docs`

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11 |
| Framework | FastAPI |
| AI / LLM | Google Gemini 1.5 Flash (free) |
| PDF extraction | pdfplumber + PyMuPDF (OCR fallback) |
| DOCX extraction | python-docx |
| Image OCR | Tesseract + pytesseract + Pillow |
| Server | Uvicorn (ASGI) |
| Containerization | Docker + Docker Compose |

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.11+
- Tesseract OCR installed on your system
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### 1. Install Tesseract OCR

**Ubuntu / Debian:**
```bash
sudo apt-get update && sudo apt-get install -y tesseract-ocr tesseract-ocr-eng
```

**macOS (Homebrew):**
```bash
brew install tesseract
```

**Windows:**
Download the installer from https://github.com/UB-Mannheim/tesseract/wiki and add it to your `PATH`.

---

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/doc-analysis-api.git
cd doc-analysis-api
```

### 3. Create Virtual Environment

```bash
python -m venv venv

# Activate:
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Set Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
API_SECRET_KEY=sk_track2_987654321
```

> **Get a free Gemini API key:** Visit https://aistudio.google.com/app/apikey → Sign in → Create API Key.

### 6. Run the Server

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

The API is now live at: **http://localhost:8000**

Interactive Swagger docs: **http://localhost:8000/docs**

---

## 🐳 Docker Deployment

### Run with Docker Compose (Recommended)

```bash
# Build and start
docker-compose up --build

# Run in background
docker-compose up --build -d

# Stop
docker-compose down
```

### Run with Docker directly

```bash
docker build -t doc-analysis-api .
docker run -p 8000:8000 --env-file .env doc-analysis-api
```

---

## ☁️ Deploy to Render (Free Cloud Hosting)

1. Push your code to GitHub.
2. Go to [render.com](https://render.com) → **New Web Service** → connect your GitHub repo.
3. Render auto-detects `render.yaml`. Set your environment variables:
   - `GEMINI_API_KEY`
   - `API_SECRET_KEY`
4. Click **Deploy**. Your public URL will be shown (e.g., `https://doc-analysis-api.onrender.com`).

> **Note:** Render's free tier spins down after inactivity. Use [UptimeRobot](https://uptimerobot.com) to keep it awake with a free monitor on `/health`.

---

## 🔌 API Reference

### Authentication

All requests to `/api/document-analyze` must include the API key header:

```
x-api-key: sk_track2_987654321
```

Requests without a valid key return `401 Unauthorized`.

---

### `GET /health`

Health check endpoint.

**Response:**
```json
{ "status": "ok" }
```

---

### `POST /api/document-analyze`

Analyze a document and extract structured information.

**Headers:**
```
Content-Type: application/json
x-api-key: sk_track2_987654321
```

**Request Body:**
```json
{
  "fileName": "report.pdf",
  "fileType": "pdf",
  "fileBase64": "<base64-encoded file content>"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `fileName` | string | Name of the uploaded file |
| `fileType` | string | `pdf`, `docx`, or `image` |
| `fileBase64` | string | Base64-encoded file content |

**Success Response (200):**
```json
{
  "status": "success",
  "fileName": "report.pdf",
  "summary": "This document is a cybersecurity incident report describing a major data breach affecting multiple financial institutions through a third-party authentication vulnerability. Sensitive customer data including account identifiers and transaction histories were exposed. Regulatory investigations have been launched and institutions are urged to strengthen their security infrastructure.",
  "entities": {
    "names": ["John Smith"],
    "dates": ["March 2026", "Q1 2026"],
    "organizations": ["ABC Bank", "Federal Reserve"],
    "amounts": ["$2.5 million", "15,000 records"]
  },
  "sentiment": "Negative"
}
```

**Error Responses:**

| Code | Reason |
|------|--------|
| `401` | Missing or invalid `x-api-key` header |
| `400` | Unsupported `fileType` or invalid base64 |
| `422` | Could not extract text from the document |
| `500` | Gemini API error |

---

## 🧪 Testing with Postman

### Step 1 — Import the collection

In Postman, create a new **POST** request:
- URL: `http://localhost:8000/api/document-analyze`
- Headers:
  - `Content-Type: application/json`
  - `x-api-key: sk_track2_987654321`
- Body: raw JSON

### Step 2 — Encode your file

Use the provided helper script to convert any file to base64:

```bash
python encode_file.py path/to/your/document.pdf
```

This creates `request_body.json` in your project folder.

### Step 3 — Send the request

Copy the contents of `request_body.json` into Postman's Body → Raw → JSON.
Click **Send**.

### Step 4 — Verify the response

You should receive a `200 OK` with the structured JSON analysis.

---

### Testing with cURL

```bash
# 1. Encode your file
python encode_file.py sample.pdf

# 2. Send the request
curl -X POST http://localhost:8000/api/document-analyze \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_track2_987654321" \
  -d @request_body.json
```

---

## 📁 Project Structure

```
doc-analysis-api/
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── .env                       # Your actual env vars (not committed)
├── Dockerfile                 # Docker container definition
├── docker-compose.yml         # Docker Compose config
├── render.yaml                # Render.com deployment config
├── encode_file.py             # Helper: file → base64 JSON body
└── src/
    ├── main.py                # FastAPI app, routes, Gemini integration
    └── extractor.py           # PDF / DOCX / Image text extraction
```

---

## 🧠 Approach & Strategy

### Text Extraction

| Format | Method | Notes |
|--------|--------|-------|
| PDF | `pdfplumber` | Layout-aware extraction preserving reading order |
| PDF (scanned) | `PyMuPDF` → `pytesseract` | Fallback when digital text is absent |
| DOCX | `python-docx` | Extracts paragraphs + table cells in order |
| Image | `pytesseract` (Tesseract OCR) | Pre-processes by upscaling small images |

### AI Analysis (Gemini 1.5 Flash)

1. Extracted text (up to 8,000 chars) is sent to Gemini with a strict prompt.
2. The prompt instructs Gemini to return **only valid JSON** (no markdown fences).
3. A regex cleanup step strips any accidental code fences before `json.loads()`.
4. The structured result is validated and returned via FastAPI's typed response model.

### Why Gemini 1.5 Flash?
- **Free tier** with generous rate limits (15 RPM / 1M TPM on free plan).
- Fast inference suitable for real-time API responses.
- Strong multilingual and document understanding capabilities.

---

## 📦 Installing Dependencies Manually

```bash
# Core API
pip install fastapi uvicorn[standard] pydantic python-dotenv

# Gemini AI
pip install google-generativeai

# Document extraction
pip install pdfplumber PyMuPDF python-docx

# OCR
pip install pytesseract Pillow
```

Tesseract binary must also be installed on your OS (see Setup step 1).

---

## 🔒 Security Notes

- Never commit your `.env` file to version control — it's in `.gitignore`.
- Rotate your `API_SECRET_KEY` before deploying to production.
- For production, consider adding rate limiting with `slowapi`.

---

## 📝 License

MIT License — free to use, modify, and distribute.
# guvi_intern
